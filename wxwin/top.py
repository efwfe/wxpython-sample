import wx
# todo 数据查看 编辑

class TopFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, "PowerParse", size=(600, 800))

        # menubar
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


if __name__ == '__main__':
    app = wx.App()
    frame = TopFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
