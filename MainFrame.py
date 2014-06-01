# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Feb 26 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.lib.mixins.inspection
import logging
import shlex

import globals
import os
import dumpelf
import ARMCPU
import arm7instrdecode

from CodeWindow import CodeWindow
from CmdWindow import CmdWindow
from IOWindow import IOWindow
from MemoryWindow import MemoryWindow
from Registers import Registers

prompt = u"RDY>"

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):
    def __init__( self, parent ):
        self.parent = parent
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        self.m_menubar = wx.MenuBar( 0 )
        self.m_filemenu = wx.Menu()
        self.m_mi_open = wx.MenuItem( self.m_filemenu, wx.ID_ANY, u"Open", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_filemenu.AppendItem( self.m_mi_open )

        self.m_filemenu.AppendSeparator()

        self.m_mi_exit = wx.MenuItem( self.m_filemenu, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_filemenu.AppendItem( self.m_mi_exit )

        self.m_menubar.Append( self.m_filemenu, u"File" )

        self.m_helpmenu = wx.Menu()
        self.m_mi_about = wx.MenuItem( self.m_helpmenu, wx.ID_ANY, u"About", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_helpmenu.AppendItem( self.m_mi_about )
        self.m_menubar.Append( self.m_helpmenu, u"Help" )

        self.SetMenuBar( self.m_menubar )

        bSizerMain = wx.BoxSizer( wx.VERTICAL )

        self.m_split_other_cmd = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
        self.m_split_other_cmd.SetSashGravity( 0.5 )
        self.m_split_other_cmd.Bind( wx.EVT_IDLE, self.m_split_other_cmdOnIdle )

        self.m_p_other_cmd = wx.Panel( self.m_split_other_cmd, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizerOther1 = wx.BoxSizer( wx.VERTICAL )

        self.m_reg_other = wx.SplitterWindow( self.m_p_other_cmd, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
        self.m_reg_other.SetSashGravity( 0.5 )
        self.m_reg_other.Bind( wx.EVT_IDLE, self.m_reg_otherOnIdle )

        self.m_reg_other_p1 = wx.Panel( self.m_reg_other, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizerRegOther = wx.BoxSizer( wx.VERTICAL )

        self.m_split_reg_other = wx.SplitterWindow( self.m_reg_other_p1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
        self.m_split_reg_other.SetSashGravity( 0.5 )
        self.m_split_reg_other.Bind( wx.EVT_IDLE, self.m_split_reg_otherOnIdle )

        self.m_regs = Registers( self.m_split_reg_other, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.CLIP_CHILDREN|wx.SUNKEN_BORDER|wx.TAB_TRAVERSAL )
        bSizerRegs = wx.BoxSizer( wx.VERTICAL )

        bSizerRegs.SetMinSize( wx.Size( 250,300 ) )

        self.m_regs.SetSizer( bSizerRegs )
        self.m_regs.Layout()
        bSizerRegs.Fit( self.m_regs )
        self.m_io = IOWindow( self.m_split_reg_other, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SUNKEN_BORDER|wx.TAB_TRAVERSAL )
        bSizerIO = wx.BoxSizer( wx.VERTICAL )


        self.m_io.SetSizer( bSizerIO )
        self.m_io.Layout()
        bSizerIO.Fit( self.m_io )
        self.m_split_reg_other.SplitHorizontally( self.m_regs, self.m_io, 0 )
        bSizerRegOther.Add( self.m_split_reg_other, 1, wx.EXPAND, 5 )


        self.m_reg_other_p1.SetSizer( bSizerRegOther )
        self.m_reg_other_p1.Layout()
        bSizerRegOther.Fit( self.m_reg_other_p1 )
        self.m_code_other = wx.Panel( self.m_reg_other, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizerCodeOther = wx.BoxSizer( wx.VERTICAL )

        self.m_split_code_other = wx.SplitterWindow( self.m_code_other, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
        self.m_split_code_other.SetSashGravity( 0.5 )
        self.m_split_code_other.Bind( wx.EVT_IDLE, self.m_split_code_otherOnIdle )

        self.m_split_code_other.SetMinSize( wx.Size( 100,-1 ) )

        self.m_scrolledcode = CodeWindow( self.m_split_code_other, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.STATIC_BORDER|wx.VSCROLL )
        self.m_scrolledcode.SetScrollRate( 5, 5 )
        self.m_mem1_mem2 = wx.Panel( self.m_split_code_other, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizerMem1Mem2 = wx.BoxSizer( wx.VERTICAL )

        self.m_split_mem_mem = wx.SplitterWindow( self.m_mem1_mem2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
        self.m_split_mem_mem.SetSashGravity( 0.5 )
        self.m_split_mem_mem.Bind( wx.EVT_IDLE, self.m_split_mem_memOnIdle )

        self.m_scrolledmem1 = MemoryWindow( self.m_split_mem_mem, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SUNKEN_BORDER|wx.VSCROLL )
        self.m_scrolledmem1.SetScrollRate( 5, 5 )
        self.m_scrolledmem2 = MemoryWindow( self.m_split_mem_mem, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SUNKEN_BORDER|wx.VSCROLL )
        self.m_scrolledmem2.SetScrollRate( 5, 5 )
        self.m_split_mem_mem.SplitHorizontally( self.m_scrolledmem1, self.m_scrolledmem2, 0 )
        bSizerMem1Mem2.Add( self.m_split_mem_mem, 1, wx.EXPAND, 5 )


        self.m_mem1_mem2.SetSizer( bSizerMem1Mem2 )
        self.m_mem1_mem2.Layout()
        bSizerMem1Mem2.Fit( self.m_mem1_mem2 )
        self.m_split_code_other.SplitVertically( self.m_scrolledcode, self.m_mem1_mem2, 350 )
        bSizerCodeOther.Add( self.m_split_code_other, 1, wx.EXPAND, 5 )


        self.m_code_other.SetSizer( bSizerCodeOther )
        self.m_code_other.Layout()
        bSizerCodeOther.Fit( self.m_code_other )
        self.m_reg_other.SplitVertically( self.m_reg_other_p1, self.m_code_other, 200 )
        bSizerOther1.Add( self.m_reg_other, 1, wx.EXPAND, 5 )


        self.m_p_other_cmd.SetSizer( bSizerOther1 )
        self.m_p_other_cmd.Layout()
        bSizerOther1.Fit( self.m_p_other_cmd )
        self.m_scrolled_cmd = CmdWindow( self.m_split_other_cmd, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SUNKEN_BORDER|wx.VSCROLL|wx.WANTS_CHARS )
        #bSizerCmd = wx.BoxSizer( wx.VERTICAL )
        #bSizerCmd.SetMinSize( wx.Size( -1,150 ) )
        #self.m_scrolled_cmd.SetSizer( bSizerCmd )
        #self.m_scrolled_cmd.Layout()
        #bSizerCmd.Fit( self.m_scrolled_cmd )
        self.m_split_other_cmd.SplitHorizontally( self.m_p_other_cmd, self.m_scrolled_cmd, 500 )
        bSizerMain.Add( self.m_split_other_cmd, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizerMain )
        self.Layout()

        self.Centre( wx.BOTH )

        #----------------------------------------------------------------------------
        self.Bind(wx.EVT_MENU, self.menuOpen, self.m_mi_open)
        #self.Bind(wx.EVT_MENU, self.menuClose, id=ID_FILE_CLOSE)
        self.Bind(wx.EVT_MENU, self.menuExit, self.m_mi_exit)
        self.Bind(wx.EVT_MENU, self.menuAbout, self.m_mi_about)
        self.m_scrolled_cmd.Bind(wx.EVT_KEY_DOWN, self.onKeyDown )        ## capture control events not normally seen, eg ctrl-tab.
                                                            ## track of previous value for undo
        #----------------------------------------------------------------------------
        timer = wx.Timer(self, -1)
        self.Bind(wx.EVT_TIMER, self.onTick, timer)
        timer.Start(milliseconds=1000, oneShot=False)

    def __del__( self ):
        pass

    def m_split_other_cmdOnIdle( self, event ):
        self.m_split_other_cmd.SetSashPosition( 475 )
        self.m_split_other_cmd.Unbind( wx.EVT_IDLE )

    def m_reg_otherOnIdle( self, event ):
        self.m_reg_other.SetSashPosition( 200 )
        self.m_reg_other.Unbind( wx.EVT_IDLE )

    def m_split_reg_otherOnIdle( self, event ):
        self.m_split_reg_other.SetSashPosition( 0 )
        self.m_split_reg_other.Unbind( wx.EVT_IDLE )

    def m_split_code_otherOnIdle( self, event ):
        self.m_split_code_other.SetSashPosition( 350 )
        self.m_split_code_other.Unbind( wx.EVT_IDLE )

    def m_split_mem_memOnIdle( self, event ):
        self.m_split_mem_mem.SetSashPosition( 0 )
        self.m_split_mem_mem.Unbind( wx.EVT_IDLE )

    def updateKids(self):
        self.m_scrolledcode.Refresh()
        self.m_scrolledmem1.Refresh()
        self.m_scrolledmem2.Refresh()
        self.m_regs.Refresh()
        self.m_io.Refresh()
        self.m_scrolled_cmd.AppendText(prompt)

    def OnChange(self, event):
        sizer = self.frame.GetSizer()
        sizer.Show( self.controlPanel, show=self.showControls.GetValue(), recursive=true)
        size=sizer.GetMinSize()
        self.frame.SetMinSize(size)
        self.frame.Fit()

    def onTick(self):
        print "onTick"
        self.m_code.update()


    #----------------------------------------------------------------------------
    def menuAbout(self, evt):
        dlg = wx.MessageDialog(self,
        "a simple application using wxFrame, wxMenu\n"
        "a statusbar, and an about message dialog.",
        "About", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def menuOpen(self, evt):
        """open a file"""
        print "Open File"
        self.dirname = ''
        fileType = "ELF (.elf)|*.elf"
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", fileType, wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
        self.full_path =  os.path.join(self.dirname, self.filename)
        print "Open file:" + self.full_path  # test
        efile = dumpelf.ELFFile(self.full_path, globals.memory)
        dlg.Destroy()
        self.updateKids()

    def menuExit(self, evt):
        self.Close(True)

    #----------------------------------------------------------------------------
    def onKeyDown(self, evt):
        self.key = evt.GetKeyCode()
        self.m_scrolled_cmd.AppendText(chr(self.key))
        if self.key == wx.WXK_RETURN:
        	self.onReturn(evt)
        #print str(self.key)
        if self.key == 8:  # where's backspace ???
            print "backspace"
            self.m_scrolled_cmd.Remove(self.m_scrolled_cmd.GetLastPosition()-1, self.m_scrolled_cmd.GetLastPosition()+1)
            #noLines = self.m_scrolled_cmd.GetNumberOfLines()
            #lineText = self.m_scrolled_cmd.GetLineText(noLines - 2)  # little magic, lines are 0 based and GetNumber returns the line you're on = +2
            #if len(lineText) > 0:
            #    lineText = lineText[:-2]
            #    self.m_scrolled_cmd.SetLineText(noLines - 2)
        evt.Skip()

    def onReturn(self, evt):
        """
            s -> step
            t -> trace
            b 0xv -> set breakpoint
            c -> ?
            d 0xv -> dump memory
            g -> go
            k -> skip?
            r# = 0xv -> set register
            """
        noLines = self.m_scrolled_cmd.GetNumberOfLines()
        lineText = self.m_scrolled_cmd.GetLineText(noLines - 2)  # little magic, lines are 0 based and GetNumber returns the line you're on = +2
        # strip prompt
        idx = lineText.find(prompt)
        if idx > -1:
            lineText = lineText[idx+len(prompt):]
        lineText = lineText.lower()
        print "return:" + str(noLines) + " '" + lineText + "'"
        if len(lineText) > 0:
            firstChar = lineText[0][:1]
            if (firstChar == 's' ):
                globals.regs[globals.PC] = arm7instrdecode.execInstructionAtAddress(self, globals.regs[globals.PC], globals.memory)
            if (firstChar == 'r' ):
                # change registers
                # r# #
                items = shlex.split(lineText)
                print items
                reg = int(items[0][1:])
                val = long(items[1],16)
                print "r:" + str(reg) + " v:" + str(val)
                globals.regs[reg] = val
                print "r:" + str(reg) + " v:" + str(val)+" PC:"+str(globals.regs[globals.PC])
        self.updateKids()
