#-*-coding=UTF-8-*-
import sys
import optparse
from time import sleep,time
from dbconnect import *
from funclib import *
from addFile import allFile,getdbTBinfo
import os
reload(sys)
sys.setdefaultencoding('utf-8')
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
FILENAME = ''
FILEPATH = ''
testCaseName = ''
funcResult = 'Error'

##############################单个函数入口；初始化:函数名，参数list#######################################
    #############################可以传入1,2,3个参数####################################################
def runfunc(func,arg):
    arg_num = len(arg)
    print func
    if arg_num == 0:
        #############################################粘贴文件路径名要单独处理，每次粘贴的路径名不相同############
        if func == 'paste_file':
            return paste_file(filename=FILEPATH)
        elif func == 'openfile':
            return openfile(FILEPATH,FILENAME)
        return eval(func)()
    elif arg_num == 1:
        ##########################新建文件夹需要根据测试文件的文件名来命名#######################################
        if func == 'mkfile':
            ############################第一个参数为文件类型参数##################
            return eval(func)(arg[0],FILENAME)
        return eval(func)(arg[0])
    elif arg_num == 2:
        ############################另存为文件时，需要粘贴不同文件路径的文件名#################################
        if func == 'paste_save_file':
            return eval(func)(FILENAME,arg[0],arg[1],testCaseName)
        return eval(func)(arg[0],arg[1])
    elif arg_num == 3:
        return eval(func)(arg[0],arg[1],arg[2])
    else:
        ################处理较长的xdotool命令########################################
        return eval(func)(' '.join(arg[:-1]), 1)

#####################################解析函数List#################
def paser_step(funclist):
    ########################定义全局变量funcResult,每执行一个单个步骤，更改一次funcResultde值，如果不为Success则return跳出函数，如果为Success则顺序执行###################
    global funcResult
    print 'funclist : ',funclist,type(funclist)
    if type(funclist) == 'str':
        funclist = [funclist]
    funcResult = 'Error'
    func_num = len(funclist)
    ##################如果是单个函数，则直接执行#######################
    if func_num == 1 :
        funcargs = funclist[0].split(' ')
        funcname = funcargs[0]
        createlog(debug=[funcname, funcargs])
        arg = []
        if len(funcargs) >1:
            arg = funcargs[1].split(',')
        funcResult =  runfunc(funcname,arg)
        error_info = check_error()
        createlog(error=['paser:',funcargs,'Result : ',error_info])
        if error_info:
            return error_info
        if funcResult != 'Success':
            return funcResult
    ##########################如果需要检查的窗口在最前面，代表执行动作直到窗口消失，循环执行窗口后的动作################
    elif not funclist[0].find('['):
        hwnd = funclist[0].strip('[]')
        startTime = time.time()
        while checkhwnd(hwnd):
            createlog(debug=['checkHwnd : ',hwnd,'check result : ',checkhwnd(hwnd)])
            if time.time() - startTime >5:
                return 'TimeOut'
            paser_step(funclist[1:])
    ########################如果需要检查的窗口在最后面，代表循环执行动作，直到窗口出现##################################
    elif not funclist[func_num-1].find('['):
        hwnd = funclist[func_num-1].strip('[]')
        startTime = time.time()
        createlog(debug=[hwnd,funclist])
        while not checkhwnd(hwnd):
            createlog(debug=['checkHwnd : ', hwnd, 'check result : ', checkhwnd(hwnd)])
            if time.time() - startTime >5:
                return 'TimeOut'
            paser_step(funclist[:-1])
    #########################如果窗口以#标记，则表示，先激活当前窗口，然后执行后续操作##################################
    elif not funclist[0].find('#'):
        hwnd = funclist[0].strip('#')
        activateWindow(hwnd)
        paser_step(funclist[1:])
    ##################################如果不是单个函数，则按顺序执行每个函数#######################################
    else:
        for func in funclist:
            result = paser_step([func])
            if funcResult != 'Success':
                return result
    return funcResult
############解析完函数串没有返回错误，说明执行函数串成功，返回成功###################################

##############################################读取xml文件##########################################################
def read_xmlFile(xmlfilename = 'export.xml'):
    try:
        tree = ET.parse(xmlfilename)
        root = tree.getroot()
        for child in root:
            for ch in child.getchildren():
                funcs = str(ch.text).split(';')
                result = paser_step(funcs)
                createlog(debug=['xmlResult: ',result])
                if result != 'Success':
                    return result
                for func in funcs:
                    print 10 * '*', func
        return result
    except Exception,e:
         createlog(error=['xmlPaserError',e])
         return 'xmlPaserError'

######################从ofdFiles数据库读取文件数据，每一条ofd文件都根据xml的操作步骤执行cases，将结果写入结果数据库，并生成html##################################
def connectdb():
    dbpath = getConfig('database','dbpath')
    cu = sqlite3.connect(dbpath)
    curs = cu.cursor()
    curs.execute("select * from ofdFiles where id < 3")
    return curs.fetchall()
def runcase(resultDB='GUItest',resultHtml='Detail.html',xmlfile = 'export.xml'):
    func = xmlfile
    xmlfilename = os.path.split(xmlfile)[1]
    global FILENAME,FILEPATH,testCaseName
    testCaseName = os.path.splitext(xmlfilename)[0]
    startTime = time.time()
    total = 0
    totalPass = 0
    createlog(name='__main__', info=['Current path: ', os.getcwd()])
    deleteDB(resultDB)
    createDB(resultDB,'funcname', 'filename','filepath', 'output', 'Result', 'sysTime')
    allTestOFDfiles = connectdb()
    for file in allTestOFDfiles:
        FILENAME = file[1]
        FILEPATH = file[2]
        total += 1
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        if xmlfilename == 'openclose.xml':
            openfileInfo = 'Success'
        else:
            openfileInfo = openfile(FILEPATH, FILENAME)
            createlog(error=[xmlfile])
        if openfileInfo == 'Success':
            ResultInfo = read_xmlFile(xmlfilename=xmlfile)
            createlog(debug=['resultInfo0 : ', ResultInfo])
        else:
            ResultInfo = openfileInfo
            createlog(debug=['resultInfo1 : ', ResultInfo])
        createlog(debug=['resultInfo : ',ResultInfo])
        #####################每个函数如果执行成功，则返回’Success‘，否则返回错误截图路径，以及错误信息############
        if ResultInfo == 'Success':
            totalPass += 1
            ResultInfo = ['null','Success']
        else:
            errorPath = FILEPATH+ResultInfo+'_scrot.png'
            printScreen(filenamep=errorPath)
            ResultInfo = [errorPath,ResultInfo]
            check_error_andkill()
            kill_windowID()
        dbinfo = [func,FILENAME,FILEPATH]
        dbinfo = dbinfo+ResultInfo
        createlog(name='dbinfo',debug=['dbinfo : ',dbinfo])
        insertResult(resultDB,dbinfo)
        createlog(name='caseEnd',debug=[200*'#'])
    summaryResult = 'Total:' + str(total) + '  Pass:' + str(totalPass)
    duration = time.time() - startTime
    createHtmlfromDB(resultDB)
    createHtml(resultDB, resultHtml, str(now), str(duration), summaryResult)
        

if __name__ == '__main__':
    xmlfilepath = getConfig('database','xmlpath')
    allFile(xmlfilepath, FILETYPE='xml')
    parser = optparse.OptionParser()
    options,args = parser.parse_args()
    for op in args:
        if op != '':
            xmlfilename = op+'.xml'
            print 100*'#',xmlfilename
            goalcase = getdbTBinfo(goalDB='xmlFiles',where='where filename='+'"'+xmlfilename+'"')
            print goalcase
            for file in goalcase:
                runcase(resultDB=op,resultHtml=op+'.html',xmlfile=file[2])