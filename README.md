# scenes-configurator

To generate executable for Windows:

`pyinstaller --onefile --windowed --add-data "icon.png:." --add-data "pulse-logo.png:." --add-data "favicon.ico:." --icon=favicon.ico .\ControlServerConfig.py`

Some code for Linux:

`
source /path/to/your/venv/bin/activate
pip install customtkinter pillow
`