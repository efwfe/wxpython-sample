#!/usr/bin/env python
"""
wxspreadsheet.py: extension of wxPython's CSheet (grid) 
with basic spreadsheet functionality
"""

import wx.lib.sheet
import wx.grid
import csv

class ContextMenu(wx.Menu):
    '''Basic right-click popup menu for CSheet controls.  Currently
    implements copy-paste selected cell(s), insert row / column, delete
    row / column.'''
    def __init__(self, parent):
        wx.Menu.__init__(self)
        self.parent = parent       
        insertrow = wx.MenuItem(self, wx.NewId(), '添加行')
        self.Append(insertrow)
        self.Bind(wx.EVT_MENU, self.OnInsertRow, id=insertrow.GetId())
        deleterow = wx.MenuItem(self, wx.NewId(), '删除行')
        self.Append(deleterow)
        self.Bind(wx.EVT_MENU, self.OnDeleteRow, id=deleterow.GetId())
        insertcol = wx.MenuItem(self, wx.NewId(), '添加列')
        self.Append(insertcol)
        self.Bind(wx.EVT_MENU, self.OnInsertCol, id=insertcol.GetId())
        deletecol = wx.MenuItem(self, wx.NewId(), '删除列')
        self.Append(deletecol)
        self.Bind(wx.EVT_MENU, self.OnDeleteCol, id=deletecol.GetId())
        self.AppendSeparator()
        copy = wx.MenuItem(self, wx.NewId(), 'Copy')
        self.Append(copy)
        self.Bind(wx.EVT_MENU, self.OnCopy, id=copy.GetId())
        paste = wx.MenuItem(self, wx.NewId(), 'Paste')
        self.Append(paste)
        self.Bind(wx.EVT_MENU, self.OnPaste, id=paste.GetId())
        clear = wx.MenuItem(self, wx.NewId(), '清空')
        self.Append(clear)
        self.Bind(wx.EVT_MENU, self.OnClear, id=clear.GetId())

    def on_action(self):
        data = self.parent.SaveData()
        window = self.parent.parent.parent.parent
        item = window.mid_item
        if item:
            dat = window.tree.getItemData(item)
            dat['data'] = data
            window.tree.setData2Item(item, dat)

    def fitWindow(self):
        window = self.parent.parent.parent.parent
        window.vbox2.Fit(window.table)

    def OnInsertRow(self, event):
        '''Basic "Insert Row(s) Here" function'''
        self.parent.SelectRow(self._getRow())
        self.parent.InsertRows(self._getRow(), self._getSelectionRowSize())
        self.fitWindow()
        self.on_action()

    def OnDeleteRow(self, event):
        '''Basic "Delete Row(s)" function'''
        self.parent.SelectRow(self._getRow())
        self.parent.DeleteRows(self._getRow(), self._getSelectionRowSize())
        self.fitWindow()
        self.on_action()
        
    def OnInsertCol(self, event):
        '''Basic "Insert Column(s) Here" function'''
        self.parent.SelectCol(self._getCol())
        self.parent.InsertCols(self._getCol(), self._getSelectionColSize())
        self.fitWindow()
        self.on_action()
        
    def OnDeleteCol(self, event):
        '''Basic "Delete Column(s)" function'''
        self.parent.SelectCol(self._getCol())
        self.parent.DeleteCols(self._getCol(), self._getSelectionColSize())
        self.fitWindow()
        self.on_action()

    def OnClear(self, event):
        '''Erases the contents of the currently selected cell(s).'''
        self.parent.ClearGrid()
        self.fitWindow()
        self.on_action()

    def OnCopy(self, event):
        '''Copies the contents of the currently selected cell(s)
        to the clipboard.'''
        self.parent.Copy()

    def OnPaste(self, event):
        '''Pastes the clipboard's contents to the currently
        selected cell(s).'''
        self.parent.Paste()
        
    def _getRow(self):
        '''Returns the first (top) row in the selected row(s) if any,
        otherwise returns the row of the current cursor position.'''
        selected_row = self.parent.GetSelectedRows()
        if  selected_row != []:
            return selected_row[0]
        else:
            return self.parent.GetGridCursorRow()
            
    def _getCol(self):
        '''Returns the first (left) row in the selected column(s) if any,
        otherwise returns the column of the current cursor position.'''
        selected_col = self.parent.GetSelectedCols()
        if  selected_col != []:
            return selected_col[0]
        else:
            return self.parent.GetGridCursorCol()  
            
    def _getSelectionRowSize(self):
        '''Returns the number of selected rows, number of rows in the
        current selection, or 1 in order of preference.'''
        numrows = 1
        if self.parent.GetSelectionBlockTopLeft() != []:
            numrows = self.parent.GetSelectionBlockBottomRight()[0][0] -\
                self.parent.GetSelectionBlockTopLeft()[0][0]+1
        else:
            numrows = len(self.parent.GetSelectedRows())
        return numrows
        
    def _getSelectionColSize(self):
        '''Returns the number of selected columns, number of columns in the
        current selection, or 1 in order of preference.'''    
        numcols = 1 
        if self.parent.GetSelectionBlockTopLeft() != []:
            numcols = self.parent.GetSelectionBlockBottomRight()[0][1] -\
                self.parent.GetSelectionBlockTopLeft()[0][1]+1
        else:
            numcols = len(self.parent.GetSelectedCols())
        return numcols

class SpreadsheetTextCellEditor(wx.TextCtrl):
    """ Custom text control for cell editing """
    def __init__(self, parent, id, grid):
        wx.TextCtrl.__init__(self, parent, id, "", 
            style=wx.NO_BORDER | wx.TE_PROCESS_ENTER)
        self._grid = grid                           # Save grid reference
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def OnChar(self, evt):                          # Hook OnChar for custom behavior
        """Customizes char events """
        key = evt.GetKeyCode()
        if key == wx.WXK_DOWN or key == wx.WXK_RETURN:
            # print("update the cell")
            self._grid.DisableCellEditControl()     # Commit the edit
            self._grid.MoveCursorDown(False)        # Change the current cell
        elif key == wx.WXK_UP:
            self._grid.DisableCellEditControl()     # Commit the edit
            self._grid.MoveCursorUp(False)          # Change the current cell
        elif key == wx.WXK_LEFT:
            self._grid.DisableCellEditControl()     # Commit the edit
            self._grid.MoveCursorLeft(False)        # Change the current cell
        elif key == wx.WXK_RIGHT:
            self._grid.DisableCellEditControl()     # Commit the edit
            self._grid.MoveCursorRight(False)       # Change the current cell

        evt.Skip()                                  # Continue event

class SpreadsheetCellEditor(wx.grid.GridCellEditor):
    """ Custom cell editor """
    def __init__(self, grid):
        super(SpreadsheetCellEditor, self).__init__(grid)
        
    def Create(self, parent, id, evtHandler):
        """ Create the actual edit control.  Must derive from wxControl.
            Must Override
        """
        self._tc = SpreadsheetTextCellEditor(parent, id, self._grid)
        self._tc.SetInsertionPoint(0)
        self.SetControl(self._tc)
        if evtHandler:
            self._tc.PushEventHandler(evtHandler)        
        
class Spreadsheet(wx.grid.Grid):
    '''Child class of CSheet (child of wxGrid) that implements a basic
    right-click popup menu.'''
    def __init__(self, parent):
        super(Spreadsheet, self).__init__(parent)
        self.CreateGrid(1, 1)
        self.setReadOnly()
        self.READABLE = False
        self.menu = ContextMenu(self)
        self.parent = parent

        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.OnRightClick)
    #     self.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.onChangeCell)
    
    # def onChangeCell(self, event):
    #     row,col = event.GetRow(), event.GetCol()
    #     data = self.GetCellValue(row, col)
    #     print("{},{}changed data:{}".format(row, col,data))
    #     print(self.SaveData())
    def OnRightClick(self, event):
        '''Defines the right click popup menu for the spreadsheet'''
        
        '''Move the cursor to the cell clicked'''
        if not self.READABLE:
            return
        row,col = event.GetRow(), event.GetCol()
        self.SetGridCursor(row,col)
        self.PopupMenu(self.menu, event.GetPosition())

    def ResetNumberRowsCols(self):
        curr = self.GetNumberRows()
        self.DeleteRows(0, curr, True)
        curr = self.GetNumberCols()
        self.DeleteCols(0, curr, True)


    def setReadOnly(self):
        self.READABLE = False
        self.EnableEditing(False)

    def setWriteAble(self):
        self.READABLE = True
        self.EnableEditing(True)

    def ShowData(self, data):
        '''Display 2D data to grid'''
        self.ClearGrid()

        try:
            if data:
                self.ResetNumberRowsCols()

            rownum = 0
            max_cols = 0
            for row in data:
                self.AppendRows(1)
                numcols = len(row)
                if self.GetNumberCols() < numcols:
                    self.AppendCols(numcols - self.GetNumberCols())
                colnum = 0
                for cell in row:
                    self.SetCellValue(rownum, colnum, str(cell))
                    colnum = colnum + 1
                rownum = rownum + 1
        except Exception as err:
            print("Skipping line {0}: {1}".format(data, err))
            return []
        self.AutoSize()

    def SaveData(self):
        '''save grid data to memory'''
        result = []
        for rownum in range(self.GetNumberRows()):
            rowdata = []
            for colnum in range(self.GetNumberCols()):
                rowdata.append(self.GetCellValue(rownum, colnum))
            
            result.append(rowdata)
        return result
        
    