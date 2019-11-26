pip install pyinstaller
pyinstaller download.py -n gog-plugins-downloader --onefile
COPY gog-plugins.bat dist\
