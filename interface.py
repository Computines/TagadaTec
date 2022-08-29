from asyncio import events
from distutils.cmd import Command
from tkinter import *
from tkinter import ttk
from os import *
from turtle import bgcolor, right
from winreg import REG_DWORD_BIG_ENDIAN
import tkinter.font as tkfont

fnt=("Arial",10)
SPACING     =   5
WIDTH       =   1200
HEIGHT      =   700
TOOLBWIDTH  =   50
MENUHEIGHT  =   30
FOLDERWIDTH =   200
NUMBERSWIDTH=   50
BUTTONSEP   =   0
BUTTONGRID  =   TOOLBWIDTH+BUTTONSEP
BUTTONSTART =   MENUHEIGHT+BUTTONSEP
BACKGROUND  =   "#1e1e1e"
TOOLBAR     =   "#333333"
FOLDERBAR   =   "#252526"
MENUBAR     =   "#3c3c3c"
LIGHTERBG   =   "#505050"
REDBG       =   "#d61425"


class Interface:
    def __init__(self):
        ########################## MAIN PANEL ###########################
        
        
        self.ventana=Tk()
        self.ventana.title("Computines Compiler")
        self.ventana.minsize(WIDTH,HEIGHT) 
        self.ventana.resizable(width=NO, height=NO)
        self.ventana.overrideredirect(True)

        def cargar_img(nombre):
            ruta=path.join("assets",nombre) #crea acceso a la ruta assets dentro de la carpeta del programa
            img=PhotoImage(file=ruta) #importa la imagen
            return img #retorna la imagen 

        mainPanel = Canvas(self.ventana, background=BACKGROUND, width=WIDTH-TOOLBWIDTH-FOLDERWIDTH, height=HEIGHT-MENUHEIGHT, highlightthickness=0)
        mainPanel.place(x=TOOLBWIDTH+FOLDERWIDTH+NUMBERSWIDTH,y=MENUHEIGHT)

        folderbar = Canvas(self.ventana, background=FOLDERBAR, width=FOLDERWIDTH, height=HEIGHT-MENUHEIGHT, highlightthickness=0)
        folderbar.place(x=TOOLBWIDTH,y=MENUHEIGHT)

        numBar = Canvas(self.ventana, background=BACKGROUND, width=NUMBERSWIDTH, height=HEIGHT-MENUHEIGHT, highlightthickness=0)
        numBar.place(x=TOOLBWIDTH+FOLDERWIDTH,y=MENUHEIGHT) 

        menubar = Canvas(self.ventana, background=MENUBAR, width=WIDTH, height=MENUHEIGHT, highlightthickness=0)
        menubar.place(x=0,y=0) 
        
        toolbar = Canvas(self.ventana, background=TOOLBAR, width=TOOLBWIDTH, height=HEIGHT-MENUHEIGHT, highlightthickness=0)
        toolbar.place(x=0,y=MENUHEIGHT)

        def get_pos(event):
            xwin = self.ventana.winfo_x()
            ywin = self.ventana.winfo_y()
            startx = event.x_root
            starty = event.y_root

            ywin = ywin - starty
            xwin = xwin - startx

            def move_window(event):
                self.ventana.geometry((str(WIDTH)+"x"+str(HEIGHT)) + '+{0}+{1}'.format(event.x_root + xwin, event.y_root + ywin))
            startx = event.x_root
            starty = event.y_root
            menubar.bind('<B1-Motion>', move_window)

        menubar.bind('<Button-1>', get_pos)

        openedFile=Label(self.ventana, font=fnt, fg="#dedede", bg=MENUBAR, text="Compilador Computines")
        openedFile.place(x=WIDTH/2,y=TOOLBWIDTH/4,anchor="center")

        ########################## TREE DIRECTORY ###########################
        yscrollTree = Scrollbar(folderbar, orient="vertical")
        xscrollTree = Scrollbar(folderbar, orient="horizontal")
        yscrollTree.place(x=FOLDERWIDTH, y=0, anchor=NE, height=HEIGHT-MENUHEIGHT-15)
        xscrollTree.place(x=0, y=HEIGHT-MENUHEIGHT, anchor=SW, width=FOLDERWIDTH)

        directory='/Documentos/TEC/'
        treeFrame=Frame(folderbar, bg=FOLDERBAR, height=HEIGHT-MENUHEIGHT-15, width=FOLDERWIDTH-15)
        treeStyle = ttk.Style(treeFrame)
        treeStyle.theme_use("alt")
        treeStyle.configure("Treeview", background=FOLDERBAR, foreground="#dedede", fieldbackground=FOLDERBAR)
        treeStyle.configure("Treeview", highlightthickness=0, bd=0, font=('Arial', 10))
        treeStyle.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        treeStyle.map("Treeview", background = [('selected', LIGHTERBG)])
        def fixed_map(option):
            return [elm for elm in treeStyle.map('Treeview', query_opt=option) if
            elm[:2] != ('!disabled', '!selected')]
        treeStyle.map('Treeview', 
            foreground=fixed_map('foreground'),
            background=fixed_map('background'))
        folderTree=ttk.Treeview(treeFrame, show='tree', yscrollcommand=yscrollTree.set,  xscrollcommand=xscrollTree.set)
        folderTree.heading('#0',text='directory:'+ directory,anchor='w')
        folderTree.heading('#0', text='Dir：'+directory, anchor='w')
        directory=path.abspath(directory)
        node=folderTree.insert('','end', text=path, open=True)
        def traverse_dir(parent, directory):
            for d in listdir(directory):
                full_path=path.join(directory,d)
                isdir = path.isdir(full_path)
                id=folderTree.insert(parent,'end',text=d,open=False)
                if isdir:
                    traverse_dir(id,full_path)
        traverse_dir(node,directory)

        xscrollTree.config(command=folderTree.xview)
        yscrollTree.config(command=folderTree.yview)

        folderTree.place(x=0, y=0, height=HEIGHT-MENUHEIGHT-15, width=FOLDERWIDTH-15)
        treeFrame.place(x=0, y=0)

        ########################## BUTTON FUNCTIONS ###########################

        def close(e):    
            self.ventana.destroy()

        def on_enterExit(e):
            exitButton['background'] = REDBG

        def on_leaveExit(e):
            exitButton['background'] = MENUBAR

        def on_enterOpen(e):
            openButton['background'] = LIGHTERBG

        def on_leaveOpen(e):
            openButton['background'] = TOOLBAR

        def on_enterSave(e):
            saveButton['background'] = LIGHTERBG

        def on_leaveSave(e):
            saveButton['background'] = TOOLBAR

        def on_enterSaveAs(e):
            saveAsButton['background'] = LIGHTERBG

        def on_leaveSaveAs(e):
            saveAsButton['background'] = TOOLBAR

        def on_enterBuild(e):
            buildButton['background'] = LIGHTERBG

        def on_leaveBuild(e):
            buildButton['background'] = TOOLBAR

        def on_enterRun(e):
            runButton['background'] = LIGHTERBG

        def on_leaveRun(e):
            runButton['background'] = TOOLBAR

        ########################## BUTTONS ###########################

        exitImage = cargar_img("quitImage.png")
        exitButton = Button(self.ventana, image=exitImage, width=MENUHEIGHT, height=MENUHEIGHT-2, border=0, bg=MENUBAR)
        exitButton.place(x=WIDTH,y=0, anchor=NE)
        exitButton.bind("<Enter>", on_enterExit)
        exitButton.bind("<Leave>", on_leaveExit)
        exitButton.bind('<Button-1>', close)

        openImage = cargar_img("openImage.png")
        openButton = Button(toolbar, image=openImage, width=TOOLBWIDTH-2, height=TOOLBWIDTH, border=0, bg=TOOLBAR)
        openButton.place(x=0,y=0, anchor=NW)
        openButton.bind("<Enter>", on_enterOpen)
        openButton.bind("<Leave>", on_leaveOpen)

        saveImage = cargar_img("saveImage.png")
        saveButton = Button(toolbar, image=saveImage, width=TOOLBWIDTH-2, height=TOOLBWIDTH, border=0, bg=TOOLBAR)
        saveButton.place(x=0,y=1*BUTTONGRID, anchor=NW)
        saveButton.bind("<Enter>", on_enterSave)
        saveButton.bind("<Leave>", on_leaveSave)

        saveAsImage = cargar_img("saveAsImage.png")
        saveAsButton = Button(toolbar, image=saveAsImage, width=TOOLBWIDTH-2, height=TOOLBWIDTH, border=0, bg=TOOLBAR)
        saveAsButton.place(x=0,y=2*BUTTONGRID, anchor=NW)
        saveAsButton.bind("<Enter>", on_enterSaveAs)
        saveAsButton.bind("<Leave>", on_leaveSaveAs)

        buildImage = cargar_img("buildImage.png")
        buildButton = Button(toolbar, image=buildImage, width=TOOLBWIDTH-2, height=TOOLBWIDTH, border=0, bg=TOOLBAR)
        buildButton.place(x=0,y=3*BUTTONGRID, anchor=NW)
        buildButton.bind("<Enter>", on_enterBuild)
        buildButton.bind("<Leave>", on_leaveBuild)

        runImage = cargar_img("runImage.png")
        runButton = Button(toolbar, image=runImage, width=TOOLBWIDTH-2, height=TOOLBWIDTH, border=0, bg=TOOLBAR)
        runButton.place(x=0,y=4*BUTTONGRID, anchor=NW)
        runButton.bind("<Enter>", on_enterRun)
        runButton.bind("<Leave>", on_leaveRun)

        ########################## TEXT AREA ###########################
        def multipleyView(*args):
            codingArea.yview(*args)
            numbArea.yview(*args)


        yscrollCode = Scrollbar(mainPanel, orient="vertical")
        xscrollCode = Scrollbar(mainPanel, orient="horizontal")
        yscrollCode.place(x=WIDTH-TOOLBWIDTH-FOLDERWIDTH-NUMBERSWIDTH, y=0, anchor=NE, height=HEIGHT-MENUHEIGHT-15)
        xscrollCode.place(x=0, y=HEIGHT-MENUHEIGHT, anchor=SW, width=WIDTH-TOOLBWIDTH-FOLDERWIDTH-NUMBERSWIDTH)

        codingArea= Text(mainPanel, background=BACKGROUND, highlightthickness=0, height=31, width=110, highlightcolor=BACKGROUND, fg= 'white', insertbackground='white', yscrollcommand=yscrollCode.set, xscrollcommand=xscrollCode.set, wrap="none")
        codingArea.place(x=-1,y=-1)
        codingArea.config(spacing1=SPACING)    # Spacing above the first line in a block of text
        font = tkfont.Font(font=codingArea['font'])
        tab_size = font.measure('    ')
        codingArea.config(tabs=tab_size)
        
        numbArea= Text(numBar, background=BACKGROUND, width=NUMBERSWIDTH, height=HEIGHT-MENUHEIGHT, highlightthickness=0, highlightcolor=BACKGROUND, fg= LIGHTERBG, yscrollcommand=yscrollCode.set, wrap="none")
        numbArea.place(x=-1,y=-1)
        numbArea.config(spacing1=SPACING)    # Spacing above the first line in a block of text
        numbArea.config(state=DISABLED)

        xscrollCode.config(command=codingArea.xview)
        yscrollCode.config(command=multipleyView)

        def newCodeLine(event):
            numbArea.config(state=NORMAL)
            currentLine = int(codingArea.index('end-1c').split('.')[0])
            numbArea.delete('1.0', END)
            if int(currentLine) > 1:
                for i in range(currentLine):
                    numbArea.insert(END,str(i+1)+"\n")
            else:
                numbArea.insert(END,"1\n")
            numbArea.config(state=DISABLED)
        

        codingArea.bind("<KeyRelease>", newCodeLine)

        #self.ventana.protocol("WM_DELETE_WINDOW",1) 
        self.ventana.mainloop()


Interface() 