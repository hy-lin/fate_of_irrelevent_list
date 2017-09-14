pyinstaller FateOfIrreleventList1.py -F -i resources\uzh.ico
mkdir dist\resources
copy resources\*.* dist\resources
mkdir dist\Data
mkdir dist\sdl_dll
copy sdl_dll\*.* dist\sdl_dll