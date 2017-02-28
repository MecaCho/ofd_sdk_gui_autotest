#-*-coding=UTF-8-*-
import commands
import os
import sqlite3
import time
from time import sleep
from dbconnect import createDB
from addFile import allFile
import pyperclip
import string
from dbconnect import getConfig,createlog,createDB,deleteDB,insertResult,createHtmlfromDB,createHtml
import gtk.gdk
softdir = getConfig('database','softdir')
def printScreen(filenamep='screenshot.png'):
    w = gtk.gdk.get_default_root_window()
    sz = w.get_size()
    print "The size of the window is %d x %d" % sz
    pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
    pb = pb.get_from_drawable(w,w.get_colormap(),0,0,0,0,sz[0],sz[1])
    if (pb != None):
        pb.save(filenamep,"png")
        createlog(name='__printScreen__', debug=["Screenshot saved to "+filenamep])
    else:
        createlog(name='__printScreen__',debug=["Unable to get the screenshot."])
def sleep_(sec= getConfig("database","sleep_second")):
	time.sleep(float(sec))

def paste(foo):
    pyperclip.copy(str(foo))
    os.system("xdotool key ctrl+v")
    time.sleep(0.5)

def get_windowID(windowname="福昕版式办公套件"):
    try:
        windowID = os.popen('xdotool search '+windowname).readlines()[0].strip()
        return windowID
    except BaseException as e:
        createlog(name="__get_windowIDError__", error=['get_windowID Error', e])
        return False

def kill_windowID(windowname="福昕版式办公套件"):
    try:
        windowID = os.popen('xdotool search '+windowname).readlines()
        createlog(name="__kill_windowIDError__",debug=['kill_windowID Error', windowID])
        for i in windowID:
            os.popen("xdotool windowkill " + i.strip())
        return True
    except BaseException as e:
        createlog(name="__kill_windowIDError__", error=['kill_windowID Error', e])
        return False

def get_softInfo(softdir):
    soft_version = 'Error'
    softInfo = os.popen(softdir + ' /version').readlines()
    for info in softInfo:
        temp = re.findall(r'Version',info)
        if temp != []:
                soft_version = info
                break
    createlog(name='__get_softInfo__',warn=['Get soft Info Error',BaseException])
    kill_windowID()
    return soft_version
def paste(foo):
    pyperclip.copy(str(foo))
    os.system('xdotool key ctrl+v')
def saveas(filename,function):
    time.sleep(1)
    os.system('xdotool key alt')
    sleep(1)
    os.system('xdotool key f')
    sleep(1)
    os.system('xdotool key a')
    sleep(1)
    now = time.strftime('%Y-%m-%d-%H-%M-%S')
    dir = os.getcwd()
    if not os.path.exists('./outputofd'):
        os.mkdir('./outputofd/')
    output_filepath = dir + '/outputofd/' + filename.split('.')[-2] + '_'+function + '_'+now + '.ofd'
    print output_filepath
    paste(output_filepath)
    os.system('xdotool key alt+s')
    return output_filepath
def openfile(filepath,filename):
    outputFilepath = filepath + '_screenshot.png'
    kill_windowID()
    try:
        ########################################打开套件###################################
        os.system(softdir + ' &')
        reader_hwnd = 0
        while not reader_hwnd:
            reader_hwnd = get_windowID()#os.popen('xdotool search "套件"')
        #######################################打开OFD文件，循环检查【打开】窗口，检测到就进入下一步###################
        op_hwnd = 0
        os.popen('xdotool key Alt+space')
        time.sleep(0.3)
        os.popen('xdotool key x')
        while not op_hwnd:
            os.popen('xdotool windowactivate '+reader_hwnd)
            os.popen("xdotool key ctrl+o")
            op_hwnd = get_windowID("打开一个文件")#os.popen('xdotool search "打开"')
        #######################################在【打开】窗口下，输入文件路径，窗口消失进入下一步#########################
        while op_hwnd:
            os.popen('xdotool windowactivate '+op_hwnd)
            paste(filepath)
            os.popen("xdotool key Return")
            op_hwnd = get_windowID("打开一个文件")
        file_hwnd = get_windowID(filename)
        createlog(name='__filehwnd__',debug=[file_hwnd])
        ################get current window info：windowpid，windowname#############################
        if os.popen('xdotool search "密码"').read():
            printScreen(outputFilepath)
            kill_windowID('密码')
            kill_windowID()
            return [outputFilepath,'加密文档']
        elif os.popen('xdotool search "Critical"').read():
            printScreen(outputFilepath)
            kill_windowID('Critical')
            kill_windowID()
            return [outputFilepath,"Crash"]
        elif len(os.popen('xdotool search "福昕版式办公套件"').readlines()) == 2:
            printScreen(outputFilepath)
            kill_windowID()
            return [outputFilepath,'文档问题']
        elif os.popen('xdotool search '+filename):
            printScreen(outputFilepath)
            file_hwnd = get_windowID(filename)
            createlog(name='__filehwnd__', debug=[file_hwnd])
            return [outputFilepath,"Success"]
        elif os.popen('xdotool search "Metacity"'):
            printScreen(outputFilepath)
            kill_windowID('Metacity')
            kill_windowID()
            return [outputFilepath,"ProgrameError"]
        else:
            printScreen(outputFilepath)
            os.popen("xdotool key Alt+F4")
            kill_windowID()
            return [outputFilepath,"Unknow"]
    except Exception as error_Message:
        printScreen(outputFilepath)
        kill_windowID()
        createlog(name='__openOFDfiles__',error=['open file fail',error_Message])
        return [outputFilepath,'Fail']
def closeFile():
    time.sleep(1)
    os.system("xdotool search --name FoxitOfficeSuite key ctrl+q")
    return

if __name__ == '__main__':
    cu = sqlite3.connect('./db/DB_GUI_Test.db')
    allFile('./testofd')
    curs = cu.cursor()
    path = './testofd'
    #createDB('FunctionTest','function','input','output','Result','testTime','sysTime')
    allFile(path)
    curs.execute("select * from ofdFiles")
    for file in curs.fetchall():
        #openfile('//mnt/Ubuntu_Share/GitLab_Linux_Workspace/pageManage'+file[1][1:])
        openfile(file[1])
        time.sleep(1)
        closeFile()