import wx

class Frame(wx.Frame):

    def __init__(self, title, pos, size):
        wx.Frame.__init__(self, None, -1, title, pos, size)
        menuFile = wx.Menu()
        menuFile.Append(1, "&About...")
        menuFile.AppendSeparator()
        menuFile.Append(2, "E&xit")
        menuBar = wx.MenuBar()
        menuBar.Append(menuFile, '&File')

        self.SetMenuBar(menuBar)
        self.CreateStatusBar()
        self.SetStatusText("Welcome to wxPython")
        self.Bind(wx.EVT_MENU, self.OnAbout, id=1)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=2)


    def OnAbout(self, event):
        wx.MessageBox("this is a hello boxy","About Hello",
                      wx.OK | wx.ICON_INFORMATION, self)

    def OnQuit(self, event):
        self.Close()

class MyApp(wx.App):
    def OnInit(self):
        frame = Frame("hello world ", (50,60),(450, 340))
        frame.Show()
        self.SetTopWindow(frame)
        return True

if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()

