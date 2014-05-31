#!/usr/bin/env python
import wx
import wx.xrc
import wx.lib.mixins.inspection
import logging

from MainFrame import MainFrame

# Modes: abort        10111
#        fast int req 10001
#        int req      10010
#        supervisor   10011
#        system       11111
#        undef        11011
#        user         10000
#
# Addresses
# 00 - reset
# 04 - undef
# 08 - software int
# 0c - prefetch abort
# 10 - data abort
# 14 - reserved
# 18 - int req IRQ
# 1c - fast int req

registerOtherSplitter = 0
memoryOtherSplitter = 0
memorySplitter = 0
codeOtherSplitter = 0
externalXSplitter = 0

###########################################################################
## Main App
###########################################################################
class ARMSimApp (wx.App, wx.lib.mixins.inspection.InspectionMixin):
    def OnInit(self):
        self.Init()  # initialize the inspection tool
        frame = MainFrame(None)
        frame.Show()
        self.SetTopWindow(frame)
        return True
    
app = ARMSimApp()
app.MainLoop()