#-*- coding=UTF-8 -*-
import os
import sqlite3
import optparse
from dbconnect import getConfig
from dbconnect import createDB,insertResult,deleteDB
dir = os.getcwd()
#print dir
def getdbTBinfo(goalDB='GUItest',where= 'where id <10'):
        dbpath = getConfig('database','dbpath')
        cu = sqlite3.connect(dbpath)
        curs = cu.cursor()
        where = "select * from "+goalDB+" "+where
        #print where
        curs.execute(where)
        #curs.execute('select * from xmlFiles where filename="openclose.xml"')

        return curs.fetchall()
def allFile(dir,FILETYPE= 'ofd'):
    dbTable = FILETYPE+'Files'
    FILETYPE = '.'+FILETYPE
    deleteDB(dbTable)
    createDB(dbTable,'id', 'filename', 'filepath', 'filesize(KB)', 'filetype', 'sysTime')
    paths = os.walk(dir)
    dblist = []
    file_id = 0
    for path,d,filenames in paths:
        #print d
        for filename in filenames:
            fileType = os.path.splitext(filename)
            print fileType
            dblist = []
            if fileType[1] == FILETYPE:
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
                print 'dblist:',dblist
                insertResult(dbTable,dblist)
            else:
                print 'not '+FILETYPE
if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-i','--input',action = 'store',default = dir +'/testofd',type = str,dest = 'FilePath',)
    parser.add_option('-o','--ofd',action = 'store',default = dir +'/testofd',type = str,dest = 'ofdFilePath',)
    parser.add_option('-x','--xml',action = 'store',default = dir +'/testcases',type = str,dest = 'xmlFilePath',)
    options,args = parser.parse_args()
    for arg in args:
        print arg
        allFile(options.FilePath,arg)
        #allFile(options.ofdFilePath, '.ofd', 'ofdFiles')
    allFile(options.ofdFilePath,'ofd')
    allFile(options.xmlFilePath,'xml')
    print options
    print options.FilePath
    #print getdbTBinfo(goalDB='xmlFiles',where='where filename="openclose.xml"')
