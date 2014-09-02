#!/usr/bin/env python
import wx
import wx.xrc

import wx.lib.mixins.inspection

import logging
import globals
import arm7instrdecode
import ARMCPU

###########################################################################
## Handle the CodeWindow window
###########################################################################
class CodeWindow(wx.ScrolledWindow):

    def __init__(self, parent, id, pos, size, style):
        self.parent = parent
        wx.ScrolledWindow.__init__(self, parent, -1, style=style|wx.TAB_TRAVERSAL|wx.VSCROLL|wx.ALWAYS_SHOW_SB, name=u"CodeWindow")
        # figure out number of pixels to show/scroll based on font and window size
        self.font = wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL)
        self.sz = self.font.GetPixelSize()
        self.fheight = self.sz.GetHeight() - 2

        self.verHeightMaxLines = 1024    # want the scrollable aread to be this
        self.verHeightScrollLines = 32 # want to scroll this many lines
        self.verHeightMaxPixels =  (self.fheight * self.verHeightMaxLines)  # how many pixels
        self.verHeightScrollPixels =  (self.fheight * self.verHeightScrollLines)  # how many pixels
        self.SetVirtualSize((300, self.verHeightScrollPixels))
        self.pixelScrollUnits = (self.fheight * self.verHeightScrollLines)
        self.SetScrollbars(0, self.pixelScrollUnits, 0, self.verHeightMaxPixels)
        #print "vMaxLPix:" + str(self.verHeightMaxPixels) + " vScrollPix:" + str(self.verHeightScrollPixels) + " PixScrollUnits:" + str(self.pixelScrollUnits)
        self.SetScrollPos(wx.VERTICAL, 0, True)
        self.Layout()
        self.numRows = 0 # number of rows that can fit on screen
        self.curRows = 0 # the current row that is scrolled to, e.g. row 0 on screen can be x
        self.Bind( wx.EVT_PAINT, self.onPaint )
        self.Bind( wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind( wx.EVT_SIZE, self.OnSize)

    #----------------------------------------------------------------------
    #def OnEraseBackground(self, event):  # empty to prevent flicker
    #    pass

    #----------------------------------------------------------------------
    def OnEraseBackground(self, evt):
        dc = evt.GetDC()
        bckColor = wx.NamedColour('white')
        dc.SetBrush(wx.Brush(bckColor));
        dc.SetPen(wx.Pen(bckColor, 1));
        w,h = self.GetClientSize()
        # We need to shift the client rectangle to take into account
        # scrolling, converting device to logical coordinates
        #self.CalcUnscrolledPosition(wrect.x, wrect.y, wrect.w, wrect.h)
        print "paintBackground w:" + str(w) + " h:" + str(h)
        dc.DrawRectangle(x=0, y=0, width=w, height=h);

    #----------------------------------------------------------------------
    def onPaint(self, event):
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        print "onPaint --------------------------------------------------------"
        self.DoDrawing(dc)

    #----------------------------------------------------------------------
    def DoDrawing(self, dc, printing=False):
        dc.BeginDrawing()
        # Get viewport size
        x1, y1, w, h = self.GetClientRect()
        #print "bbox  x:" + str(x1) + " y:" + str(y1) + " w:" + str(w) + " h:" + str(h)
        # Get where the scrolling is, units are in number of pixels per scroll "page"
        x1,y1 = self.GetViewStart()
        #print "VS    x:" + str(x1) + " y:" + str(y1) + " w:" + str(w) + " h:" + str(h)
        # convert pages back to starting of viewport
        cspx,cspy = self.CalcUnscrolledPosition(x1,y1)
        cspy = abs(cspy) - y1 # fixes subtle bug in which the lines slowly disappear when scrolling
        cspw,csph = self.CalcUnscrolledPosition(w,h)
        #print "VSCSP x:" + str(x1) + " y:" + str(cspy) + " w:" + str(w) + " h:" + str(h)
        # debug
        dc.SetPen(wx.Pen(wx.NamedColour('red'), 2))
        dc.DrawRectangle(x1, cspy, w, h)
        # enable the selected font
        dc.SetFont(self.font)
        # figure out how many lines of the selected font will fit in viewport
        self.numRows = int(h / self.fheight)
        self.curRow = cspy / self.fheight
        #print "fheight:" + str(self.fheight) + " n:" + str(self.numRows) + " cRow:" + str(self.curRow) + " st addr:" + str(self.curRow * 4)
        # need: current line color
        #       debug line color
        #
        for i in range(0, self.numRows):
            addr = (i + self.curRow) * 4
            instrStr = arm7instrdecode.getInstructionFromAddress(self, addr, globals.memory)
            h = self.fheight * i + cspy
            dc.SetPen(wx.Pen(wx.NamedColour('white'), 20))
            print 'h:{0:d} fheight:{1:d} i:{2:d} cspy:{3:d}'.format(h, self.fheight, i, cspy)
            #print "c:" + str(addr) + " PC:" + str(globals.regs[globals.PC]) + " h:" + str(h)
            if (addr == globals.regs[globals.PC]):
                dc.SetPen(wx.Pen(wx.NamedColour('green'), 20))
            dc.DrawRectangle(0, h + self.fheight, w, self.fheight)
            dc.SetPen(wx.Pen(wx.NamedColour('black'), 20))
            dc.DrawText(str(instrStr), 2, h + 2)
        dc.EndDrawing()

    #----------------------------------------------------------------------
    def OnSize(self, evt):
        w,h = evt.GetSize()
        #print "OnSize evt:" + str(w) + " " + str(h)
