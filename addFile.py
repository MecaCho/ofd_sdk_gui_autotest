#-*- coding=UTF-8 -*-
import os
from dbconnect import createDB,insertResult,deleteDB
dir = os.getcwd()+'/testofd/'
print dir
def allFile(dir):
    deleteDB('ofdFiles')
    createDB('ofdFiles','id', 'filename TEXT', 'filepath', 'filesize(KB)', 'filetype', 'sysTime')
    path = os.walk(dir)
    dblist = []
    file_id = 0
    for path,d,filenames in path:
        #print d
        for filename in filenames:
            fileType = os.path.splitext(filename)
            print fileType
            dblist = []
            if fileType[1] == '.ofd':
                temp  = os.path.join(path, filename)
                dblist.append(file_id)
                file_id += 1
                dblist.append(filename)
                dblist.append(temp)
                filesize = os.path.getsize(temp)/1024
                if filesize == 0:
                    filesize = '<1KB'
                dblist.append(filesize)
                dblist.append('ofd')
                print dblist
                print 'dblist:',dblist
                insertResult('ofdFiles',dblist)
            else:
                print 'not OFD'
            print os.path.join(path,filename)
if __name__ == '__main__':
    allFile(dir)
