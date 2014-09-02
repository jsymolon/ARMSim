#!/usr/bin/env python
import wx
import wx.xrc
import wx.lib.mixins.inspection
import logging
import globals
import ARMCPU
import utils

###########################################################################
## Handle the Register window
###########################################################################
class Registers(wx.Panel):

    def __init__(self, parent, id, pos, size, style):
        self.parent = parent
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY, style=style, name=u"Registers")
        gb = wx.GridBagSizer(vgap=0, hgap=3)
        self.sizer = gb
        self.SetSizer(self.sizer)
        self.font = wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL)
        fontsz = self.font.GetPixelSize()
        self.fheight = fontsz.GetHeight()
        self.Bind( wx.EVT_PAINT, self.onPaint )

    def onPaint(self, event):
        dc = wx.PaintDC(self)
        x1,y1,w,h = dc.GetBoundingBox()
        dc.DrawRectangle(x1, y1, w, h)
        y1 = abs(y1)
        h = abs(h)
        # convert pixels back to lines
        self.curRow = abs(y1) / self.fheight;
        dc.SetFont(self.font)
        for i in range(self.curRow, globals.LAST_REG):  # 16 registers
            self.h = self.fheight * i - y1
            dc.SetPen(wx.Pen(wx.NamedColour('white'), 20))
            dc.DrawRectangle(0, self.h+10, w, self.fheight)
            dc.SetPen(wx.Pen(wx.NamedColour('black'), 20))
            out = utils.buildRegValString(self, i)
            dc.DrawText(out, 5, self.h)

    def OnInnerSizeChanged(self):
        w,h = self.sizer.GetMinSize()
        self.SetVirtualSize((w,h))
