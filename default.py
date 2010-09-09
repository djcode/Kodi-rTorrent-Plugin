# main imports
import sys
import os
import urllib
import xbmc
import xbmcgui
import xbmcplugin

#adding plugin libary to python library path
sys.path.append (xbmc.translatePath(os.path.join(os.getcwd(), 'resources', 'lib')))

#extra imports
from functions import *
g = __import__('global')

#Set plugin fanart
#TODO: Check to see if this actually works or not, haven't managed to see it yet!
xbmcplugin.setPluginFanart(int(sys.argv[1]), os.path.join(os.getcwd(),'fanart.jpg'))

params=get_params()

url=None
hash=None
mode=None
numfiles=None
method=None
arg1=None
arg2=None
arg3=None
test=False

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        hash=str(params["hash"])
except:
        pass
try:
        mode=str(params["mode"])
except:
        pass
try:
        numfiles=int(params["numfiles"])
except:
        pass
try:
        method=str(urllib.unquote_plus(params["method"]))
except:
        pass		
try:
        arg1=str(urllib.unquote_plus(params["arg1"]))
except:
        pass		
try:
        arg2=str(urllib.unquote_plus(params["arg2"]))
except:
        pass		
try:
        arg3=str(urllib.unquote_plus(params["arg3"]))
except:
        pass
		
#print "Params: "+str(params) print "Mode: "+str(mode) print "Method: "+str(method) #print "Arg1: "+str(arg1) print "Arg2: "+str(arg2) print "URL: "+str(url)

if mode==None or mode=='files' or mode=='action':

	test=connectionOK()

if test==True:
	if mode==None:
		from mode_main import *
		main()
	elif mode=='files':
		from mode_files import *
		main(hash,numfiles)
	elif mode=='action':
		from mode_action import *
		main(method,arg1,arg2,arg3)

if mode=='play':
		from mode_play import *
		main(url,arg1)