# -*- coding: UTF-8 -*-
import os, shutil, getpass, Tkinter, ttk, tkMessageBox
from P4 import P4
from PIL import Image, ImageTk
yourName = getpass.getuser()

def p4Clients():
    p4 = P4()
    p4.port = "proxy:1667"
    p4.user = yourName
    p4.connect()
    p4clientinfo = p4.run('clients', '--me')  # 获得所有本机的workspace
    p4ArtSource_client =[]
    p4Engine_client = []
    p4Release_client = []
    for i in p4clientinfo:
        if i['client'].lower() == yourName+ '_artsource':
            p4ArtSource_client.append(i['client'])
            p4ArtSource_client.append(i['Root'])
        elif i['client'].lower() == yourName + '_main':
            p4Engine_client.append(i['client'])          #sirui.chen的artsource
            p4Engine_client.append(i['Root'])
        elif i['client'].lower() == yourName+ '_fortnite_engine':
            p4Engine_client.append(i['client'])
            p4Engine_client.append(i['Root'])
        elif i['client'].lower() == yourName+ '_fortnite_release':      # Release有版号 所以只爬前半部
            p4Release_client.append(i['client'])
            p4Release_client.append(i['Root'])
    p4.disconnect()
    return (p4ArtSource_client, p4Engine_client, p4Release_client)
# (['Yifei.Zhang_ArtSource', 'd:\\Build'], ['Yifei.Zhang_Fortnite_Engine', 'd:\\Builds_Fortnite_Engine'], ['Yifei.Zhang_Fortnite_Release', 'd:\\Builds_Fortnite_Release'])

def delcreate(pyfile, Folder):
    if os.path.exists(Folder) == False:
        os.makedirs(Folder)
    if os.path.isfile(Folder + '\\' + pyfile) == True:
        os.remove(Folder + '\\' + pyfile)
    shutil.copy(pyfile, Folder)
    return (Folder+'\\'+pyfile+'\n')

def delete(pyfile, Folder):
    if os.path.isfile(Folder+'\\'+pyfile) == True:
        os.remove(Folder + '\\' + pyfile)
    return (Folder+'\\'+pyfile+'\n')

EGC_Plugins = 'D:\\EGC_Plugins'
Maxscriptfolder = 'C:\\Program Files\\Autodesk\\3ds Max 2018\\scripts\\Startup'
MayaMelfolder = 'C:\\Users\\%s\\Documents\\maya\\2018\\prefs\\shelves' % yourName
MarmosetPlugFolder = 'C:\\Users\\%s\\AppData\\Local\\Marmoset Toolbag 3\\plugins' % yourName
Bakefolder = p4Clients()[1][1] + '\\FortniteGame\\Content\\EGC_Bake'

# Create GUI
win = Tkinter.Tk()
win.iconbitmap('01.ico')
win.title('EGC_PluginSetup')
win.resizable(0, 0)                                       #cant resize UI
winlabel1 = Tkinter.Label(win, text=u'选择用户')
MAYAICON = ImageTk.PhotoImage(Image.open('maya.ico'))
MAXICON = ImageTk.PhotoImage(Image.open('icon_main.ico'))
# winlistbox = Tkinter.Listbox(win, height=len(software))
# for i in software:
#     winlistbox.insert(0, i)
def selmax():
    try:
        Marmo_Setuped = delcreate('EGC_Bake_AutoGroup.py', MarmosetPlugFolder)
        software_Setuped = delcreate('EGC_ExportFBX.ms', Maxscriptfolder)
        Engine_Setuped = delcreate('EGC_Auto_Export_MAX.uasset', Bakefolder)
        EGC_Setuped = delcreate('EGC_AutoImEx_MAX.py', EGC_Plugins)
        tkMessageBox.showinfo(u'安装成功',
                              u'安装成功\n%s\n%s\n%s\n%s'%(EGC_Setuped, software_Setuped, Marmo_Setuped, Engine_Setuped))
    except Exception as e:
        tkMessageBox.showerror(u'注意', u'请关闭MAX,MAYA和引擎\n%s' % e)

def selmaya():
    try:
        Marmo_Setuped = delcreate('EGC_Bake_AutoGroup.py', MarmosetPlugFolder)
        software_Setuped = delcreate('shelf_EGC_ExportFBX.mel', MayaMelfolder)
        Engine_Setuped = delcreate('EGC_Auto_Export_MAYA.uasset', Bakefolder)
        EGC_Setuped = delcreate('EGC_AutoImEx_MAYA.py', EGC_Plugins)
        tkMessageBox.showinfo(u'安装成功',
                              u'安装成功\n%s\n%s\n%s\n%s' % (EGC_Setuped, software_Setuped, Marmo_Setuped, Engine_Setuped))
    except Exception as e:
        tkMessageBox.showerror(u'注意', u'请关闭MAX,MAYA和引擎\n%s' % e)

def unsel():
    try:
        delete('EGC_Bake_AutoGroup.py', MarmosetPlugFolder)
        delete('EGC_ExportFBX.ms', Maxscriptfolder)
        delete('EGC_Auto_Export_MAX.uasset', Bakefolder)
        delete('EGC_AutoImEx_MAX.py', EGC_Plugins)
        delete('shelf_EGC_ExportFBX.mel', MayaMelfolder)
        delete('EGC_Auto_Export_MAYA.uasset', Bakefolder)
        delete('EGC_AutoImEx_MAYA.py', EGC_Plugins)
        tkMessageBox.showinfo(u'卸载成功', u'卸载成功')
    except Exception as e:
        tkMessageBox.showerror(u'注意', u'请关闭MAX,MAYA和引擎\n%s' % e)

maxbutton = ttk.Button(win, image=MAXICON, command=selmax)
mayabutton =  ttk.Button(win, image=MAYAICON, command=selmaya)
unsetupbutton = ttk.Button(win, text=u'卸载', width=80,command=unsel)

winlabel1.grid(row=0,columnspan=2)
# winlistbox.grid(row=0, column=1,sticky='W')
maxbutton.grid(row=1, column=0)
mayabutton.grid(row=1, column=1)
unsetupbutton.grid(row=2, columnspan=2)

win.mainloop()