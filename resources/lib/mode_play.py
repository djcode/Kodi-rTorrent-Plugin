# Imports
import xbmc
import xbmcgui
g = __import__('global')

#XBMC file player code
def main(url,arg1):
	# Check to see if the file has completely downloaded.
	if int(arg1)==0:
		dialog = xbmcgui.Dialog()
		ret = dialog.yesno(g.__lang__(30150), g.__lang__(30151), g.__lang__(30152))
		if ret==True:
			xbmc.Player().play(url);
	else:
		xbmc.Player().play(url);