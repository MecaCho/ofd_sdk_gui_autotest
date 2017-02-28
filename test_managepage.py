#-*-coding=UTF-8-*-
import time
import sys,getopt
import os
import subprocess
from dbconnect import *
from casestep import *
from addFile import allFile
def add(a='1', b='2'):
    print a + b
    return ['null','Success']

def run(func):
    dbpath = './db/DB_GUI_Test.db'
    cu = sqlite3.connect(dbpath)
    curs = cu.cursor()
    dir = os.getcwd()
    createlog(name='__main__', info=['Current path: ', dir])
    createDB('GUIFunctionTest1', 'input', 'output', 'Result', 'sysTime')
    curs.execute("select * from ofdFiles where id<3")
    for file in curs.fetchall():
        print file
        print func.__name__
        func(file[2],file[1])
##################################################从ofdFiles数据库读取数据，执行cases，将结果写入结果数据库，并生成html##################################
class runcase(object):
    def __init__(self,func,resultDB='GUItest',resultHtml='Detail.html'):
        self.func = func
        self.resultDB = resultDB
        self.resultHtml = resultHtml
        self.funcname = self.func.__name__
    def run(self):
        startTime = time.time()
        total = 0
        totalPass = 0
        dbpath = './db/DB_GUI_Test.db'
        cu = sqlite3.connect(dbpath)
        curs = cu.cursor()
        dir = os.getcwd()
        createlog(name='__main__', info=['Current path: ', dir])
        deleteDB(self.resultDB)
        createDB(self.resultDB,'funcname', 'filename','filepath', 'output', 'Result', 'sysTime')
        curs.execute("select * from ofdFiles where id<3")
        for file in curs.fetchall():
            total += 1
            print file
            print self.func.__name__
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            ResultInfo = self.func(file[2],file[1])
            if ResultInfo[-1] == 'Success':
                totalPass += 1
            dbinfo = [self.funcname,file[1],file[2]]
            dbinfo = dbinfo+ResultInfo
            createlog(name='dbinfo',debug=['dbinfo : ',dbinfo])
            insertResult(self.resultDB,dbinfo)
        summaryResult = 'Total:' + str(total) + '  Pass:' + str(totalPass)
        duration = time.time() - startTime
        createHtmlfromDB(self.resultDB)
        createHtml(self.funcname, self.resultHtml, str(now), str(duration), summaryResult)
def test_insertBlankPage(filepath='',filename=''):
    ###################,local='',pageSize='',pageNum=''
    if openfile(filepath,filename) == 'Success':
        ########pageManage and insert Blank Page
        try:
            os.system('xdotool key alt')
            time.sleep(1)
            os.system('xdotool key o')
            time.sleep(1)
            os.system('xdotool key i')
            time.sleep(1)
            os.system('xdotool key b')
            time.sleep(1)
            os.system('xdotool getactivewindow')
            os.system('xdotool key alt+o')
            outputFilePath = saveas(filename, function='insertBlankPage')
            sleep(1)
            os.system('xdotool key ctrl+q')
            closeFile()
            createlog(name='__insertBlankPage__', debug=[filename, outputFilePath])
            lostTime = 5 + 4.036 + 0.072
            result = 'Success'
            return [outputFilePath,result]
        except BaseException as errorMessage:
            createlog(name='__insertBlankPage__',error=[errorMessage,'line:81'])
            return ['null','Error']
    return ['null','OpenFileError']


def insertFilePage(filepath='',filename=''):
    '''insert Page From File'''
    #############insert Page from Files########
    if openfile(filepath,filename) == 'Success':
        try:
            openfile(filepath)
            os.system('xdotool key alt')
            sleep(1)
            os.system('xdotool key o')
            sleep(1)
            os.system('xdotool key i')
            sleep(1)
            os.system('xdotool key f')
            sleep(1)
            os.system('xdotool key alt+a')
            sleep(1)
            os.system('xdotool key "Return"')
            sleep(1)
            os.system('xdotool key "Return"')
            sleep(1)
            insertFile = dir + '/testofd/insertFile.ofd'
            paste(insertFile)
            sleep(1)
            os.system('xdotool key "Return"')
            sleep(1)
            os.system('xdotool key "Return"')
            sleep(1)
            outputFilePath = saveas(filename, function='insertPageFromFiles')
            sleep(1)
            os.system('xdotool key ctrl+q')
            closeFile()
            createlog(name='__insertFilePage__', debug=[filename, outputFilePath], info=[], warn=[], error=[], fetal=[])
            lostTime = 11 + 4.036 + 0.120
            return [outputFilePath, 'Success']
        except BaseException as errorMessage:
            createlog(name='__insertFilePage__', error=[errorMessage, 'line:123'])
            return ['null', 'Error']
    return ['null', 'OpenFileError']


def test_extractPage(filepath='',filename=''):  ########mode:perPage a doc or allPage a doc
    '''extractPage'''
    #######################extract Page 1
    if openfile(filepath,filename) == 'Success':
        try:
            os.system('xdotool key alt')
            sleep(1)
            os.system('xdotool key o')
            sleep(1)
            os.system('xdotool key e')
            sleep(1)
            for i in range(3): os.system('xdotool key Tab')
            print paste('1')
            sleep(1)
            os.system('xdotool key "Return"')
            sleep(1)
            now = time.strftime('%Y-%m-%d-%H-%M-%S')
            if not os.path.exists('./testofd/outputofd'): os.mkdir('./testofd/outputofd')
            if mode == 'perpage':
                output_filepath = dir + '/testofd/outputofd/' + os.path.splitext(filename)[0] + '_' + 'extractPage' + '_' + now
            else:
                output_filepath = dir + '/testofd/outputofd/' + os.path.splitext(filename)[
                    0] + '_' + 'extractPage' + '_' + now + '.ofd'
            paste(output_filepath)
            sleep(1)
            os.system('xdotool key alt+s')
            closeFile()
            createlog(name='__extractPage__', debug=[filename, output_filepath], info=[], warn=[], error=[], fetal=[])
            lostTime = 6 + 0.072
            return [outputFilePath, result]
        except BaseException as errorMessage:
            createlog(name='__extractPage__', error=[errorMessage, 'line:123'])
            return ['null', 'Error']
    return ['null', 'OpenFileError']
def test_exchangePage(self, pageNo1='', pageNo2=''):
    ####################exchange Page 3 and 1
    if openfile(filepath,filename) =="Success":
        try:
            os.system('xdotool key alt')
            sleep(1)
            os.system('xdotool key o')
            sleep(1)
            os.system('xdotool key x')
            sleep(1)
            os.system('xdotool key Tab')
            sleep(1)
            print paste('2')
            sleep(1)
            os.system('xdotool key "Return"')
            sleep(1)
            outputFilePath = saveas(filename, function='exchangePage2and1')
            os.system('xdotool key ctrl+q')
            time.sleep(1)
            closeFile()
            createlog(name='__exchangePage__', debug=[filename, outputFilePath], info=[], warn=[], error=[], fetal=[])
            lostTime = 7 + 4.036 + 0.072
            return [outputFilePath, result]
        except BaseException as errorMessage:
            createlog(name='__exchangePage__', error=[errorMessage, 'line:123'])
        return ['null', 'Error']
    return ['null', 'OpenFileError']
def test_dropPage(filepath,filename):
    '''Delete Page'''
    #############delete Page###########
    if openfile(filepath,filename) == 'Success':
        try:
            os.system('xdotool key alt')
            sleep(1)
            os.system('xdotool key o')
            sleep(1)
            os.system('xdotool key d')
            sleep(1)
            print paste('1')
            os.system('xdotool key "Return"')
            sleep(1)
            outputFilePath = saveas(filename, function='deletePage1')
            os.system('xdotool key ctrl+q')
            time.sleep(1)
            closeFile()
            createlog(name='__dropPage__', debug=[filename, outputFilePath], info=[], warn=[], error=[], fetal=[])
            lostTime = 5 + 4.036 + 0.060
            return [outputFilePath, result]
        except BaseException as errorMessage:
            createlog(name='__dropPage__', error=[errorMessage, 'line:123'])
        return ['null', 'Error']
    return ['null', 'OpenFileError']
def test_replacePage(self, sourceFile='', sourcePageRange='', desPageRange=''):
    '''replace Page from source Files'''
    #############replace Page from replacePage
    if openfile(filepath,filename) == 'Success':
        try:
            os.system('xdotool key alt')
            sleep(1)
            os.system('xdotool key o')
            sleep(1)
            os.system('xdotool key r')
            sleep(1)
            replacePage = dir + '/testofd/replace.ofd'
            paste(replacePage)
            sleep(1)
            os.system('xdotool key "Return"')  ###############################选择文件后确认
            sleep(1)
            os.system('xdotool key "Return"')  ###############################确认替换页
            sleep(1)
            outputFilePath = saveas(filename, function='replacePage')
            time.sleep(1)
            closeFile()
            createlog(name='__replacePage__', debug=[filename, outputFilePath], info=[], warn=[], error=[], fetal=[])
            lostTime = 7 + 4.036 + 0.060
            return [outputFilePath, result]
        except BaseException as errorMessage:
            createlog(name='__replacePage__', error=[errorMessage, 'line:123'])
        return ['null', 'Error']
    return ['null', 'OpenFileError']
def test_splitPage(self, splitMode, pageNum='', desFileMode='', desPath=''):
    '''splitPage'''
    ###################split Page
    if openfile(filepath,filename) == 'Success':
        try:
            os.system('xdotool key alt')
            sleep(1)
            os.system('xdotool key o')
            sleep(1)
            os.system('xdotool key s')
            sleep(1)
            for i in range(3): os.system('xdotool key Tab')
            os.system('xdotool key "Return"')
            sleep(1)
            # saveas(filename,function='splitPage')######save as others files
            os.system('xdotool key ctrl+q')
            time.sleep(1)
            closeFile()
            createlog(name='__splitPage__', debug=[filename, filepath], info=[], warn=[], error=[], fetal=[])
            lostTime = 6 + 0.072
            return [outputFilePath, result]
        except BaseException as errorMessage:
            createlog(name='__splitPage__', error=[errorMessage, 'line:123'])
        return ['null', 'Error']
    return ['null', 'OpenFileError']



if __name__ =='__main__':
    opts,args = getopt.getopt(sys.argv[1:],"hi:o:",['insert','insertf','drop','move','exchange','replace','extract','split'])
    #test_insertBlankPage('/mnt/Ubuntu_Share/GitLab_Linux_Workspace/GUI_linux/testofd/saveas.ofd','saveas.ofd')
    try:
        op = sys.argv[1]
    except BaseException as e:
        op = ''
        createlog(name='__', info=['python shell argvs : ', op, e])
    if op == 'insert':
        case = runcase(test_insertBlankPage,resultDB='insertBlankPage',resultHtml='insertBlankPage.html')
        case.run()
    elif op == 'insertf':
        case = run(insertFilePage,resultDB = 'insertPagefrom')
        #run(test_insertBlankPage)



