import objc, re, os
from Foundation import *
from AppKit import *
from multiprocessing import *
from ctypes import c_char_p
from PyObjCTools import NibClassBuilder, AppHelper
from sftp import sftp
from directory import initialize

# Global read only
start_time = NSDate.date()
icon_status = {
	 'idle':'icons/StatusItem@2x.png',
	 'active':'icons/menubar_busy_2@2x.png',
	 'success':'icons/menubar_complete@2x.png',
	 'failure':'icons/StatusBarButtonImage@2x.png'
}
#LALAALAL
class App(NSObject):
	icons = {}
	statusbar = None
	current_state = 'idle'
	icon_iteration = 0

	def applicationDidFinishLaunching_(self, notification):
		statusbar = NSStatusBar.systemStatusBar()
		self.statusitem = statusbar.statusItemWithLength_(NSVariableStatusItemLength)
		for i in icon_status.keys():
			self.icons[i] = NSImage.alloc().initByReferencingFile_(icon_status[i])
		self.statusitem.setImage_(self.icons[self.current_state])
		self.statusitem.setHighlightMode_(1)

		# Build the menu
		self.menu = NSMenu.alloc().init()
		item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Sync', 'sync:', '')
		self.menu.addItem_(item)
		# terminate_ is a default menu item, closes the process.
		item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')
		self.menu.addItem_(item)
		self.statusitem.setMenu_(self.menu)

	def set_Active(self):
		self.current_state = 'active'
		self.statusitem.setImage_(self.icons[self.current_state])

	def sync_(self, notification):
		self.set_Active()
		serverAddress, serverPath, localPath, username, password, sftp_list = initialize()
		print serverPath, localPath, username, password, sftp_list
		status = sftp(serverAddress, serverPath, localPath, username, password, sftp_list)
		print status



if __name__ == "__main__":
	app = NSApplication.sharedApplication()
	delegate = App.alloc().init()
	app.setDelegate_(delegate)
	AppHelper.runEventLoop()

