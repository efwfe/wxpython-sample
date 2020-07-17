import wx
import wx.grid as gridlib
from wxspreadsheet import Spreadsheet
from files_tree import FilesTree
from files import FileHandler

class XPanel(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent

class WinUI(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Tree", size=(800, 600))
        self.Center()
        # 设置菜单栏
        self.SetMenuBar(self.init_Menu())

        swindow = wx.SplitterWindow(parent=self, id=-1)
        swindow.parent = self
        left = XPanel(parent=swindow)
        right = XPanel(parent=swindow)
        # 设置左右布局的分割窗口left和right
        swindow.SplitVertically(left, right, 200)
        # 设置最小窗格大小，左右布局指左边窗口大小
        swindow.SetMinimumPaneSize(200)
        self.file_helper = FileHandler()
        self.tree = self.CreateTreeCtrl(left)
        self.table = Spreadsheet(right)
       
        self.Bind(wx.EVT_TREE_SEL_CHANGING, self.on_click, self.tree)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.show_img, self.tree)
        self.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.change_cell, self.table)
        self.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.change_cell, self.table)

        # 为left面板设置一个布局管理器
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        left.SetSizer(vbox1)

        # 为right面板设置一个布局管理器
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        right.SetSizer((vbox2))

        vbox1.Add(self.tree, 1, flag=wx.EXPAND | wx.ALL, border=5)
        vbox2.Add(self.table, 1, flag=wx.EXPAND | wx.ALL)

        vbox2.Fit(self.table)
        vbox1.Fit(self.tree)

        # 中间item 数据提交更新中转
        self.mid_item = None

    def change_cell(self, event):
        if self.mid_item:
            data = self.table.SaveData()
            item_data = self.tree.getItemData(self.mid_item)
            item_data["data"] = data
            self.tree.setData2Item(self.mid_item, item_data)
            self.mid_item = None

    def show_img(self, event):
        """ 双击打开图片
        """
        item = event.GetItem()
        data = self.tree.getItemData(item)
        if data:
            file_path = data['file_path']
            print(self.tree.GetItemText(item), "double clicked {}".format(file_path))

    def init_Menu(self):
        menuBar = wx.MenuBar()

        s1 = wx.Menu()
        s2 = wx.Menu()

        fileItem = s1.Append(1, '打开文件', "")
        fileDirItem = s1.Append(2, '打开文件夹', "")
        exitItem = s1.Append(-1, '退出', "")

        menuBar.Append(s1, "&文件")
        exportItem = s2.Append(-1, "导出到...")
        menuBar.Append(s2, "&导出")
        

        self.Bind(wx.EVT_MENU, self.OnCloseMe, exitItem)
        self.Bind(wx.EVT_MENU, self.onOpenFile, fileItem)
        self.Bind(wx.EVT_MENU, self.onOpenDirectory, fileDirItem)
        self.Bind(wx.EVT_MENU, self.exportData, exportItem)
        
        return menuBar

    def exportData(self, event):
        dialog = wx.DirDialog(
            self,
            "Choose a directory:",
            style=wx.DD_DEFAULT_STYLE
        )

        if dialog.ShowModal() == wx.ID_CANCEL:
            return

        path = dialog.GetPath()
        all_items = self.tree.getAllCodes()
        print(all_items)
        # with open("数据导出.csv", 'w') as f:
    
    def on_click(self, event):
        item = event.GetItem()
        # 更新数据 展示
        data = self.tree.getItemData(item)
        if not data:
            data = {'data':[['']]}
            self.table.setReadOnly()
            self.mid_item = None
        else:
            self.table.setWriteAble()
            self.mid_item = item
        table_data = data['data']
        self.table.ShowData(table_data)


    def CreateTreeCtrl(self, parent):
        tree = FilesTree(parent)
        # 返回树对象
        return tree

    def onOpenFile(self, event):
        wildcard = "image files (*.jpg)|*.jpg|*.jpeg|*.png|*.bmp|"
        dialog = wx.FileDialog(self, "Open Text Files", wildcard=wildcard,
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if dialog.ShowModal() == wx.ID_CANCEL:
            return

        path = dialog.GetPath()
        file_name, data = self.file_helper.extract_file(path)
        item = self.tree.addFile2Dir(file_name)
        self.tree.setData2Item(item, data)
        # 更新表单数据
        table_data = data["data"]
        self.table.ShowData(table_data)
        self.tree.ExpandAll()
        self.mid_item = item
        self.tree.SelectItem(item)

    def onOpenDirectory(self, event):
        dialog = wx.DirDialog(
            self,
            "Choose a directory:",
            style=wx.DD_DEFAULT_STYLE
        )

        if dialog.ShowModal() == wx.ID_CANCEL:
            return

        path = dialog.GetPath()
        dir_name, datas = self.file_helper.extract_files(path)
        dir_elem = self.tree.addDir2Root(dir_name)
        for f, data in datas:
            elem = self.tree.addFile2Dir(item=f, parent=dir_elem)
            self.tree.setData2Item(elem, data)
        self.tree.ExpandAll()

    def OnCloseMe(self, event):
        self.Close(True)

    def OnCloseWindow(self, event):
        self.Destroy()


class App(wx.App):
    def OnInit(self):
        # 创建窗口对象
        frame = WinUI()
        frame.Show()
        return True

    def OnExit(self):
        print("应用程序退出")
        return 0


if __name__ == '__main__':
    app = App()
    app.MainLoop()
