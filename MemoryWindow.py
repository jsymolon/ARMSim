#!/usr/bin/env python
import wx
import wx.xrc

import wx.lib.mixins.inspection

import logging
import globals

###########################################################################
## Handle the Memory window
###########################################################################
class MemoryWindow(wx.ScrolledWindow):
    def __init__(self, parent, id, pos, size, style):
        self.parent = parent
        wx.ScrolledWindow.__init__(self, parent, -1, style=style|wx.TAB_TRAVERSAL, name=u"Memory")
        gb = wx.GridBagSizer(vgap=0, hgap=3)
        self.sizer = gb
        self.SetSizer(self.sizer)
        fontsz = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT).GetPixelSize()
        self.SetScrollRate(fontsz.x, fontsz.y)
        self.EnableScrolling(True,True)
        # figure out number of pixels to show/scroll based on font and window size
        self.font = wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL)
        self.sz = self.font.GetPixelSize()
        self.fheight = self.sz.GetHeight()
        self.numRows = 17
        self.scrollRows = self.numRows -3
        self.curRow = 0
        self.Layout()
        self.Bind( wx.EVT_PAINT, self.onPaint )

    def onPaint(self, event):
        #PrepareDC is used in wxScrolledWindows when scrolling is activated.
        wx.PaintDC(self) 
        dc = wx.PaintDC(self)
        x1,y1,w,h = dc.GetBoundingBox()
        dc.DrawRectangle(x1, y1, w, h)
        x1,y1 = self.CalcScrolledPosition(x1, y1)
        w,h = self.CalcScrolledPosition(w, h)
        y1 = abs(y1)
        h = abs(h)
        # convert pixels back to lines
        dc.SetFont(self.font) 
        # currow * 32 == address
        # need: current line color
        #       debug line color
        #
        for i in range(0, self.numRows):
            h = self.fheight * i - y1
            dc.SetPen(wx.Pen(wx.NamedColour('white'), 20))
            dc.DrawRectangle(0, h+10, w, self.fheight)
            dc.SetPen(wx.Pen(wx.NamedColour('black'), 20))
            addr = (i + self.curRow) * 8
            code = 0
            for accum in range(0, 4):
                code = code << 8
                code += globals.memory[addr]
            out = '%08X' % addr
            out  += ' %02X' % (code >> 24)
            out += '%02X ' % (code >> 16 & 255)
            out += '%02X' % (code >> 8 & 255)
            out += '%02X' % (code & 255)
            code = 0
            for accum in range(0, 4):
                code = code << 8
                code += globals.memory[addr]
            out  += ' %02X' % (code >> 24)
            out += '%02X ' % (code >> 16 & 255)
            out += '%02X' % (code >> 8 & 255)
            out += '%02X' % (code & 255)
            dc.DrawText(str(out), 5, h)
            
    def OnSize(self, evt):
        if self.getAutoLayout():
            self.Layout()

    def OnInnerSizeChanged(self):
        w,h = self.sizer.GetMinSize()
        self.SetVirtualSize((w,h))
        
    #----------------------------------------------------------------------
    def onRightClick(self, event):
        """"""
        x, y = self.myGrid.CalcUnscrolledPosition(event.GetX(),
                                                  event.GetY())
        row, col = self.myGrid.XYToCell(x, y)
        print row, col
