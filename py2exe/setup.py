from distutils.core import setup

import py2exe, os, sys, shutil, pygame

for p in sys.path:
	if p[-13:] == "site-packages":
		sppath = p
try:
	shutil.rmtree(sppath+"/rtslib")
except:
	print "RTSLIB not removed"
try:
	shutil.rmtree("../../Build")
except:
	print "Build folder not removed"
os.makedirs("../../Build")

shutil.copytree("../rtslib", sppath+"/rtslib")

sys.argv.append("py2exe")

#Hack to get fonts to work!
origIsSystemDLL = py2exe.build_exe.isSystemDLL
def isSystemDLL(pathname):
       if os.path.basename(pathname).lower() in ["libfreetype-6.dll", "libogg-0.dll","sdl_ttf.dll"]:
               return 0
       return origIsSystemDLL(pathname)
py2exe.build_exe.isSystemDLL = isSystemDLL
#From http://thadeusb.com/weblog/2009/4/15/pygame_font_and_py2exe

exc = ['email', 'tk', 'socket', 'tcl', 'distutils', 'urllib', 'urllib2', "urlparse", 'AppKit', 'curses', 'webbrowser', 'setuptools', 'pydoc', '_ssl', "BaseHTTPServer"]
opts = {'py2exe': {"optimize":2, 'bundle_files':1, 'includes':["rtslib", "pygame"], 'dist_dir':"../../Build", 'dll_excludes':['pywintypes27.dll'], 'excludes':exc}}

setup(name='Save Our City', data_files=[], windows=[{'script':'../main.py', "icon_resources": [(1, "../resources/icon.ico")]}], options=opts, zipfile=None)

shutil.rmtree("build")
shutil.copytree("../resources", "../../Build/resources")
os.remove("../../Build/w9xpopen.exe")
os.rename("../../Build/main.exe", "../../Build/Save Our City.exe")
#Write default saves
os.mkdir("../../Build/saves/")
for save in ["1", "2", "3"]:
	f = open("../../Build/saves/"+save+".sav", "w")
	f.write("0")
	f.close()
#Write default settings
f = open("../../Build/resources/settings.cfg", "w")
f.write("0")
f.close()