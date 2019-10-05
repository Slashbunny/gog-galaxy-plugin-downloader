#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import shutil
import tempfile
import yaml
import zipfile
from io import BytesIO
from string import Template
from urllib.parse import urlparse
from urllib.request import urlopen


def get_plugin_config(config_uri):
    """
    Downloads/opens configuration yaml file, returns
    dict of Galaxy plugins
    """
    # Try to open the URI as a URL or fall back to opening local file
    try:
        urlparse(config_uri)
        url = urlopen(config_uri)
        yaml_data = url.read()
    except ValueError:
        with open(config_uri, 'r') as file_data:
            yaml_data = file_data.read()

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
            print('NOTICE: Skipping "{}" download, {} already exists'
                  .format(name, dest_dir))
            continue
        else:
            print('Downloading {} version {}'.format(name, version))

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


if __name__ == "__main__":
    """
    Entry point to script

    - Parses command line arguments
    - Calls function to fetch/parse plugin config yaml file
    - Calls function to download plugins
    """
    # Define script arguments
    parser = argparse.ArgumentParser(
                                 description='Download GOG Galaxy 2.0 Plugins')
    parser.add_argument('-c', '--conf',
                        default='https://raw.githubusercontent.com/'
                                'Slashbunny/gog-galaxy-plugin-downloader/'
                                'master/plugins.yaml',
                        help='Path or URL to plugin configuration YAML file')
    parser.add_argument('-d', '--dest', required=True,
                        help='Destination directory for plugins')

    # Parse arguments
    args = parser.parse_args()

    # Download/Load Plugin Data
    plugins = get_plugin_config(args.conf)

    # Replace variables in templated strings
    plugins = process_template_strings(plugins)

    # Download plugins
    download_plugins(plugins, args.dest)
