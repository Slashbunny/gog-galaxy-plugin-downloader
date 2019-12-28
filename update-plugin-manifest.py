#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import json
import ruamel.yaml
from urllib.request import urlopen

__version__ = '0.0.1'

# Friends of Galaxy Config File
fog_cfg = 'https://raw.githubusercontent.com/FriendsOfGalaxy/cfg/master/' \
          'config.json'


def fetch_fog_config_data(cfg):
    """
    Fetches Friends of Galaxy's master cfg file, then loops through all plugins
    and determines the latest version information
    """
    results = {}

    # Download and parse cfg file
    url = urlopen(cfg)
    json_data = url.read()
    plugins = json.loads(json_data)

    for p in plugins['plugins']:
        platform = p['platform']
        guid = p['guid']
        cfg_url = p['update_url']

        # Download platform's update file
        update_url = urlopen(cfg_url)
        update_data = update_url.read()

        update = json.loads(update_data)
        version = update['tag_name']
        dl_url = ''

        for a in update['assets']:
            if 'win' in a['name']:
                dl_url = a['browser_download_url']

        # If version is prefixed with a "v", remove it
        if version.startswith('v'):
            version = version[1:]

        # Save results to dict
        results[platform] = {
            "guid": guid,
            "version": version,
            "dl_url": dl_url
        }

        print('Found plugin {} version {}'.format(
              platform, version))

    return results


def update_plugins_manifest(data, manifest_file):
    """
    Updates manifest file with new data
    """

    # Open/Read Existing file
    with open(manifest_file, 'r') as file_data:
        yaml_data = file_data.read()

    yaml = ruamel.yaml.YAML()
    yaml.indent(mapping=4, sequence=2, offset=0)
    yaml.preserve_quotes = True
    plugin_data = yaml.load(yaml_data)

    # Loop through each item in plugins manifest
    for plugin, cur_data in plugin_data['plugins'].items():
        # Skip non-FOG plugins
        if plugin not in data:
            continue

        cur_guid = cur_data['guid']
        cur_version = cur_data['version']
        cur_url = cur_data['url']
        fog_guid = data[plugin]['guid']
        fog_version = data[plugin]['version']
        fog_url = data[plugin]['dl_url']

        print('Checking manifest for {}'.format(plugin))

        if cur_guid != fog_guid:
            print('   New GUID (old: "{}" new: "{}")'.format(
                  cur_guid, fog_guid))
            plugin_data['plugins'][plugin]['guid'] = fog_guid

        if cur_version != fog_version:
            print('   New Version (old: "{}" new: "{}")'.format(
                  cur_version, fog_version))
            plugin_data['plugins'][plugin]['version'] = fog_version

        if cur_url != fog_url:
            print('   New URL (old: "{}" new: "{}")'.format(
                  cur_url, fog_url))
            plugin_data['plugins'][plugin]['url'] = fog_url

    # Write the updated yaml file to disk
    with open(manifest_file, 'w') as yaml_file:
        yaml.dump(plugin_data, yaml_file)

    # Check that there aren't any items in the fog config that are missing from
    # the manifest
    for fog_name in data:
        if fog_name not in plugin_data['plugins'].keys():
            print('ERROR: {} not found in plugin manifest!'.format(fog_name))


if __name__ == "__main__":
    """
    Entry point to script

    - Downloads Friends of Galaxy's config
    - Loops through each plugin and pulls in current version information
    - Updates plugins.yaml
    """

    # Define script arguments
    parser = argparse.ArgumentParser(
                        description='Plugin Manifest Updater')

    parser.add_argument('--version', action='version',
                        version='{}'.format(__version__))

    # Parse arguments
    args = parser.parse_args()

    # Download/Load Plugin Data
    fog_plugins = fetch_fog_config_data(fog_cfg)

    # Update existing plugins manifest
    update_plugins_manifest(fog_plugins, './plugins.yaml')
