#!/usr/bin/env python
import wx
import wx.xrc

import wx.lib.mixins.inspection

import logging

###########################################################################
## Handle the External window
###########################################################################
class ExternalWindow(wx.ScrolledWindow):
    def __init__(self, parent, id, pos, size, style, title):
        self.parent = parent
        wx.ScrolledWindow.__init__(self, parent, -1, style=style|wx.TAB_TRAVERSAL, name=title)
        gb = wx.GridBagSizer(vgap=0, hgap=3)
        self.sizer = gb
        self._labels = []
        for y in xrange(1,30):
            self._labels.append(wx.StaticText(self, -1, "Label #%d" % (y,)))
            gb.Add(self._labels[-1], (y,1), (1,1))
        self.SetSizer(self.sizer)
        fontsz = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT).GetPixelSize()
        self.SetScrollRate(fontsz.x, fontsz.y)
        self.EnableScrolling(True,True)

    def OnInnerSizeChanged(self):
        w,h = self.sizer.GetMinSize()
        self.SetVirtualSize((w,h))
