# GOG Galaxy Plugins Downloader

## Summary

This program downloads GOG Galaxy 2.0 Plugins and installs them to the proper location.

You _probably_ do not want to use this software anymore.

As of the Galaxy 2.0 Euporie update, released November 19th, 2019, the GOG Galaxy
client automatically downloads and updates plugins from within the Integrations
screens. You should install plugins using GOG Galaxy itself, not this software.

However, not all plugins are available from the GOG Galaxy interface. If you are
interested in those other plugins, this program may be beneficial to you.

The plugins are from Mixaill's excellent [Awesome GOG Galaxy](https://github.com/Mixaill/awesome-gog-galaxy)
repository. If you'd like to see a plugin included in this program, please
request it be added to that project _first_.

# Usage

This section is meant for Windows users only. If you are using another OS,
you will need to follow the Advanced instructions below.

* Download the latest release from the [Releases](https://github.com/Slashbunny/gog-galaxy-plugin-downloader/releases) page.
* Extract the zip file anywhere on your PC.
* Within the zip file, there is a single executable:
   * `gog-plugins-downloader.exe`: Downloads and installs all Friends of Galaxy plugins
   * If you want to install other plugins, you'll need to create a `.bat` file with the plugins you are interested in (see "Customizing the list..." section below)
* Run the program regularly to keep your plugins up to date

## Install through Scoop

Alternatively, on Windows, [Scoop](https://scoop.sh/) package manager can be used to install and update this tool:

```
scoop bucket add extras
scoop install gog-galaxy-plugin-downloader
```

## Customizing the list of plugins being downloaded

If you want to download a specific set of plugins, refer to the `gog-plugins.bat` file that comes with the
release. Open it in Notepad. Plugins are specified via a comma-separated list, using the `-p` flag. For example:

```
gog-plugins-downloader.exe -p steam,battlenet,humblebundle,ffxiv,gw2,minecraft,poe,snes,nes
```

Change the list to whatever you require and save the `.bat` file. Double click
on the `.bat` file to install or update the list of plugins.

# Advanced Usage

## Requirements

Install Python 3 on your OS. Clone or [download](https://github.com/Slashbunny/gog-galaxy-plugin-downloader/archive/master.zip),
then extract this repository into a directory of your choice.

## Running the Program

Open a command line terminal and navigate to the directory where you downloaded
or cloned this repository. In this example, it was extracted to a folder on the
Desktop.

```
cd Desktop\gog-galaxy-plugin-downloader-master
```

Next, install python dependencies:

```
pip install -r requirements.txt
```

To download default plugins to Galaxy's "installed" directory on Windows (`%localappdata%\GOG.com\Galaxy\plugins\installed`):

```
python download.py
```

### List Available Plugins

```
python download.py -l
```

## Custom Parameters

### Custom Output Directory

You can download to a custom directory (This is required on non-Windows systems):

```
python download.py -d output-folder
```

For example, on MacOS, to install Store plugins to the default Galaxy plugins folder:

```
python download.py -d "${HOME}/Library/Application Support/GOG.com/Galaxy/plugins/installed/"
```

### Custom Plugin Lists

You can use your own local plugins YAML file like this:

```
python download.py -c plugins.yaml
```

Or use your own remote plugins YAML file hosted at any URL:

```
python download.py -c https://www.mydomain.com/gog-plugins.yaml
```

### Filtering Plugins

Rather than install all the plugins referenced in a `yaml` file, you can filter
the list using the `-p` option:

```
python download.py -p battlenet,steam,rockstar,humblebundle
```

## Building the Executable

If you want to build the Windows executable, you can run the following batch
files on a Windows PC:

```
build-win.bat
```

The `.exe` files will be in the `dist/` subfolder.
