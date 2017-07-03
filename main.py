# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 19:27:32 2017

@author: Abhishek
"""
# importing of the neccessary files
import sys
import tkinter as tk
from tkinter import *
import tkinter.filedialog as tkFileDialog
import os




# color variables


rootBg = '#eef'
btnBg = '#eef'
actLbl = '#0e2e33'
dirlbl = '#eee'
dirfont = '#333'
editorBgColor = '#002233'
fontColor = 'white'
insertColor = '#dec'
labelBgColor = '#002233'
fontLabel = 'white'
closeBg = '#00223A'
closeActive = '#002244'
selectBg = '#002211'
#variable
filesHid = 0
currentEditor = 0
dirshowed = 0

# Initiation


root=Tk("Text Editor")
root.configure(background=rootBg)
root.geometry('800x500')
root.update()


rootHeight = root.winfo_screenheight()
rootWidth = root.winfo_screenwidth()



#image VAriables

folderPng = PhotoImage(file="img/folder.gif")
filePng   = PhotoImage(file="img/file.gif")
addPng    = PhotoImage(file="img/add.png")
savePng   = PhotoImage(file="img/save.png")
openPng   = PhotoImage(file="img/open.png")
#File vars

currentDir  = '../'



# page
class ScrollFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    
    scrollwidth =10
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=TRUE)
        hscrollbar = Scrollbar(self, orient=HORIZONTAL)
        hscrollbar.pack(fill=X, side=BOTTOM, expand=TRUE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set,xscrollcommand=hscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)
        hscrollbar.config(command=canvas.xview)
        self.canvas = canvas
        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

     
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            
        interior.bind('<Configure>', _configure_interior)

        


class WebText(Text):
    def __init__(self,Editor,i):
        self.id = i
        self.frame = Frame(Editor) 
        self.frame.pack(fill=BOTH, expand=YES,side=LEFT)
        self.text=Text(self.frame,wrap=NONE,padx=20,pady=20)
        self.text.configure(background=actLbl,fg=fontColor,height = rootHeight ,width=rootWidth,insertbackground=insertColor,bd=0,selectbackground = selectBg)
        self.scrolly = Scrollbar(self.frame)
        self.scrolly.pack(fill=Y,side=RIGHT,expand = YES)
        self.scrollx = Scrollbar(self.frame,orient=HORIZONTAL)
        self.scrollx.pack(fill=X,side=BOTTOM,expand = YES)
        self.text.pack(fill=BOTH, expand=YES,side=LEFT)
        self.scrolly.config(command=self.text.yview)
        self.scrollx.config(command=self.text.xview)
        self.text.config(yscrollcommand=self.scrolly.set,xscrollcommand=self.scrollx.set)
        
        def tab(arg):
            print("tab pressed")
            self.text.insert(tk.INSERT, " " * 4 )
            return 'break'
        
        self.text.bind("<Tab>", tab)

        
class WebLabel(Button):
    def __init__(self,FilesPane,i,name):
        self.id = i
        self.frame = Frame(FilesPane)
        self.frame.pack(fill=BOTH, expand=NO,side=LEFT)
        self.button=Button(self.frame,text=name,padx=20,height=2,width=8,background=labelBgColor,activebackground=labelBgColor,activeforeground=fontColor,fg=fontLabel,relief=SUNKEN,bd=0,command=lambda: tabClicked(self.id))
        self.button.pack(fill=BOTH, expand=NO,side=LEFT)
        self.close=Button(self.frame,text='x',padx=10,height=2,background=closeBg,activebackground=closeActive,activeforeground=fontLabel,fg=fontLabel,relief=GROOVE,bd=0,command=lambda: tabClose(self.id))
        self.close.pack(fill=BOTH, expand=NO,side=LEFT)
        
class upLabel(Button):
    def __init__(self,FilesPane,i,txt,name):
        self.id = i
        self.path = txt
        self.image = folderPng
        self.frame = Frame(FilesPane)
        self.frame.pack(fill=BOTH,expand=NO,side=TOP)
        self.button=Button(self.frame,image=self.image,pady=2,width=20,height=1,background=dirlbl,activebackground=dirlbl,activeforeground=dirfont,fg=dirfont,relief=SUNKEN,bd=0,anchor=N,command = lambda : openFolder('../'))
        self.button.pack(fill=BOTH, expand=NO,side=LEFT)
        self.innerframe = Frame(self.frame)
        self.innerframe.pack(fill=BOTH, expand=NO,side=TOP)
        self.label=Button(self.innerframe,text=name,pady=1,anchor=NW,height=1,background=dirlbl,activebackground=dirlbl,activeforeground=dirfont,fg=dirfont,relief=SUNKEN,bd=0)
        self.label.pack(fill=BOTH, expand=NO,side=TOP)
        
class DirLabel(Button):
    def __init__(self,FilesPane,i,txt,name):
        self.id = i
        self.path = txt+'/'+name
        self.image = folderPng
        self.expanded = 0
        self.index=[]
        self.frame = Frame(FilesPane)
        self.frame.pack(fill=BOTH,expand=NO,side=TOP)
        self.button=Button(self.frame,image=self.image,pady=2,width=20,height=1,background=dirlbl,activebackground=dirlbl,activeforeground=dirfont,fg=dirfont,relief=SUNKEN,bd=0,command=lambda :toggleExpand(self),anchor=N)
        self.button.pack(fill=BOTH, expand=NO,side=LEFT)
        self.innerframe = Frame(self.frame)
        self.innerframe.pack(fill=BOTH, expand=NO,side=TOP)
        self.label=Button(self.innerframe,text=name,pady=1,anchor=NW,height=1,background=dirlbl,activebackground=dirlbl,activeforeground=dirfont,fg=dirfont,relief=SUNKEN,bd=0)
        self.label.pack(fill=BOTH, expand=NO,side=TOP)
    
class FileLabel(Button):
    def __init__(self,FilesPane,i,txt,name):
        self.id = i
        self.path = txt
        self.name = name
        self.image = filePng
        self.frame = Frame(FilesPane)
        self.frame.pack(fill=BOTH,expand=NO,side=TOP)
        self.button=Button(self.frame,image=self.image,pady=2,width=20,height=1,background=dirlbl,activebackground=dirlbl,activeforeground=dirfont,fg=dirfont,relief=SUNKEN,bd=0,command = lambda: openPage(self))
        self.button.pack(fill=BOTH, expand=NO,side=LEFT)
        self.label=Button(self.frame,text=name,pady=1,anchor=NW,height=1,background=dirlbl,activebackground=dirlbl,activeforeground=dirfont,fg=dirfont,relief=SUNKEN,bd=0)
        self.label.pack(fill=BOTH, expand=NO,side=TOP)
        
# add page function

def addNewPage():   
    startLabel = WebLabel(FilesPane,len(LabelList),'new')
    LabelList.append(startLabel)
    start=WebText(EditorPane,len(EditList))
    EditList.append(start)
    tabClicked(len(EditList)-1)

def openPage(FL):
    txt = FL.path+'/'+FL.name
    file = open(txt,'r')
    content = file.read()
    file.close()
    startLabel = WebLabel(FilesPane,len(LabelList),FL.name)
    LabelList.append(startLabel)
    start=WebText(EditorPane,len(EditList))
    start.text.insert(END, content)
    EditList.append(start)
    tabClicked(len(EditList)-1)
    
def savePage():
    if (len(EditList)!=0):
        text = EditList[currentEditor].text
        t = text.get("1.0", "end-1c")
        savelocation=tkFileDialog.asksaveasfilename()
        file1=open(savelocation, "w+")
        file1.write(t)
        file1.close()

def openFolder(txt=NONE):
    global dirshowed
    global currentDir
    global WDirTree
    if (txt == '../'):
        path = os.path.abspath(currentDir+'/../')
        dirname = path
    else:
        path = os.path.abspath(currentDir)
        dirname = tkFileDialog.askdirectory(parent=root,initialdir=path,title='Please select a directory')
    
    currentDir = dirname
    
    for item in WDirTree:
        item.frame.pack_forget()
    del WDirTree[:]

    path = currentDir
    WDirTree = [upLabel(directory.interior,0,path,'../')]
    dirList = os.listdir(path)
    
    for item in dirList:
        newpath = path + '/' + item
        if (not os.path.isfile(newpath)):
            WDirTree.append(DirLabel(directory.interior,len(WDirTree),path,item))
    
            
    for item in dirList:
        newpath = path + '/' + item
        if (os.path.isfile(newpath)):
            WDirTree.append(FileLabel(directory.interior,len(WDirTree),path,item))
            
    if (dirshowed == 0):
        dirshowed = 1
        showDirs()
    else:
        pass
            
    

    
    
# tab clicked

def tabClicked(id):
    for item in EditList:
        if item.id != id:
            item.frame.pack_forget()
        else:
            item.frame.pack(fill=BOTH, expand=YES)
            
    for item in LabelList:
        if item.id != id:
            item.button.configure(background=labelBgColor)
            item.close.configure(background=closeBg) 
        else:
            item.button.configure(background=actLbl) 
            item.close.configure(background=actLbl)
             
    global currentEditor
    currentEditor = id
    
     
def tabClose(id):
    EditList[id].frame.pack_forget()
    LabelList[id].frame.pack_forget()
    del EditList[id]
    del LabelList[id]
    
        
    i = 0
    for item in EditList:
        item.id = i
        i+=1
        
    i = 0
    for item in LabelList:
        item.id = i
        i+=1
        
    
    global currentEditor
    print(currentEditor,id)    
    if ((id != 0) and (currentEditor==id)):
        tabClicked(id-1)
    elif ((id ==0) and (currentEditor==id)):
        tabClicked(id)
        currentEditor = currentEditor-1
    else:
        currentEditor = currentEditor-1
   
        
def showDirs():
    global filesHid
    global dirshowed
    dir.pack_forget()
    print(filesHid)
    if (filesHid == 0):
        dir.pack_forget()
        Folders.configure(width = 150)
        closedir.pack(fill = X,expand=NO,side=TOP)
        directory.pack(fill=Y, expand=NO,side=TOP)
        filesHid = 1
        dirshowed = 1
        
   
    else:
        directory.pack_forget()
        Folders.configure(width = 30)
        filesHid = 0
        dir.pack(side=TOP)
        closedir.pack_forget()
        dirshowed = 0
        
        
def toggleExpand(DL):
    path = DL.path
    id   = DL.id
    List = os.listdir(path)
    if (DL.expanded == 0):
        for item in List:
            newpath = path + '/' + item
            if (not os.path.isfile(newpath)):
                DL.index.append(DirLabel(DL.innerframe,len(DL.index),path,item))
        for item in List:
            newpath = path + '/' + item
            if (os.path.isfile(newpath)):
                DL.index.append(FileLabel(DL.innerframe,len(DL.index),path,item)) 
        DL.expanded = 1
    else:
        for item in DL.index:
            item.frame.pack_forget()
        del DL.index[:]
        DL.expanded = 0
        return 0
    

#code



Panelone = PanedWindow(root,height = int(rootHeight/25),bg = rootBg,bd=0)
Panelone.pack(fill=BOTH, expand=YES,side=TOP)



Paneltwo = PanedWindow(root,height = int(24*rootHeight/25),bd=0)
Paneltwo.pack(fill=BOTH, expand=YES,side=TOP)
Folders = PanedWindow(Paneltwo,bd=2,width=150,height=24*rootHeight/25)
Folders.pack(fill=BOTH, expand=YES,side=LEFT)
Editor = PanedWindow(Paneltwo,bd=0)
Editor.pack(fill=BOTH, expand=YES)

dir =  Button(Folders,image=folderPng,padx=10,pady=10,fg=fontColor,bd=0,command=showDirs,relief=SUNKEN)
dir.pack(fill = X,side=TOP)




directory = ScrollFrame(Folders,width=150,bg=dirlbl,bd=0,height = 24*rootHeight/25)
directory.canvas.configure(height = 24*rootHeight/25)
directory.pack(fill=Y, expand=YES,side=TOP)
Folders.pack_propagate(0)



path = '../'
WDirTree = [upLabel(directory.interior,0,path,path)]
dirList = os.listdir(path)
for item in dirList:
    if (not os.path.isfile(item)):
        WDirTree.append(DirLabel(directory.interior,len(WDirTree),path,item))

        
for item in dirList:
    if (os.path.isfile(item)):
        WDirTree.append(FileLabel(directory,len(WDirTree),path,item))
        
directory.pack_forget()
Folders.configure(width = 30)

FilesPane = PanedWindow(Editor ,bg=insertColor,bd=0)
FilesPane.pack(fill=BOTH, expand=YES,side=TOP)
EditorPane = PanedWindow(Editor ,bg=insertColor,bd=0) 
EditorPane.pack(fill=BOTH, expand=YES,side=TOP)




image2 = PhotoImage(file="img/close.gif")
closedir = Button(Folders,image=image2,padx=2,pady=2,fg=fontColor,bd=0,height=30,command=showDirs,relief=SUNKEN)
closedir.pack_forget()



# Buttons Operations
openLabel= Button(Panelone,image=openPng,width=40,height=35,background=btnBg,fg=fontColor,relief=FLAT,bd=0,command=openFolder)
openLabel.pack(side=LEFT)
addLabel = Button(Panelone,image=addPng,width=40,height=35,background=btnBg,fg=fontColor,relief=FLAT,bd=0,command=addNewPage)
addLabel.pack(side=LEFT)
saveLabel = Button(Panelone,image=savePng,width=40,height=35,background=btnBg,fg=fontColor,relief=FLAT,bd=0,command=savePage)
saveLabel.pack(side=LEFT)

LabelList = []
EditList = []


startLabel = WebLabel(FilesPane,len(LabelList),'new')
LabelList.append(startLabel)
start=WebText(EditorPane,len(EditList))
EditList.append(start)
startLabel.button.configure(background=actLbl) 
startLabel.close.configure(background=actLbl)

showDirs()

root.mainloop()

