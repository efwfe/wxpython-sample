import wx


class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.label = wx.StaticText(self, label="Hello this is a label", style=wx.ALIGN_CENTER)
        vbox.Add(self.label, 1, wx.EXPAND)

        self.label2 = wx.StaticText(self, label="Hello this is a label", style=wx.ALIGN_CENTER)
        hbox.Add(self.label2, 1, wx.EXPAND)

        self.SetSizer(vbox)
        self.SetSizer(hbox)


class MyFrame(wx.Frame):
    def __index__(self, parent, title, size):
        super(MyFrame, self).__index__(parent, title=title, size=size)
        self.panel = MyPanel(self)


class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(parent=None, title="my window", size=(600, 400))
        self.frame.Show(True)
        return True


if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()
