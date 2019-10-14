# GOG Galaxy Plugins Downloader

Downloads all GOG Galaxy 2.0 Plugins to a directory. By default, it uses the
list of plugins from this from this repository on Github (`plugins.yaml`).

The plugins are from Mixaill's excellent [Awesome GOG Galaxy](https://github.com/Mixaill/awesome-gog-galaxy)
repository. If you'd like to see a plugin included in this program, please
request it be added to that project _first_.

# Basic Usage

* Download the latest release from the [Releases](https://github.com/Slashbunny/gog-galaxy-plugin-downloader/releases) page.
* Extract the zip file anywhere on your PC.
* Within the zip file, there are 3 programs:
   * `gog-plugins-downloader-stores`: Downloads and installs plugins for game stores- Steam, Origin, Uplay, Epic, PSN, BattleNet, and more.
   * `gog-plugins-downloader-games`: Downloads and installs plugins for single game launchers- Minecraft, Final Fantasy XIV, Path of Exile, Guild Wars 2, and more.
   * `gog-plugins-downloader-emulators`: Downloads and installs plugins for emulators- bSNES, RetroArch, Cemu, Dolphin, Citra, mGBA, and more.
* Run the programs of your choice regularly to keep your plugins up to date

This will only work for Windows. If you are using another OS, you will need to
follow the Advanced instructions below.

# Install through Scoop

Alternatively, on Windows, [Scoop](https://scoop.sh/) package manager can be used to install and update this tool: `scoop install gog-galaxy-plugin-downloader`.

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

To download Store plugins to Galaxy's "installed" directory on Windows (`%localappdata%\GOG.com\Galaxy\plugins\installed`):

```
python download.py
```

### Install Single Game Launcher Plugins

```
python download.py -c https://raw.githubusercontent.com/Slashbunny/gog-galaxy-plugin-downloader/master/plugins-games.yaml
```

or:

```
python download.py -c plugins-games.yaml
```

### Install Emulator Plugins

```
python download.py -c https://raw.githubusercontent.com/Slashbunny/gog-galaxy-plugin-downloader/master/plugins-emulators.yaml
```

or

```
python download.py -c plugins-emulators.yaml
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

### Custom Plugins

You can use your own local plugins YAML file like this:

```
python download.py -c plugins.yaml
```

Or use your own remote plugins YAML file hosted at any URL:

```
python download.py -c https://www.mydomain.com/gog-plugins.yaml
```

## Building the Executables

If you want to build the Windows executables, you can run the following batch
files on a Windows PC:

```
build-win.bat
```

The `.exe` files will be in the `dist/` subfolder.
