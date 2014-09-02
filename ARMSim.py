#!/usr/bin/env python
import wx
import wx.xrc
import wx.lib.mixins.inspection
import logging

from MainFrame import MainFrame

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
