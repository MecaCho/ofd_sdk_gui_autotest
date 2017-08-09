#-*-coding=UTF-8-*-
import os
import time
from time import sleep
import pyperclip
from dbconnect import getConfig,createlog
import gtk.gdk
output_filepath = ''
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

def closeofd():
    error_info = check_error()
    if error_info:
        return error_info
    if get_windowID():
        reader_hwnd = get_windowID()
    else:
        reader_hwnd = 0
    while reader_hwnd:
        os.popen('xdotool windowacivate '+str(reader_hwnd))
        os.popen('xdotool key ctrl+q')
        reader_hwnd = get_windowID()
    if not get_windowID():
        return 'Success'
    else:
        return 'CloseFileError'

def xdtkey(keyvalue = '',freq = 1):
    freq = int(freq)
    for i in xrange(freq):
        os.popen('xdotool key '+keyvalue)
    return 'Success'

def xdt(op = '',op1='',freq = 1):
    freq = int(freq)
    for i in xrange(freq):
        op_value = 'xdotool '+str(op)+' '+str(op1)
        os.popen(op_value)
        createlog(debug=[op_value])
    return 'Success'

def paste(foo):
    pyperclip.copy(str(foo))
    os.system("xdotool key ctrl+v")
    time.sleep(0.2)
    return 'Success'

def paste_file(filename = ''):
    foo = filename
    createlog(debug=['paste file',foo])
    pyperclip.copy(str(foo))
    os.system("xdotool key ctrl+v")
    time.sleep(0.3)
    return 'Success'

def paste_save_file(filename= '',filepath ='',FILETYPE='',addChars = '' ):
    filebasename = os.path.splitext(filename)[0]
    now = time.strftime('%Y-%m-%d_%H_%M_%S')
    if not os.path.exists(filepath):
		os.makedirs(filepath)
    foo = filepath + '/'+filebasename+'_'+addChars+now+'.'+FILETYPE
    pyperclip.copy(str(foo))
    createlog(debug=['paste 1', foo])
    os.system("xdotool key ctrl+v")
    sleep(3)
    time.sleep(0.1)
    return 'Success'

def get_windowID(windowname="福昕版式办公套件",id = ' '):
    windowID = os.popen('xdotool search '+windowname).readlines()
    if windowID:
        return windowID[0].strip()
    else:
        return 0

def get_windownum(windowname="福昕版式办公套件",id = ' '):
    windowID = os.popen('xdotool search '+windowname).readlines()
    if windowID:
        return len(windowID)
    else:
        return 0

def kill_windowID(windowname="福昕版式办公套件"):
    try:
        windowID = os.popen('xdotool search '+windowname).readlines()
        for i in windowID:
            os.popen("xdotool windowkill " + i.strip())
        return True
    except BaseException as e:
        return False
def activateWindow(hwnd=''):
    windowID = get_windowID(hwnd)
    os.popen('xdotool windowactivate '+str(windowID))

def opensoft():
    kill_windowID()
    os.system(softdir+' &')
    readhwnd = get_windowID()
    start_time = time.time()
    while not readhwnd:
        if time.time() - start_time >3:
            break
        sleep(1)
        readhwnd = get_windowID()
    if readhwnd:
        return 'Success'
    else:
        return 'OpenSoftError'

def makedirs_(filedir=''):
    createlog(debug=['makedirs',filedir])
    if not os.path.exists(filedir):
        try:
            os.makedirs(filedir)
        except:
            return 'mkdirError'
    return 'Success'

def mkdir(filename='png'):
    global output_filepath
    createlog(debug=['paste', filename])
    output_filepath = str(os.getcwd()) + '/output/' + filename
    if not os.path.exists(output_filepath):
        try:
            os.mkdir(output_filepath)
        except:
            return 'mkdirError'
    now = time.strftime('%Y-%m-%d-%H-%M-%S')
    output_filepath = output_filepath + '/' + filename + '_' + now
    createlog(debug=['paste',output_filepath])
    try:
        os.mkdir(output_filepath)
    except:
        return 'mkdirFileError'
    return 'Success'

def mkfile(funcname='png',filebasename = ''):
    global output_filepath
    filebasename = os.path.splitext(filebasename)[0]
    output_filepath = str(os.getcwd()) + '/output/' + filebasename
    if not os.path.exists(output_filepath):
        try:
            os.mkdir(output_filepath)
        except:
            return 'mkdirError'
    now = time.strftime('%Y-%m-%d-%H-%M-%S')
    output_filepath = output_filepath + '/' + filebasename + '_' + now
    createlog(debug=['paste',output_filepath])
    try:
        os.mkdir(output_filepath)
    except:
        return 'mkdirFileError'
    return 'Success'

def checkhwnd(windowname = ''):
    windowID = os.popen('xdotool search '+windowname).readlines()
    if windowID:
        return len(windowID)
    else:
        return 0
def waitwindow(windowname = ''):
    count = 0
    while count<100:
        if checkhwnd(windowname):
            return 'Success'
        count += 1
    return 'WaitWindowError'


def check_num(proName = 'FoxitOfficeSuite',now = '5',then = '3'):
    now = int(now)
    then = int(then)
    pro_num = get_windownum(windowname=proName)
    start_time = time.time()
    while pro_num != then:
        sleep(2)
        pro_num = get_windownum(windowname=proName)
        if time.time() -start_time > 10:
            return 'TimeOut'
    return 'Success'

def check_error(filename = ''):
    if get_windowID(windowname="密码"):
        return  '加密文档'
    elif get_windowID(windowname="Critical"):
        return  "Crash"
    elif get_windownum() == 2:
        return  '文档问题'
    elif get_windowID(windowname="Metacity"):
        return  "ProgrameError"
    else:
        return 0

def check_error_andkill(filename=''):
    if get_windowID(windowname="密码"):
        kill_windowID()
        return '加密文档'
    elif get_windowID(windowname="Critical"):
        kill_windowID()
        return "Crash"
    elif get_windownum() == 2:
        kill_windowID()
        return '文档问题'
    elif get_windowID(windowname="Metacity"):
        kill_windowID()
        return "ProgrameError"
    else:
        return 0

def sleep(TIME=1):
    time.sleep(int(TIME))
    return 'Success'
def openfile(filepath='',filename=''):
    createlog(debug=[filename,filepath])
    opensoft_info = opensoft()
    if opensoft_info == 'Success':
        op_hwnd = get_windowID('打开一个文件')
        while not op_hwnd:
            xdtkey('ctrl+o',1)
            sleep(0.3)
            op_hwnd = get_windowID('打开一个文件')
        start_time = time.time()
        while op_hwnd:
            activateWindow(hwnd='打开一个文件')
            paste(filepath)
            sleep(0.3)
            xdtkey('Return',1)
            op_hwnd = get_windowID('打开一个文件')
            if time.time() - start_time >3:
                return 'TimeOut'
        check_result = check_error()
        if check_result:
            return check_result
        elif get_windowID(windowname=filename):
                return 'Success'
        elif get_windownum(windowname='FoxitOfficeSuite')==3:
            return 'Success'
        else:
            return '打开文件步骤错误'
    else:
        return opensoft_info



if __name__ =='__main__':
    #result =  openfile('/mnt/Ubuntu_Share/GitLab_Linux_Workspace/GUI_linux_xml/testofd/2s左右/文字+图形+JPG图像600DPI-10页.ofd','文字+图形+JPG图像600DPI-10页.ofd')
    #closeofd()
    #print result
    print checkhwnd('插入空白页')
