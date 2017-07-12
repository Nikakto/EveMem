# -*- coding: utf-8 -*-
"""
@author: VaffanCulo
"""

import sys

import pymem
import EveNode
import EveMem

from PyQt5 import QtGui, QtCore, QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self, parent=None):
        
        super(MainWindow, self).__init__(parent)

        self.show()
        self.setWindowTitle('EveMem Tool')
        
            # window size
        self.setMinimumHeight(480)
        self.setMinimumWidth(640)
        
            # create GUI
        self.createGUI()
        
            # main vars (temporary manual imput)
        self.eveOnlineProcessId = 22208
        self.eveOnlineHandle = pymem.openProc(self.eveOnlineProcessId)
        self.eveOnlineNodeUIRoot = 0x1731f2b0
        
            # read GUI and get node of UIRoot
        self.uiRoot = EveNode.Node(self.eveOnlineHandle,self.eveOnlineNodeUIRoot)
        
        self.uiTreeCreate(self.uiRoot)
        
    def createGUI(self):
        ''' create all GUI on layout '''
        
            # create new central widget with layout
        centralWidget = QtWidgets.QWidget(self)
        layout = QtWidgets.QHBoxLayout()
        centralWidget.setLayout(layout)
        
        self.setCentralWidget(centralWidget)
        
            # create UITree Widget and add to layout
        self.widgetUITree = self.createWidgetUITree()
        layout.addWidget(self.widgetUITree)
        
            # create TableData Widget and add to layout
        self.widgetTableData = self.createWidgetTableData()
        layout.addWidget(self.widgetTableData)
        
    def createWidgetTableData(self):
        ''' create TableData '''
        
            # create new table
        widget = QtWidgets.QTableWidget()
        
            # set propeties
        widget.setFixedWidth(520)

            # columns
        widget.setColumnCount(4)
        widget.setColumnWidth(0,200)
        widget.setColumnWidth(1,50)
        widget.setColumnWidth(2,150)
        widget.setColumnWidth(3,100)
        
            # scrolls
        widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        
            # headers
        widget.verticalHeader().hide()
        widget.verticalHeader().setDefaultSectionSize(12)
        
        header = ['Name','Value','Type','Address']
        widget.setHorizontalHeaderLabels(header)
        
        for i in range(widget.columnCount()):
            (widget.horizontalHeaderItem(1))

        return widget
        
    def createWidgetUITree(self):
        ''' create QTreeWidget '''
        
            # create new tree viewer
        widget = QtWidgets.QTreeWidget()
        
            # event
        widget.itemSelectionChanged.connect(self.widgetTableDataUpdate)
        widget.itemExpanded.connect(self.uiTreeAddChildOfChild)
        widget.itemCollapsed.connect(self.uiTreeRemoveChildOfChild)
        
            # set propeties
        widget.setColumnCount(2)
        
        header = ['Nodes','Type']
        widget.setHeaderLabels(header)
        
        return widget
    
    def uiTreeCreate(self, node):
        ''' create uitree with high level from node '''
        
            # create topItem and add it to UITree
        topItem = QtWidgets.QTreeWidgetItem(['UIRoot',node.type])
        topItem.node = node
        
        self.widgetUITree.addTopLevelItem(topItem)
        
            # get children for node (uiroot)
        node.getChildren()
        
            # create widget for each children
        children = []
        for childNode in node.children:
            item = QtWidgets.QTreeWidgetItem([childNode.name,childNode.type])
            item.node = childNode
            children.append(item)
        
            # create children items and update UItree
        topItem.addChildren(children)
        topItem.sortChildren(0,QtCore.Qt.SortOrder(0))
        
        self.widgetUITree.update()
        
    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem)
    def uiTreeAddChildOfChild(self,item):
        ''' add children for item children'''
        
            # get node for item
        node = item.node
        
            # for each child item
        for index in range(item.childCount()):
    
                # get child item
            childItem = item.child(index)
            
                # get child chidren
            childNode = childItem.node
            childNode.getChildren()
            
            children = []
            for childofChildNode in childNode.children:
                
                childOfChildItem = QtWidgets.QTreeWidgetItem([childofChildNode.name,
                                                          childofChildNode.type])
                childOfChildItem.node = childofChildNode
                children.append(childOfChildItem)
                
                # add children to UITree
            childItem.addChildren(children)
            childItem.sortChildren(0,QtCore.Qt.SortOrder(0))
   
    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem)
    def uiTreeRemoveChildOfChild(self,item):
        ''' remove children from item children'''
        
            # get node for item
        node = item.node
        
            # for each child item
        for index in range(item.childCount()):
            
                # get child item
            childItem = item.child(index)
            
                # remove all children
            while childItem.childCount()>0:
                childItem.removeChild(childItem.child(0))
        
    def widgetTableDataUpdate(self):
        ''' update data for selected item '''
        
            # clear table
        self.widgetTableData.clearContents()
        self.widgetTableData.setRowCount(0)
        
            # get node
        currentItem = self.widgetUITree.currentItem()
        node = currentItem.node
        
            # get list of keys for dict propeties
        keys = list(node.propeties.keys())
        keys.sort()
        
            # fill tables
        for key in keys:
            
                # table information
            row = self.widgetTableData.rowCount()
            self.widgetTableData.insertRow(row)
            
                # get some information about ropety
            dataType = EveMem.readType(self.eveOnlineHandle,node.propeties[key])
            value = EveMem.readValue(self.eveOnlineHandle,node.propeties[key])
            
                # item name
            itemName = QtWidgets.QTableWidgetItem(key)
            self.widgetTableData.setItem(row,0,itemName)
            
                # item value
            itemValue = QtWidgets.QTableWidgetItem(str(value))
            self.widgetTableData.setItem(row,1,itemValue)
            
                # item type
            itemType = QtWidgets.QTableWidgetItem(dataType)
            self.widgetTableData.setItem(row,2,itemType)
            
                # item address
            itemAddress = QtWidgets.QTableWidgetItem(str('0x%X' % node.propeties[key]))
            self.widgetTableData.setItem(row,3,itemAddress)
            
            self.widgetTableData.update()
        
if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)

    main = MainWindow()
    main.show()

    sys.exit(app.exec_())
    