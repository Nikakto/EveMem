# -*- coding: utf-8 -*-
"""
@author: VaffanCulo
"""

import pymem
import EveMem

    # values of module
simpleTypes = ['int','float','bool','NoneType','str','instancemethod']

    # represent list (sometimes list contains nodes)
simpleNode = ['list','Bunch', 'tuple']

    # classes
class Node:
    ''' represent all expandable  objects '''
    
    def __init__(self, handle, address, parent = None, defaultName = 'Node'):
        
            # simple data
        self.address = address
        self.handle = handle
        self.parent = parent
        
            # try to get type
        self.type = EveMem.readType(handle, address)
        self.name = defaultName
        self.children = []
        
            # try to get node propeties
        self.propeties = EveMem.readNode(handle, address)
            
            # if can get it
        if self.propeties:
            self.name = self.getName()
            
    def fromDict(self):
        ''' create node from dict '''
        
        self.propeties = EveMem.readDict(self.handle, self.address)
            
    def fromList(self):
        ''' create node from list '''
        
            # read list
        values = EveMem.readList(self.handle, self.address)
        
            # fill temporary propeties
        propeties = dict()
        for value in values:
            propeties[str(len(propeties))] = value
            
            # set propeties
        self.propeties = propeties
        
    def fromTuple(self):
        ''' create node from tuple '''
    
            # get len of tuple
        length = pymem.readInt(self.handle,self.address+8)
        
            # fill temporary propeties
        propeties = dict()
        for index in range(length):
            value = pymem.readInt(self.handle,self.address+12+4*index)
            propeties[str(len(propeties))] = value
            
            # set propeties
        self.propeties = propeties
        
    def getChildren(self):
        ''' node will get all expandable childrens '''
        
        children = []
        
            # for each propeties
        keys = list(self.propeties.keys())
        for key in keys:
            
                # get dataType of propety
            dataType = EveMem.readType(self.handle,self.propeties[key])
            
                # if not simple type
            if dataType not in simpleTypes:
                
                    # if simple node
                if dataType in simpleNode:
                    
                        # create child node from list
                    if dataType == 'list':
                        childNode = Node(self.handle, self.propeties[key], defaultName = key)
                        childNode.fromList()
                        children.append(childNode)
                        
                    elif dataType == 'tuple':
                        childNode = Node(self.handle, self.propeties[key], defaultName = key)
                        childNode.fromTuple()
                        children.append(childNode)
                        
                        # create child node from bunch
                    elif dataType == 'Bunch':
                        childNode = Node(self.handle, self.propeties[key], defaultName = key)
                        childNode.fromDict()
                        children.append(childNode)
                        
                        # create child node from dict
                    elif dataType == 'dict':
                        print('dict: ', "%X" % (self.propeties[key]))
                        childNode = Node(self.handle, self.propeties[key], defaultName = key)
                        childNode.fromDict()
                        children.append(childNode)
                
                    # create child node
                if EveMem.readNode(self.handle, self.propeties[key]):
                    childNode = Node(self.handle, self.propeties[key], self, key)
                    children.append(childNode)
                
        self.children = children
                
    def getName(self):
        ''' return '_name' from propeties '''
        
        if '_name' in self.propeties.keys():
            address = self.propeties['_name']
            return EveMem.readString(self.handle, address)
        else:
            return self.name
