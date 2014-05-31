#!/usr/bin/env python
import wx
import wx.xrc
import wx.lib.mixins.inspection
import logging
import globals

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
    
    def buildRegValString(self, i):
        out = "R"+str("%02d"%i)+":"+str("%08x" % globals.regs[i])
        out += str(" %08x" % globals.regs[i])
        if (i == globals.SP):
            out += " (sp)"
        if (i == globals.LINK):
            out += " (lr)"
        if (i == globals.PC):
            out += " (pc)"
        if (i == globals.CPSR):
            out += " (cpsr)"
            if (globals.regs[i] & globals.NEGATIVEBIT == globals.NEGATIVEBIT):
                cpsr = " N"
            else:
                cpsr = " n"
            if (globals.regs[i] & globals.ZEROBIT == globals.ZEROBIT):
                cpsr += "Z"
            else:
                cpsr += "z"
            if (globals.regs[i] & globals.CARRYBIT == globals.CARRYBIT):
                cpsr += "C"
            else:
                cpsr += "c"
            if (globals.regs[i] & globals.OVERBIT == globals.OVERBIT):
                cpsr += "V"
            else:
                cpsr += "v"
            if (globals.regs[i] & globals.QBIT == globals.QBIT):
                cpsr += "Q"
            else:
                cpsr += "q"
            if (globals.regs[i] & globals.INTIRQBIT == globals.INTIRQBIT):
                cpsr += "I"
            else:
                cpsr += "i"
            if (globals.regs[i] & globals.INTFIQBIT == globals.INTFIQBIT):
                cpsr += "F"
            else:
                cpsr += "f"
            if (globals.regs[i] & globals.THUMBBIT == globals.THUMBBIT):
                cpsr += "T "
            else:
                cpsr += "t "
            if (globals.regs[i] & globals.OPMODEBIT == int("00000017",16)):
                cpsr += " abort"
            if (globals.regs[i] & globals.OPMODEBIT == int("00000011",16)):
                cpsr += " fintreq"
            if (globals.regs[i] & globals.OPMODEBIT == int("00000012",16)):
                cpsr += " intreq"
            if (globals.regs[i] & globals.OPMODEBIT == int("00000013",16)):
                cpsr += " sup"
            if (globals.regs[i] & globals.OPMODEBIT == int("0000001f",16)):
                cpsr += " system"
            if (globals.regs[i] & globals.OPMODEBIT == int("0000001b",16)):
                cpsr += " undef"
            if (globals.regs[i] & globals.OPMODEBIT == int("00000010",16)):
                cpsr += " user"
        if (i == 18):
            out += "(spsr):"
        
        if (i == 17):
            out += cpsr
        return out
                
    def onPaint(self, event):
        dc = wx.PaintDC(self)
        x1,y1,w,h = dc.GetBoundingBox()
        dc.DrawRectangle(x1, y1, w, h)
        y1 = abs(y1)
        h = abs(h)
        # convert pixels back to lines
        self.curRow = abs(y1) / self.fheight;
        dc.SetFont(self.font)
        for i in range(self.curRow, 16):  # 16 registers
            self.h = self.fheight * i - y1
            dc.SetPen(wx.Pen(wx.NamedColour('white'), 20))
            dc.DrawRectangle(0, self.h+10, w, self.fheight)
            dc.SetPen(wx.Pen(wx.NamedColour('black'), 20))
            out = self.buildRegValString(i)
            dc.DrawText(out, 5, self.h)
            
    def OnInnerSizeChanged(self):
        w,h = self.sizer.GetMinSize()
        self.SetVirtualSize((w,h))
