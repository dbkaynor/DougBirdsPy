import sys
import os
import time
import platform
sys.path.append('auxfiles')
import tkinter
from tkinter import *
import tkinter.messagebox
import argparse
import logging
from ToolTip import ToolTip
import __main__ as main
from inspect import currentframe, getframeinfo

Main = tkinter.Tk()
#------------------------------
class Vars():
    StartUpDirectoryVar = StringVar()
    AuxDirectoryVar = StringVar()
    HelpFileVar = StringVar()
    LogFileNameVar = StringVar()
    BirdFileNameVar = StringVar()
    StatusVar = StringVar()

    BirdInfoList = []

    SizeVar = IntVar()
    BillShapeVar = IntVar()
    ColorVar = IntVar()
    HeadColorVar = IntVar()
    BillColorVar = IntVar()
    BackColorVar = IntVar()
#------------------------------
#LogLevel 0 is log everything
def Logger(LogMessage, FrameInfoDict, LogLevel = 0, ShowInStatus = False, PrintToCommandLine = False):
    MyLogger = logging.getLogger(Vars.LogFileNameVar.get())
    mystr = LogMessage + ' Module:' + str(FrameInfoDict[0]) +  '  Line:' + str(FrameInfoDict[1])
    MyLogger.debug(mystr)
    if PrintToCommandLine: print(mystr)
    if ShowInStatus: Vars.StatusVar.set(LogMessage)
'''
debug, info,warning, error, critical, log, exception
'''
#------------------------------
#Initialize the program
def StartUpStuff():
    #-- Lots of startup stuff ------------------------------------
    Vars.StartUpDirectoryVar.set(os.getcwd())
    Vars.AuxDirectoryVar.set(Vars.StartUpDirectoryVar.get() + '\\auxfiles')
    Vars.HelpFileVar.set(Vars.AuxDirectoryVar.get() + '\\PyBirds.hlp')

    SetUpLogger()
    ParseCommandLine()
    Vars.BirdFileNameVar.set('BirdData.txt')

    try:
        f = open(Vars.BirdFileNameVar.get(), 'r')
    except IOError:
        tkinter.tkessagebox.showerror('Bird file name', 'Requested file does not exit.\n>>' + Vars.BirdFileNameVar.get() + '<<')
        return

    Vars.BirdInfoList = f.readlines()
    f.close()

    Logger(str(os.environ.get('OS')), getframeinfo(currentframe()))
    Logger(str(platform.uname()), getframeinfo(currentframe()))
    Logger('Number of argument(s): ' + str(len(sys.argv)), getframeinfo(currentframe()), True)
    Logger('Argument List: ' + str(sys.argv), getframeinfo(currentframe()))

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
#Setup the logger
def SetUpLogger():
    Vars.LogFileNameVar.set(Vars.StartUpDirectoryVar.get() + os.sep + 'PyBirds.log')
    logger = logging.getLogger(Vars.LogFileNameVar.get())
    #logger.setLevel(logging.DEBUG)
    if os.path.exists(Vars.LogFileNameVar.get()): os.remove(Vars.LogFileNameVar.get())
    logger = logging.basicConfig(level=logging.DEBUG,
                filename=Vars.LogFileNameVar.get(),
                format='%(asctime)s %(levelname)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%BirdInfoListS')
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
        tkMessageBox.showerror('StartFile did a Badddddd thing ' , \
         'Arguments: ' + str(args) + '\nReturn code: ' + str(ce))
        return
#------------------------------
#Some debug stuff
def About():
    Logger('About ' + main.Vars.StartUpDirectoryVar.get(), getframeinfo(currentframe()))
    tkinter.messagebox.showinfo('About',  main.Vars.StartUpDirectoryVar.get() +
      '\n' + Main.geometry() +
      '\n' + str(Main.winfo_screenwidth()) + 'x' +  str(Main.winfo_screenheight()) +
      '\n' + 'Python version: ' + platform.python_version())
#------------------------------
#The help file (someday)
def Help():
    Logger('Help ' + main.Vars.StartUpDirectoryVar.get(), getframeinfo(currentframe()))

    try:
        f = open(Vars.HelpFileVar.get(), 'r')
    except IOError:
        tkinter.messagebox.showerror('Help file error', 'Requested file does not exist.\n>>' + Vars.HelpFileVar.get() + '<<')
        return
    lines = f.readlines()
    f.close()
    helpdata = 'Not implemented yet\n'
    for l in lines:
        helpdata = helpdata + l

    tkinter.messagebox.showinfo('Help', helpdata)
#------------------------------
#Show the log in the defined system editor
def ViewLog():
    Logger('View log  ', getframeinfo(currentframe()))
    print('ViewLog',Vars.LogFileName.get())
    StartFile(Vars.SystemEditorVar.get(), Vars.LogFileName.get())
#------------------------------
#Build all the gui and start the program

menubar = Menu(Main)
Main['menu'] = menubar
SizeMenu = Menu(menubar)
menubar.add_cascade(menu=SizeMenu, label='Size')
SizeMenu.add_radiobutton(label='Not set', variable=Vars.SizeVar, value=0)
SizeMenu.add_radiobutton(label='Huge (Like Swan 30"+)', variable=Vars.SizeVar, value=1)
SizeMenu.add_radiobutton(label='Very large (Like Double-crested Cormorant 25"-34")', variable=Vars.SizeVar, value=2)
SizeMenu.add_radiobutton(label='Large (Like Hawk 21"-29")', variable=Vars.SizeVar, value=3)
SizeMenu.add_radiobutton(label='Medium large (Peregrine Falcon 17"-24")', variable=Vars.SizeVar, value=4)
SizeMenu.add_radiobutton(label='Medium (Like crow 15"-20")', variable=Vars.SizeVar, value=5)
SizeMenu.add_radiobutton(label='Medium small (Like flicker 11-17)', variable=Vars.SizeVar, value=6)
SizeMenu.add_radiobutton(label='Small (Like Robin 7"-14")', variable=Vars.SizeVar, value=7)
SizeMenu.add_radiobutton(label='Very small (Like Sparrow 5"-9")', variable=Vars.SizeVar, value=8)
SizeMenu.add_radiobutton(label='Tiny (Like Hummingbird <5)', variable=Vars.SizeVar, value=9)

BillMenu = Menu(menubar)
menubar.add_cascade(menu=BillMenu, label='Bill shape')
BillMenu.add_radiobutton(label='Not set', variable=Vars.BillShapeVar, value=0)
BillMenu.add_radiobutton(label='Thin', variable=Vars.BillShapeVar, value=1)
BillMenu.add_radiobutton(label='Short pointed', variable=Vars.BillShapeVar, value=2)
BillMenu.add_radiobutton(label='Long pointed', variable=Vars.BillShapeVar, value=3)
BillMenu.add_radiobutton(label='Conical', variable=Vars.BillShapeVar, value=4)
BillMenu.add_radiobutton(label='Duck', variable=Vars.BillShapeVar, value=5)
BillMenu.add_radiobutton(label='Tube nosed', variable=Vars.BillShapeVar, value=6)
BillMenu.add_radiobutton(label='Hooked', variable=Vars.BillShapeVar, value=7)
BillMenu.add_radiobutton(label='Huge', variable=Vars.BillShapeVar, value=8)
BillMenu.add_radiobutton(label='Straight down curved', variable=Vars.BillShapeVar, value=9)
BillMenu.add_radiobutton(label='Wedge down curve', variable=Vars.BillShapeVar, value=10)
BillMenu.add_radiobutton(label='Triangular', variable=Vars.BillShapeVar, value=11)
BillMenu.add_radiobutton(label='Knobbed', variable=Vars.BillShapeVar, value=12)
BillMenu.add_radiobutton(label='Spooned', variable=Vars.BillShapeVar, value=13)
BillMenu.add_radiobutton(label='Straight point tip', variable=Vars.BillShapeVar, value=14)
BillMenu.add_radiobutton(label='Very thick', variable=Vars.BillShapeVar, value=15)
BillMenu.add_radiobutton(label='Short hooked', variable=Vars.BillShapeVar, value=16)
BillMenu.add_radiobutton(label='Crossed bill', variable=Vars.BillShapeVar, value=17)

OtherMenu = Menu(menubar)
menubar.add_cascade(menu=OtherMenu, label='Other')
OtherMenu.add_radiobutton(label='---- Bill color ----')
OtherMenu.add_radiobutton(label='Not set', variable=Vars.BillColorVar, value=0)
OtherMenu.add_radiobutton(label='Yellow bill', variable=Vars.BillColorVar, value=1)
OtherMenu.add_radiobutton(label='Orange bill', variable=Vars.BillColorVar, value=2)
OtherMenu.add_radiobutton(label='---- Head color ---- ')
OtherMenu.add_radiobutton(label='Not set', variable=Vars.HeadColorVar, value=0)
OtherMenu.add_radiobutton(label='White', variable=Vars.HeadColorVar, value=1)
OtherMenu.add_radiobutton(label='Dark brown', variable=Vars.HeadColorVar, value=2)
OtherMenu.add_radiobutton(label='Yellow', variable=Vars.HeadColorVar, value=3)
OtherMenu.add_radiobutton(label='Stripped', variable=Vars.HeadColorVar, value=4)
OtherMenu.add_radiobutton(label='Mottled', variable=Vars.HeadColorVar, value=5)
OtherMenu.add_radiobutton(label='---- Back color ----')
OtherMenu.add_radiobutton(label='Not set', variable=Vars.BackColorVar, value=0)
OtherMenu.add_radiobutton(label='White', variable=Vars.BackColorVar, value=1)
OtherMenu.add_radiobutton(label='Black', variable=Vars.BackColorVar, value=2)
OtherMenu.add_radiobutton(label='Gray', variable=Vars.BackColorVar, value=3)
OtherMenu.add_radiobutton(label='Brown', variable=Vars.BackColorVar, value=4)
OtherMenu.add_radiobutton(label='Blue', variable=Vars.BackColorVar, value=5)
OtherMenu.add_radiobutton(label='Mottled Black/White', variable=Vars.BackColorVar, value=6)
OtherMenu.add_radiobutton(label='Mottled Brown/Gray', variable=Vars.BackColorVar, value=7)

HelpMenu = Menu(menubar)
menubar.add_cascade(menu=HelpMenu, label='Help')
HelpMenu.add_command(label='About', command=About)
HelpMenu.add_command(label='Help', command=Help)

def Search(Section,value):
    Start = False
    count = 0
    for Line in Vars.BirdInfoList:
        count += 1
        Line = Line.strip()
        if len(Line.strip()) == 0 : Start = False
        if Line.find(Section.strip()) >= 0:
            Start = True
        if Start:
            if Line.find(str(value)) == 0:
                return "%s : %s" % (Section.strip(),Line.strip())

def Doit():
    ResultsListbox.insert(END, Search('SizeVar', Vars.SizeVar.get()))
    ResultsListbox.insert(END, Search('BillShapeVar', Vars.BillShapeVar.get()))
    ResultsListbox.insert(END, Search('BillColorVar', Vars.BillColorVar.get()))
    ResultsListbox.insert(END, Search('HeadColorVar', Vars.HeadColorVar.get()))
    ResultsListbox.insert(END, Search('BackColorVar', Vars.BackColorVar.get()))

def ClearAll():
    ResultsListbox.delete(0,END)
    Vars.SizeVar.set(0)
    Vars.BillShapeVar.set(0)
    Vars.ColorVar.set(0)
    Vars.HeadColorVar.set(0)
    Vars.BillColorVar.set(0)
    Vars.BackColorVar.set(0)

#--------Results display--------
Statuslabel = Label(Main, textvariable=Vars.StatusVar, relief=GROOVE)
Statuslabel.pack(side=TOP, expand=TRUE, fill=X)

yScroll = Scrollbar(Main, orient=VERTICAL)
yScroll.pack(side=RIGHT, fill=Y, expand=TRUE)
xScroll = Scrollbar(Main, orient=HORIZONTAL)
xScroll.pack(side=BOTTOM, fill=X, expand=TRUE)

ResultsListbox = Listbox(Main, width=50, yscrollcommand=yScroll.set, xscrollcommand=xScroll.set)
ResultsListbox.pack(side=TOP, fill=BOTH, expand=TRUE, padx=2, pady=1)
ToolTip(ResultsListbox,'Saved list of source files')
yScroll.config(command=ResultsListbox.yview)
xScroll.config(command=ResultsListbox.xview)
#lambda: f.read(block_size)
Button(Main, text='Do it', width=12, command=Doit).pack(side=LEFT)
Button(Main, text='Clear results', width=12, command=ClearAll).pack(side=LEFT)
#------------------------------

StartUpStuff()
#------------------------------
Vars.LogFileNameVar.set(Vars.StartUpDirectoryVar.get() + os.sep + 'PyCopyMoveTk.log')
#if os.path.exists(Vars.LogFileName.get()): os.remove(Vars.LogFileName.get())
MyLogger = logging.getLogger(Vars.LogFileNameVar.get())

MyLogger = logging.basicConfig(level=logging.DEBUG,
        filename=Vars.LogFileNameVar.get(),
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
#------------------------------
Vars.StatusVar.set('Waiting')
Main.minsize(200,200)
Main.title('PyBirdsTk')
Main.option_add('*Font', 'courier 10')
Main.wm_iconname('PyBirdsTk')
Main.mainloop()
