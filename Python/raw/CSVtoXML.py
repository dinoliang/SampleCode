import array as arr
import numpy as np
import time
import csv
import scipy.misc
import matplotlib.pyplot as plt
import os
import xml.etree.ElementTree as ET

StartTime = time.time()

g_sFilePath = '/home/dino/RawShared/Temp/'
g_sInFile = 'ZettTool_StringTable.csv'
g_sOutFile = 'Language_{}.xml'
g_sLanguage = 'zh-CN' #'en-US' / 'ja-JP' / 'zh-TW' / 'zh-CN'
g_sXMLStringFormat = '<String no=\"{}\" text=\"{}\"/>'

g_bFirstOpen = False

def prettyXml(element, indent, newline, level = 0): # Elment class by elemnt，indent for indentation，newline for wrap
    if element: # have child item of element
        if element.text == None or element.text.isspace(): # no content of element text
            element.text = newline + indent * (level + 1)  
        else: 
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1) 
    #else: # 此处两行如果把注释去掉，Element的text也会另起一行 
    #element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level 
    temp = list(element) # 将elemnt转成list 
    for subelement in temp: 
        if temp.index(subelement) < (len(temp) - 1): # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致 
            subelement.tail = newline + indent * (level + 1) 
        else: # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个 
            subelement.tail = newline + indent * level 
        prettyXml(subelement, indent, newline, level = level + 1) # 对子元素进行递归操作 

def WriteXML(rows):
    sOutFileTemp = g_sOutFile.format(g_sLanguage);
    sOutFile = g_sFilePath + sOutFileTemp
    if os.path.exists(sOutFile):
        os.remove(sOutFile)

    #NodeRoot = ET.Element('?xml version=\"1.0\" encoding=\"utf-8\"')

    Node1 = ET.Element('ZettTool')
    #Node1 = ET.SubElement(NodeRoot, 'ZettTool')
    Node1.attrib = {'Language' : g_sLanguage}

    Node2 = ET.SubElement(Node1, 'Text')

    for row in rows:
        #print(row)
        #sStringFormat = g_sXMLStringFormat.format(row[0], row[1])
        #print(sStringFormat)
        Node3 = ET.SubElement(Node2, 'String')
        Node3.attrib = {'no' : row[0], 'text' : row[1]}

    prettyXml(Node1, '\t', '\n')
    #Tree = ET.ElementTree(NodeRoot)
    Tree = ET.ElementTree(Node1)
    Tree.write(sOutFile, encoding='utf-16', xml_declaration=True)

    return

def CSVtoXML():

    sInFile = g_sFilePath + g_sInFile
    with open(sInFile, newline="", encoding="utf-16")as file:
        rows = csv.reader(file)
        #dataList = list(rows)
        #print(dataList)
        WriteXML(rows)

    return

if __name__ == "__main__":
    CSVtoXML()
    pass

EndTime = time.time()
print("Durning Time(sec): ", EndTime - StartTime)
