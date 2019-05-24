SET name=OLE

pyInstaller --onefile ^
--clean ^
--name %name% ^
--icon=ole.ico ^
--add-data="README.md;." ^
--add-data="Settings.XML;." ^
--windowed ^
__main__.py

xcopy Fonts dist\Fonts /s /i
xcopy Images dist\Images /s /i
xcopy Saves dist\Saves /s /i
xcopy Stats dist\Stats /s /i
xcopy Stories dist\Stories /s /i
xcopy "Settings.XML" dist\ /i