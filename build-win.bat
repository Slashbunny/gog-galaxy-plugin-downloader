pip install -r requirements.txt
pip install -U pyinstaller
pyinstaller.exe download.py -n gog-plugins-downloader --onefile
COPY gog-plugins.bat dist\
