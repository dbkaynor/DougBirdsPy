import os
import logging
import argparse
import __main__ as main
from inspect import currentframe, getframeinfo
import subprocess
from subprocess import Popen, PIPE
from tkinter import *
import tkinter.messagebox

# TODO

#------------------------------
# Checks if file name exists
# File may be either on the system path
# or file may be a full path
def SearchPath(name):
  path = os.environ['PATH']
  for dir in path.split(os.pathsep):
    binpath = os.path.join(dir, name)
    if os.path.exists(binpath):
      return True
  return False
#------------------------------
#Parses the frame inspect information
def MyTrace(FrameInfoDict):
    filename = 0
    lineno = 1
    function = 2
    return FrameInfoDict[function], FrameInfoDict[lineno], FrameInfoDict[filename]
#------------------------------
#Displays a custom messagebox
def MyMessageBox(Title='MyMessageBox', XSize=250, YSize=120 ):
    MyMessageBoxToplevel = Toplevel()
    MyMessageBoxToplevel.title(Title)
    MyMessageBoxToplevelX = XSize
    MyMessageBoxToplevelY = YSize
    '''
    MyMessageBoxToplevel.wm_transient(Main)
    Mainsize = Main.geometry().split('+')
    x = int(Mainsize[1]) + (MyMessageBoxToplevelX / 2)
    y = int(Mainsize[2]) + (MyMessageBoxToplevelY / 2)
    MyMessageBoxToplevel.geometry("%dx%d+%d+%d" % (MyMessageBoxToplevelX, MyMessageBoxToplevelY, x, y))
    '''
    MyMessageBoxToplevel.resizable(1,1)

    Label(MyMessageBoxToplevel, text='Left:  ',
        relief=GROOVE).pack(expand=FALSE, fill=X)

    TextBox = Text(MyMessageBoxToplevel, height=2, width=30)
    TextBox.pack()

    Label(MyMessageBoxToplevel, text='Right:  ',
        relief=GROOVE).pack(expand=FALSE, fill=X)

    Button(MyMessageBoxToplevel, text='Close', command=lambda : MyMessageBoxToplevel.destroy()).pack()

#------------------------------
#Logs a message to a disk file. Optionaly Prints to command line and/or displays a MessageBox
def Logger(LogMessage = '', FrameInfoDict=None, PrintToCommandLine=False, MessageBox = False):
    MyLogger = logging.getLogger()
    if FrameInfoDict:
        mystr = LogMessage + '  Trace: ' + str(MyTrace(FrameInfoDict))
    else:
        mystr = LogMessage
    MyLogger.debug(mystr)
    if PrintToCommandLine: print(mystr)
    if MessageBox: tkinter.messagebox.showerror('Logger message', mystr)
    #print('Logger OK')
#------------------------------
#Parse the command line
def ParseCommandLine():
    parser = argparse.ArgumentParser(description='A tool to compare to directories and move files')
    parser.add_argument('-debug',help='Enable debugging',action='store_true')
    args = parser.parse_args()

    if args.debug:
        import pdb
        pdb.set_trace()
        Logger('debug is on', getframeinfo(currentframe()))
    else:
        Logger('debug is off', getframeinfo(currentframe()))
#------------------------------
#This function starts a system file such as notepad.exe
def StartFile(filename, arg1='', arg2='', arg3=''):
    if arg1 == '':
        args = [filename]
    elif arg2 == '':
        args = [filename, arg1]
    elif arg3 == '':
        args = [filename, arg1, arg2]
    else:
        args = [filename, arg1, arg2, arg3]
    #args = filename

    Logger('StartFile arguments: ' + str(args), getframeinfo(currentframe()))
    ce = None
    try:
        ce = subprocess.call(args)
    except OSError:
        tkinter.messagebox.showerror('StartFile did a Badddddd thing ' , \
         'Arguments: ' + str(args) + '\nReturn code: ' + str(ce))
        return
#------------------------------
if __name__ == '__main__':
    print('DougModules.py')
    print('Trace',MyTrace(getframeinfo(currentframe())))
    print('Search for notepad.exe',SearchPath('Notepad.exe'))

    Main = tkinter.Tk()
    Main.title('Doug module test')
    Main.minsize(250,300)
    Main.wm_iconname('Doug module')
    Main.option_add('*Dialog.msg.wrapLength', '20i')
    MyMessageBox(Title='This is a test')
    Main.mainloop()
    StartFile('Notepad.exe')
