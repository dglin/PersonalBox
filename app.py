import objc, re, os
from Foundation import *
from AppKit import *
from multiprocessing import *
from ctypes import c_char_p
from PyObjCTools import NibClassBuilder, AppHelper
import time
# Local files
import sftp


# Global read only
start_time = NSDate.date()
icon_status = {
	 'idle':'icons/StatusBarButtonImage@2x.png',
	 'active_0':'icons/menubar_busy_2@2x.png', 
	 'active_1':'icons/menubar_busy_3@2x.png',
	 'active_2':'icons/menubar_busy_4@2x.png',
	 'active_3':'icons/menubar_busy_5@2x.png',
	 'active_4':'icons/menubar_busy_6@2x.png',
	 'active_5':'icons/menubar_busy_7@2x.png',
	 'active_6':'icons/menubar_busy_8@2x.png',
	 'active_7':'icons/menubar_busy_9@2x.png',
	 'active_8':'icons/menubar_busy_10@2x.png',
	 'active_9':'icons/menubar_busy_11@2x.png',
	 'active_10':'icons/menubar_busy_12@2x.png',
	 'active_11':'icons/menubar_busy_13@2x.png',
	 'complete':'icons/menubar_complete@2x.png'
}

def sftp_(c_storage):
	c_storage.value = "Success"

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


	def sync_(self, notification):
		# Start timer
		self.timer = NSTimer.alloc().initWithFireDate_interval_target_selector_userInfo_repeats_(start_time, 0.1, self, 'tick:', None, True)
		loop = NSRunLoop.currentRunLoop().addTimer_forMode_(self.timer, NSDefaultRunLoopMode)
		self.timer.fire()

		manager = Manager()
		status = manager.Value(c_char_p, "Placeholder")
		p = Process(target=sftp_, args=(status,))
		p.start()
		p.join()
		
		print 'Hello' + status.value
		if status.value == "Success":
			print 'David'
			self.icon_iteration = 0
			self.current_state = 'idle'
			self.statusitem.setImage_(self.icons[self.current_state])
			self.timer = None
			print 'Trying to stop'

	def tick_(self, notification):
		self.current_state = 'active_' + str(self.icon_iteration)
		self.statusitem.setImage_(self.icons[self.current_state])
		self.icon_iteration += 1
		if self.icon_iteration == 11:
			self.icon_iteration = 0

if __name__ == "__main__":
	app = NSApplication.sharedApplication()
	delegate = App.alloc().init()
	app.setDelegate_(delegate)
	AppHelper.runEventLoop()

