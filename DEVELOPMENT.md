## DEVELOPMENT

To modify the UI use the qtdesigner. For python you can launch the qt5-tools:

qt5-tool.exe designer 

Open the views/main.ui, modify it and save it. Then you have to export it:

pyuic5 views/main.iu -o views/main.py

To create an executable use the pyinstaller:

pyinstaller --onefile .\log_config_creator.pypyinstaller 