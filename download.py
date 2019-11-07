#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import shutil
import sys
import tempfile
import yaml
import zipfile
from io import BytesIO
from string import Template
from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.error import URLError

__version__ = '0.0.3'

# Base URL to plugins
plugin_url = 'https://raw.githubusercontent.com/Slashbunny/' \
             'gog-galaxy-plugin-downloader/master/'


def get_plugin_config(config_uri):
    """
    Downloads/opens configuration yaml file, returns
    dict of Galaxy plugins
    """
    # Try to open the URI as a URL or fall back to opening local file
    try:
        config_uri_parsed = urlparse(config_uri)
        if config_uri_parsed.scheme in ['https', 'http']:
            url = urlopen(config_uri)
            yaml_data = url.read()
        else:
            with open(config_uri, 'r') as file_data:
                yaml_data = file_data.read()
    except URLError as e:
        print(e)

    # Parse the YAML configuration
    try:
        plugin_data = yaml.safe_load(yaml_data)

        return plugin_data['plugins']
    except yaml.YAMLError as e:
        print(e)


def process_template_strings(data):
    """
    Replaces $variables in strings with corresponding variables in plugin data
    """
    for plugin_name, plugin_data in data.items():
        version = plugin_data['version']

        for key, value in plugin_data.items():
            if key == 'version':
                continue

            # Replace references to $name and $version with the real values
            data[plugin_name][key] = Template(value).substitute(
                                        name=plugin_name,
                                        version=version)

    return data


def download_plugins(data, dest):
    """
    Downloads and extracts plugins

    If the destination directory already exists, the plugin is skipped
    """
    for name, data in data.items():
        version = data['version']
        url = data['url']
        if 'archive_path' in data:
            archive_path = data['archive_path']
        else:
            archive_path = None

        # Destination directory
        dest_dir = os.path.join(dest, name + '_v' + version)

        if os.path.isdir(dest_dir):
            print('NOTICE: Skipping "{}" download, "{}" already exists'
                  .format(name, dest_dir))
            continue
        else:
            print('Downloading "{}" version "{}"'.format(name, version))

        # Download zip file into memory
        plugin_url = urlopen(url)
        plugin_zip = zipfile.ZipFile(BytesIO(plugin_url.read()))

        # Extract zip directly into destination if there are no sub-folders
        #  to deal with
        if not archive_path:
            plugin_zip.extractall(path=dest_dir)
        else:
            # Create temporary directory for extraction
            tmp_dir = tempfile.TemporaryDirectory(prefix='galaxy-plugin')

            # Extract zip to temporary directory
            plugin_zip.extractall(path=tmp_dir.name)

            # Move sub-directory into final destination directory
            shutil.move(os.path.join(tmp_dir.name, archive_path), dest_dir)

            # Cleanup temporary directory
            tmp_dir.cleanup()


def delete_old_plugins(data, dest):
    """
    Deletes versions of plugins that don't match the yaml manifest. In theory
    this should only be older versions, but any version that doesn't match
    the yaml definition will be deleted

    This explicitly does not touch other directories that do not match the
    known plugin names. It only deletes directories of the format:

        <plugin name>_v<version>

    If the version doesn't match the yaml definition, the directory is removed
    """
    # Loop over each plugin
    for name, data in data.items():
        current_plugin_dir = name + '_v' + data['version']

        # Loop through directories in the destination directory
        for item in os.listdir(dest):
            full_path = os.path.join(dest, item)

            # Skip non-directories
            if not os.path.isdir(full_path):
                continue

            # Skip directory names that are in the valid plugin directory array
            if item == current_plugin_dir:
                continue

            # If any other directory begins with <plugin_name>_v, delete it
            if item.startswith(name + '_v'):
                print('Deleting wrong version "{}" from "{}"'
                      .format(item, dest))
                shutil.rmtree(full_path)


if __name__ == "__main__":
    """
    Entry point to script

    - Parses command line arguments
    - Calls function to fetch/parse plugin config yaml file
    - Calls function to download plugins
    - Calls function to delete old/invalid plugins
    """
    # Define script arguments
    parser = argparse.ArgumentParser(
                        description='GOG Galaxy Plugin Downloader')

    if os.name == "nt":
        # Windows Defaults

        # Plugin config default: Depends on which .exe is being run
        if sys.argv[0].endswith('-emulators.exe'):
            plugins_file = 'plugins-emulators.yaml'
        elif sys.argv[0].endswith('-games.exe'):
            plugins_file = 'plugins-games.yaml'
        else:
            plugins_file = 'plugins.yaml'

        parser.add_argument('-c', '--conf', default=plugin_url + plugins_file,
                            help='Path/URL to plugin configuration YAML file')

        # Destination default: %LOCALAPPDATA%\GOG.com\Galaxy\plugins\installed\
        plugins_dir = os.path.join(os.environ['localappdata'], 'GOG.com',
                                   'Galaxy', 'plugins', 'installed')

        parser.add_argument('-d', '--dest', default=plugins_dir,
                            help='Destination directory for plugins')
    else:
        # Non-Windows Defaults
        parser.add_argument('-c', '--conf', default=plugin_url + 'plugins.yml',
                            help='Path/URL to plugin configuration YAML file')
        parser.add_argument('-d', '--dest', required=True,
                            help='Destination directory for plugins')

    parser.add_argument('--version', action='version',
                        version='{}'.format(__version__))

    # Parse arguments
    args = parser.parse_args()

    # Download/Load Plugin Data
    plugins = get_plugin_config(args.conf)

    # Replace variables in templated strings
    plugins = process_template_strings(plugins)

    # Download plugins
    download_plugins(plugins, args.dest)

    # Delete old plugins
    delete_old_plugins(plugins, args.dest)

    # If on Windows, prompt user to press a button before exiting
    if os.name == "nt":
        input('Process complete! Press the Enter key to exit...')
