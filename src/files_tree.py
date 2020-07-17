# -*- coding:utf-8 -*-
"""
@file name :  custom_tree
@description: 
@author:      zhangdh
@date :       2020/7/8-4:10 下午
"""

import wx
from wx.lib.agw.customtreectrl import CustomTreeCtrl
from itertools import chain

class FilesTree(CustomTreeCtrl):
    def __init__(self, parent, style=wx.TR_HIDE_ROOT, **kwargs):
        super(FilesTree, self).__init__(parent, style=style, **kwargs)
        imglist = wx.ImageList(16, 16, True, 2)
        
        imglist.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, size=wx.Size(16, 16)))
        imglist.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, size=(16, 16)))
        self.AssignImageList(imglist)
        self.root = self.AddRoot('目录', image=0)

        self.childs = dict()
        self.childs[self.root] = []

        # todo 点击展示数据到grid中
        # self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, lambda _: print("actived"))

    def addDir2Root(self, directory):
        """
        添加文件夹节点到根目录
        :param directory:
        :return:
        """
        elem = self.AppendItem(self.root, text=directory, image=0)
        self.childs[elem] = []
        return elem

    def addFile2Dir(self, item, parent=None):
        """
        添加文件信息到节点中
        :param parent:
        :param item:
        :return:
        """
        if not parent:
            parent = self.root

        if parent not in self.childs:
            self.childs[parent] = []  
        elem = self.AppendItem(parent, text=item)
        self.childs[parent].append(elem)
        return elem

    def getAllItems(self):
        """获取所有的元素"""
        container = []
        for value in self.childs.values():
            for i in value:
                container.append(i)
        return container

    def getAllData(self):
        items = self.getAllItems()
        data = [self.getItemData(i) for i in items]
        return data

    def setData2Item(self, item, data):
        """
        设置元素的data属性
        :param item:
        :param data:
        :return:
        """
        if not data:
            return item
        if 'file_path' in data:
            print(data)
            if '' in list(chain(*data['data'])):
                self.setColorRed(item)
            else:
                self.setColorBlack(item)
        self.SetPyData(item, data)
        return item

    def getItemData(self, item):
        """
        获取元素的数据
        :param item:
        :return:
        """
        return self.GetItemData(item)

    def setColorRed(self, item):
        self.SetItemTextColour(item, wx.RED)

    def setColorBlack(self, item):
        self.SetItemTextColour(item, wx.BLACK)

    def getAllCodes(self):
        items = self.getAllData()
        datas = [list(chain(*i['data'])) for i in items if 'file_path' in i]
        return list(chain(*datas))