pip install pyinstaller==3.6
pyinstaller download.py -n gog-plugins-downloader --onefile
COPY gog-plugins.bat dist\
