import wx

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)


class MyFrame(wx.Frame):
    def __index__(self, parent, title,size):
        super(MyFrame, self).__index__(parent, title=title, size=size)

        self.panel = MyPanel()

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(parent=None, title="okay",size=(600 , 800))
        self.frame.Show()
        return True


if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()