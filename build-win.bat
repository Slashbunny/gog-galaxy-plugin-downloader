pip install pyinstaller
pyinstaller download.py -n gog-plugins-downloader-stores --onefile
copy dist\gog-plugins-downloader-stores.exe dist\gog-plugins-downloader-games.exe
copy dist\gog-plugins-downloader-stores.exe dist\gog-plugins-downloader-emulators.exe
