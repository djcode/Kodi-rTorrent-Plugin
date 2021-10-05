''' Wrapper around xmlrpc with Kodi-specific behaviour '''
import os
import sys
import xmlrpc.client
from urllib.parse import urlparse
import xbmc
import xbmcgui
from . import rtorrent_xmlrpc
from . import globals as g

class RTorrentKodiClient:
    ''' Wrapper around xmlrpc calls '''
    def __init__(self):
        self.uri = urlparse(g.__setting__('uri'))
        if self.uri.scheme == 'scgi':
            self.rtc = rtorrent_xmlrpc.SCGIServerProxy(self.uri.geturl())
        else:
            self.rtc = xmlrpc.client.ServerProxy(self.uri.geturl())
    def __getattr__(self, name):
        try:
            result = getattr(self.rtc, name)
        except xmlrpc.client.ProtocolError as err:
            xbmcgui.Dialog().ok('Error','An XMLRPC protocol error occurred. Submit a bug report!')
            xbmc.log("An XMLRPC protocol error occurred")
            xbmc.log("URL: %s" % err.url)
            xbmc.log("HTTP/HTTPS headers: %s" % err.headers)
            xbmc.log("Error code: %d" % err.errcode)
            xbmc.log("Error message: %s" % err.errmsg)
        except xmlrpc.client.Fault as err:
            xbmcgui.Dialog().ok('Error','An XMLRPC fault occurred. Submit a bug report!')
            xbmc.log("An XMLRPC fault occurred")
            xbmc.log("Fault code: %d" % err.faultCode)
            xbmc.log("Fault string: %s" % err.faultString)
        except ConnectionRefusedError:
            xbmcgui.Dialog().ok('Error','Connection to rTorrent refused. Check firewall settings.')
        except TimeoutError:
            xbmcgui.Dialog().ok('Error','Connection to rTorrent timed out. Check the host is correct.')
        except:
            xbmcgui.Dialog().ok('Error','Unexpected error occurred.')
            xbmc.log("Unexpected error:", sys.exc_info()[0])
            raise
        return result
    def local(self):
        ''' Work out if rTorrent is running on the same machine. '''
        local_names = ['localhost', '127.0.0.1', os.getenv('COMPUTERNAME'), None]
        if self.uri.hostname in local_names:
            return True
        return False


def error_dialog(message, show_settings=True):
    ''' Display error dialog '''
    if show_settings:
        dialog = xbmcgui.Dialog().yesno(
            g.__lang__(30155),
            message, #g.__lang__(30156),
            g.__lang__(30157),
            g.__lang__(30158)
        )
        if dialog:
            g.__addon__.openSettings()
            xbmc.executebuiltin('RunAddon(%s)' % g.__addonID__)
            sys.exit()
        else:
            sys.exit()
    else:
        xbmcgui.Dialog().ok(
            g.__lang__(30155),
            message, #g.__lang__(30156),
        )
        sys.exit()
