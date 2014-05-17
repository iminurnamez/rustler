import sys
from cx_Freeze import setup, Executable

base = None 
if sys.platform == "win32":
    base = "Win32GUI"
   
exe = Executable(script="rustler.py", base=base)
include_files=["resources/music", "resources/graphics", "resources/sound",
                     "resources/fonts", "resources/json"]
includes=[]
excludes=[]
packages=[]

setup(version="0.1",
         description="Pyweek 18",
         author="iminurnamez",
         name="rustler",
         options={"build_exe": {"includes": includes, "include_files": include_files, "packages": packages, "excludes": excludes}},
         executables=[exe])

