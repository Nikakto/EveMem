# -*- coding: utf-8 -*-
"""
@author: VaffanCulo
"""

import pymem

def readDict(handle, address):
    ''' read python dict & bunch from address'''
    
    ###
    typedict = readType(handle, address)
    ###
    size = pymem.readInt(handle,address+8)
    
    data = dict()

    # get ma_loc
    ma_loc = pymem.readInt(handle,address+20)
    
    # read small table
    if ma_loc == address+28:
        for i in range(8):
    
            data_hash = pymem.readInt(handle,address+16+12*i)
            data_key_adrs = pymem.readInt(handle,address+16+12*i+4)
            
            if data_key_adrs!=0:
                keylen = pymem.readInt(handle,data_key_adrs+8)
                
                if keylen<50 and keylen>0:
                    
                    keyType = readType(handle, data_key_adrs)
                    
                    if 'str' == keyType:
                        key = pymem.readBytes(handle,data_key_adrs+20,keylen).decode("utf-8")
                    elif 'unicode' == keyType:
                        key = readStringUnicode(handle, data_key_adrs)
                    else:
                        continue

                    data_data_adrs = pymem.readInt(handle,address+16+12*i+8)
                    data[key] = data_data_adrs

    # if maloc is pointer to additional table
    else:
        
        i = -1
        while len(data)<size:
            
            i=i+1
            
                # if too much slot index
            print(i,size)
    
            data_hash = pymem.readInt(handle,ma_loc+12*i)
            data_key_adrs = pymem.readInt(handle,ma_loc+12*i+4)
            
            if data_key_adrs!=0:
                keylen = pymem.readInt(handle,data_key_adrs+8)
                
                if keylen<50 and keylen>0:
                    
                    keyType = readType(handle, data_key_adrs)
                    
                    if 'str' == keyType:
                        key = pymem.readBytes(handle,data_key_adrs+20,keylen).decode("utf-8")
                    elif 'unicode' == keyType:
                        key = readStringUnicode(handle, data_key_adrs)
                    else:
                        continue
                                            
                    data_data_adrs = pymem.readInt(handle,ma_loc+12*i+8)
                    data[key] = data_data_adrs
                            
    return data

def readList(handle, address):
    ''' return pithon <list> from address'''
    
    size = pymem.readInt(handle, address+8)
    
    list_address = pymem.readInt(handle, address+12)
    list_data = []
    
    while len(list_data)<size:

        list_data.append(pymem.readInt(handle,list_address))
        list_address+=4
        
    return list_data
    
def readNode(handle, address):
    ''' read eve online node from address
        return dict of content
        key - attribute
        value - address
    '''
    
    try:
        dictAddrs = pymem.readInt(handle, address+8)
        
        if 'dict' == readType(handle,dictAddrs):
            data = readDict(handle,dictAddrs)
            return data
        
        else:
            return None
    
    except Exception:
        return None
    
def readString(handle, address):
    ''' return python <string> from address '''
    
    size = pymem.readInt(handle,address+8)
    string = pymem.readBytes(handle,address+20,size).decode('utf-8')

    return string

def readStringUnicode(handle, address):
    ''' return unicode <string> from address '''
    
    size = pymem.readInt(handle,address+8)
    stringAddress = pymem.readInt(handle,address+12)
    string = pymem.readBytes(handle,stringAddress,size*2)
    string = ''.join([chr(string[each]) for each in range(0,size*2,2)])

    return string

def readType(handle, address):
    ''' return type of value in address '''
    
    try:
        type_address = pymem.readInt(handle,address+4)
        type_address_str =  pymem.readInt(handle,type_address+12)
        
        type_name = ''
        while pymem.readByte(handle,type_address_str) > 0:
            type_name += chr(pymem.readByte(handle,type_address_str))
            type_address_str += 1
            
        return type_name
    
    except Exception:
        return None

def readValue(handle, address):
    ''' return int or float value from address
        for list, dict, bunch return size
        for other None
    '''
    
    dataType = readType(handle, address)
    
    if 'int' == dataType:
        return pymem.readInt(handle, address+8)
        
    elif 'float' == dataType:
        return pymem.readDouble(handle, address+8)
        
    elif 'bool'  == dataType:
        return pymem.readByte(handle, address+8)
        
    elif 'str'  == dataType:
        return readString(handle, address)
    
    elif 'unicode' == dataType:
        return readStringUnicode(handle, address)
        
    elif 'list' == dataType:
        return pymem.readInt(handle, address+8)
    
    elif 'Bunch' == dataType:
        return pymem.readInt(handle, address+8)
    
    elif 'dict' == dataType:
        return pymem.readInt(handle, address+8)
    
    elif 'LayerCore' == dataType:
        sizeAddress = pymem.readInt(handle, address+8)
        return pymem.readInt(handle, sizeAddress+8)
    
    elif 'PyChildrenList' == dataType:
        sizeAddress = pymem.readInt(handle, address+8)
        return pymem.readInt(handle, sizeAddress+8)
    
    else:
        return None