#!/usr/bin/env python
import wx
import wx.xrc

import wx.lib.mixins.inspection

import logging

###########################################################################
## Handle the Cmd window
###########################################################################
class CmdWindow(wx.TextCtrl):
    def __init__(self, parent, id, pos, size, style):
        self.parent = parent
        wx.TextCtrl.__init__(self, parent, -1, style=style|wx.TAB_TRAVERSAL|wx.TE_MULTILINE, name=u"IO")
        fontsz = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT).GetPixelSize()
