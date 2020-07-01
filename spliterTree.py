import wx
import wx.grid as gridlib


class TablePanel(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)

        grid = gridlib.Grid(self)
        grid.CreateGrid(2,2)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid,0, wx.EXPAND)
        self.SetSizer(sizer)


# 自定义窗口类MyFrame
class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Tree", size=(500, 400))
        self.Center()
        # 设置菜单栏
        menuBar = wx.MenuBar()
        s1 = wx.Menu()
        fileItem = s1.Append(1, '打开文件', "")
        fileDirItem = s1.Append(2, '打开文件夹', "")
        exitItem = s1.Append(-1, '退出', "")
        menuBar.Append(s1, "&文件")
        self.Bind(wx.EVT_MENU, self.OnCloseMe, exitItem)
        self.Bind(wx.EVT_MENU, self.onOpenFile, fileItem)
        self.Bind(wx.EVT_MENU, self.onOpenDirectory, fileDirItem)

        s2 = wx.Menu()
        s2.Append(1, "导出excel")
        menuBar.Append(s2, "&导出")
        self.SetMenuBar(menuBar)

        swindow = wx.SplitterWindow(parent=self, id=-1)
        left = wx.Panel(parent=swindow)
        right = wx.Panel(parent=swindow)
        # 设置左右布局的分割窗口left和right
        swindow.SplitVertically(left, right, 200)
        # 设置最小窗格大小，左右布局指左边窗口大小
        swindow.SetMinimumPaneSize(80)
        # 创建一棵树

        self.tree = self.CreateTreeCtrl(left)
        self.Bind(wx.EVT_TREE_SEL_CHANGING, self.on_click, self.tree)
        # 为left面板设置一个布局管理器
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        left.SetSizer(vbox1)
        vbox1.Add(self.tree, 1, flag=wx.EXPAND | wx.ALL, border=5)
        # 为right面板设置一个布局管理器
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        right.SetSizer((vbox2))
        self.st = TablePanel(right)
        vbox2.Fit(self.st)
        vbox2.Add(self.st, 1, flag=wx.EXPAND | wx.ALL, border=5)

    def on_click(self, event):
        item = event.GetItem()
        self.st.SetLabel(self.tree.GetItemText(item))

    def CreateTreeCtrl(self, parent):
        tree = wx.TreeCtrl(parent)
        # 通过wx.ImageList()创建一个图像列表imglist并保存在树中
        imglist = wx.ImageList(16, 16, True, 2)
        imglist.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, size=wx.Size(16, 16)))
        imglist.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, size=(16, 16)))
        tree.AssignImageList(imglist)
        # 创建根节点和5个子节点并展开
        root = tree.AddRoot('目录', image=0)
        item1 = tree.AppendItem(root, 'Item1', 0)
        item2 = tree.AppendItem(root, 'Item2', 0)
        item3 = tree.AppendItem(root, 'Item3', 0)
        item4 = tree.AppendItem(root, 'Item4', 0)
        item5 = tree.AppendItem(root, 'Item5', 0)
        tree.Expand(root)
        tree.SelectItem(root)

        # 给item1节点添加5个子节点并展开
        tree.AppendItem(item1, 'file 1', 1)
        tree.AppendItem(item1, 'file 2', 1)
        tree.AppendItem(item1, 'file 3', 1)
        tree.AppendItem(item1, 'file 4', 1)
        tree.AppendItem(item1, 'file 5', 1)
        # tree.Expand(item1)

        # 给item2节点添加5个子节点并展开
        tree.AppendItem(item2, 'file 1', 1)
        tree.AppendItem(item2, 'file 2', 1)
        tree.AppendItem(item2, 'file 3', 1)
        tree.AppendItem(item2, 'file 4', 1)
        tree.AppendItem(item2, 'file 5', 1)
        # tree.Expand(item2)

        # 返回树对象
        return tree

    def onOpenFile(self, event):
        wildcard = "image files (*.jpg)|*.jpg|*.jpeg|*.png|*.bmp|"
        dialog = wx.FileDialog(self, "Open Text Files", wildcard=wildcard,
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if dialog.ShowModal() == wx.ID_CANCEL:
            return

        path = dialog.GetPath()
        print(path)

    def onOpenDirectory(self, event):
        dialog = wx.DirDialog(
            self,
            "Choose a directory:",
            style=wx.DD_DEFAULT_STYLE
        )

        if dialog.ShowModal() == wx.ID_CANCEL:
            return

        path = dialog.GetPath()
        print(path)

    def OnCloseMe(self, event):
        self.Close(True)

    def OnCloseWindow(self, event):
        self.Destroy()



class App(wx.App):
    def OnInit(self):
        # 创建窗口对象
        frame = MyFrame()
        frame.Show()
        return True

    def OnExit(self):
        print("应用程序退出")
        return 0


if __name__ == '__main__':
    app = App()
    app.MainLoop()