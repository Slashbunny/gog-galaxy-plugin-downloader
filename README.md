# GOG Galaxy Plugins Downloader

Downloads all GOG Galaxy 2.0 Plugins to a directory. By default, it uses the
list of plugins from this from this repository on Github (`plugins.yaml`).

If does not modify any directories in the destination folder. You should
manually delete your existing/old plugins.

# Requirements

Install Python 3 on your OS. Clone or [download](https://github.com/Slashbunny/gog-galaxy-plugin-downloader/archive/master.zip)+extract this repository into a directory of your choice.

# Usage

Open a command line terminal and navigate to the directory where you downloaded
or cloned this repository.

```
cd Desktop\gog-galaxy-plugin-downloader-master
```

Install dependencies

```
pip install -r requirements.txt
```

Download plugins to Galaxy's "installed" directory:

```
python download.py -d %localappdata%\GOG.com\Galaxy\plugins\installed
```

# Advanced Usage

By default the list of plugins comes from the YAML file in this repository. You
can use your own local plugins YAML file like this:

```
python download.py -d output-directory -c plugins.yaml
```

Or use your own remote plugins YAML file hosted at any URL:

```
python download.py -d output-directory -c https://www.mydomain.com/gog-plugins.yaml
```

# Contibute

Open a Merge Request with updates to plugins in `plugins.yaml` so everyone
can benefit

