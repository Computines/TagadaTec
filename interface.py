from asyncio import events
from distutils.cmd import Command
from tkinter import *
from os import path
from winreg import REG_DWORD_BIG_ENDIAN
fnt=("Arial Narrow",10)
WIDTH       =   1200
HEIGHT      =   700
TOOLBWIDTH  =   50
MENUHEIGHT  =   30
FOLDERWIDTH =   200
BACKGROUND  =   "#1e1e1e"
TOOLBAR     =   "#333333"
FOLDERBAR   =   "#252526"
MENUBAR     =   "#3c3c3c"
LIGHTERBG   =   "#505050"
REDBG       =   "#d61425"


class Interface:
    def __init__(self):
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
        mainPanel.place(x=TOOLBWIDTH+FOLDERWIDTH,y=MENUHEIGHT)

        folderbar = Canvas(self.ventana, background=FOLDERBAR, width=FOLDERWIDTH, height=HEIGHT-MENUHEIGHT, highlightthickness=0)
        folderbar.place(x=TOOLBWIDTH,y=MENUHEIGHT)

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

        def close(e):    
            self.ventana.destroy()

        def on_enterExit(e):
            exitButton['background'] = REDBG

        def on_leaveExit(e):
            exitButton['background'] = MENUBAR

        def on_enterBuild(e):
            buildButton['background'] = LIGHTERBG

        def on_leaveBuild(e):
            buildButton['background'] = TOOLBAR

        def on_enterRun(e):
            runButton['background'] = LIGHTERBG

        def on_leaveRun(e):
            runButton['background'] = TOOLBAR

        exitImage = cargar_img("quitImage.png")
        exitButton = Button(self.ventana, image=exitImage, width=MENUHEIGHT, height=MENUHEIGHT-2, border=0, bg=MENUBAR)
        exitButton.place(x=WIDTH,y=0, anchor=NE)
        exitButton.bind("<Enter>", on_enterExit)
        exitButton.bind("<Leave>", on_leaveExit)
        exitButton.bind('<Button-1>', close)

        buildImage = cargar_img("buildImage.png")
        buildButton = Button(self.ventana, image=buildImage, width=TOOLBWIDTH-2, height=TOOLBWIDTH, border=0, bg=TOOLBAR)
        buildButton.place(x=0,y=MENUHEIGHT+10, anchor=NW)
        buildButton.bind("<Enter>", on_enterBuild)
        buildButton.bind("<Leave>", on_leaveBuild)

        runImage = cargar_img("runImage.png")
        runButton = Button(self.ventana, image=runImage, width=TOOLBWIDTH-2, height=TOOLBWIDTH, border=0, bg=TOOLBAR)
        runButton.place(x=0,y=MENUHEIGHT+70, anchor=NW)
        runButton.bind("<Enter>", on_enterRun)
        runButton.bind("<Leave>", on_leaveRun)

        #self.ventana.protocol("WM_DELETE_WINDOW",1) 
        self.ventana.mainloop()


Interface() 