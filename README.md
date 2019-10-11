# GOG Galaxy Plugins Downloader

Downloads all GOG Galaxy 2.0 Plugins to a directory. By default, it uses the
list of plugins from this from this repository on Github (`plugins.yaml`).

# Basic Usage

* Download the latest release from the [Releases](https://github.com/Slashbunny/gog-galaxy-plugin-downloader/releases) page.
* Extract the zip file anywhere on your PC.
* Double click on `gog-plugins-downloader.exe` to run the program to download or
update your plugins.

This will only work for Windows. If you are using another OS, you will need to
follow the Advanced instructions below.

# Advanced Usage

## Requirements

Install Python 3 on your OS. Clone or [download](https://github.com/Slashbunny/gog-galaxy-plugin-downloader/archive/master.zip), then extract this repository into a directory of your choice.

## Running the Program

Open a command line terminal and navigate to the directory where you downloaded
or cloned this repository.

```
cd Desktop\gog-galaxy-plugin-downloader-master
```

Install dependencies

```
pip install -r requirements.txt
```

Download plugins to Galaxy's "installed" directory on Windows (`%localappdata\GOG.com\Galaxy\plugins\installed`):

```
python download.py
```

You can also download to a custom directory (Required on non-Windows systems):

```
python download.py -d output-folder
```

## Custom Plugins

By default the list of plugins comes from the YAML file in this repository. You
can use your own local plugins YAML file like this:

```
python download.py -d output-directory -c plugins.yaml
```

Or use your own remote plugins YAML file hosted at any URL:

```
python download.py -d output-directory -c https://www.mydomain.com/gog-plugins.yaml
```

## Building the Executable

If you want to build the Windows executable, you must follow these steps on
Windows.

First, install pyinstaller:

```
pip install pyinstaller
```

Then build the executable as follows:

```
pyinstaller download.py -n gog-plugins-downloader --onefile
```

`gog-plugins-downloader.exe` will be in the `dist/` subfolder.

# Contibute

Open a Merge Request with updates to plugins in `plugins.yaml` so everyone
can benefit

