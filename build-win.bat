pip install pyinstaller
pyinstaller download.py -n gog-plugins-downloader --onefile
copy dist\gog-plugins-downloader.exe dist\gog-plugins-downloader-games.exe
copy dist\gog-plugins-downloader.exe dist\gog-plugins-downloader-emulators.exe
