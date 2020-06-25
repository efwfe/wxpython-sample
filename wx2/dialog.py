import wx

class App(wx.App):
    def __init__(self, redirect=True, filename=None):
        wx.App.__init__(self,redirect, filename)


    def OnInit(self):
        dlg = wx.MessageDialog(None, "Is this the coolest thing ever!",
                           "MessageDialog",wx.YES_NO | wx.ICON_QUESTION )
        result = dlg.ShowModal()
        print(result)
        dlg.Destroy()

        dlg = wx.TextEntryDialog(None, "Who is buried in Grant's tomb",
                                 "A Question", "Cary Grant")

        if dlg.ShowModal() == wx.ID_OK:
            response = dlg.GetValue()
            print(response)

        dlg.Destroy()
        dlg = wx.SingleChoiceDialog(None,"what version of python are you using?",
                                    "Single Choice", ['2.1',"2.7","3.8"])

        if dlg.ShowModal() == wx.ID_OK:
            response = dlg.GetStringSelection()
            print(response)
        dlg.Destroy()
        return True

if __name__ == '__main__':
    app = App(False, "output")
    app.MainLoop()
