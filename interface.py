from asyncio import events
from asyncio.windows_events import NULL
from distutils.cmd import Command
from distutils.command.build import build
from distutils.command.build_scripts import first_line_re
from tkinter import *
from tkinter import ttk
import os
import tkinter.font as tkfont
from tkinter import filedialog
from lex import *
from parserTokens import Parser
from ctypes import windll
from emitter import *

fnt=("Arial",10)
filename = ""
hasstyle = False
SPACING     =   5
WIDTH       =   1200
HEIGHT      =   700
TOOLBWIDTH  =   50
MENUHEIGHT  =   30
FOLDERWIDTH =   200
CONHEIGHT   =   230
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
        self.ventana.title("TagaPlate")
        self.ventana.minsize(WIDTH,HEIGHT) 
        self.ventana.resizable(width=NO, height=NO)

        def set_appwindow():
            global hasstyle
            GWL_EXSTYLE=-20
            WS_EX_APPWINDOW=0x00040000
            WS_EX_TOOLWINDOW=0x00000080
            if not hasstyle:
                hwnd = windll.user32.GetParent(self.ventana.winfo_id())
                style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
                style = style & ~WS_EX_TOOLWINDOW
                style = style | WS_EX_APPWINDOW
                res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
                self.ventana.withdraw()
                self.ventana.after(10, lambda:self.ventana.wm_deiconify())
                hasstyle=True


        self.ventana.overrideredirect(True)

        def cargar_img(nombre):
            ruta=os.path.join("assets",nombre) #crea acceso a la ruta assets dentro de la carpeta del programa
            img=PhotoImage(file=ruta) #importa la imagen
            return img #retorna la imagen 

        mainPanel = Canvas(self.ventana, background=BACKGROUND, width=WIDTH-TOOLBWIDTH-FOLDERWIDTH, height=HEIGHT-MENUHEIGHT-CONHEIGHT, highlightthickness=0)
        mainPanel.place(x=TOOLBWIDTH+FOLDERWIDTH+NUMBERSWIDTH,y=MENUHEIGHT)

        consolePanel = Canvas(self.ventana, background=BACKGROUND, width=WIDTH-FOLDERWIDTH, height=CONHEIGHT, highlightthickness=0)
        consolePanel.place(x=TOOLBWIDTH+FOLDERWIDTH,y=HEIGHT-CONHEIGHT)

        folderbar = Canvas(self.ventana, background=FOLDERBAR, width=FOLDERWIDTH, height=HEIGHT-MENUHEIGHT, highlightthickness=0)
        folderbar.place(x=TOOLBWIDTH,y=MENUHEIGHT)

        numBar = Canvas(self.ventana, background=BACKGROUND, width=NUMBERSWIDTH, height=HEIGHT-MENUHEIGHT-CONHEIGHT, highlightthickness=0)
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

        openedFile=Label(self.ventana, font=fnt, fg="#dedede", bg=MENUBAR, text="TagaPlate")
        openedFile.place(x=WIDTH/2,y=TOOLBWIDTH/4,anchor="center")
        
        ########################## TREE DIRECTORY ###########################
        directory=os.getcwd()
        treeFrame=Frame(folderbar, bg=FOLDERBAR, height=HEIGHT-MENUHEIGHT-15, width=FOLDERWIDTH-15)

        treeStyle = ttk.Style(treeFrame)
        treeStyle.theme_use("alt")
        treeStyle.configure("Treeview", background=FOLDERBAR, foreground="#dedede", fieldbackground=FOLDERBAR)
        treeStyle.configure("Treeview", highlightthickness=0, bd=0, font=('Arial', 10))
        treeStyle.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        treeStyle.map("Treeview", background = [('selected', LIGHTERBG)])

        scrollStyle = ttk.Style(folderbar)
        scrollStyle.element_create('Horizontal.Scrollbar.trough', 'from', 'default')
        scrollStyle.element_create('Horizontal.Scrollbar.thumb', 'from', 'default')
        scrollStyle.element_create('Horizontal.Scrollbar.leftarrow', 'from', 'default')
        scrollStyle.element_create('Horizontal.Scrollbar.rightarrow', 'from', 'default')
        scrollStyle.element_create('Horizontal.Scrollbar.grip', 'from', 'default')
        scrollStyle.layout('Horizontal.TScrollbar',
            [
                ('Horizontal.Scrollbar.trough', {'children':
                    [('Horizontal.Scrollbar.leftarrow', {'side': 'left', 'sticky': ''}),
                    ('Horizontal.Scrollbar.rightarrow', {'side': 'right', 'sticky': ''}),
                    ('Horizontal.Scrollbar.thumb', {'unit': '1', 'children':
                        [('Horizontal.Scrollbar.grip', {'sticky': ''})],
                    'sticky': 'nswe'})],
                    'sticky': 'we'}),
            ])
        scrollStyle.layout('Horizontal.TScrollbar', [('Horizontal.Scrollbar.trough', 
        {'children': [('Horizontal.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})], 'sticky': 'ew'})])
        scrollStyle.configure('Horizontal.TScrollbar',
            troughcolor=FOLDERBAR,
            background=FOLDERBAR,
            arrowcolor=LIGHTERBG,
            gripcolor="white",
            thumbcolor="white")
        scrollStyle.map('Horizontal.TScrollbar',
            background=[('pressed', '!disabled', LIGHTERBG), ('active', TOOLBAR)])
        
        scrollStyle.element_create('Vertical.Scrollbar.trough', 'from', 'default')
        scrollStyle.element_create('Vertical.Scrollbar.thumb', 'from', 'default')
        scrollStyle.element_create('Vertical.Scrollbar.leftarrow', 'from', 'default')
        scrollStyle.element_create('Vertical.Scrollbar.rightarrow', 'from', 'default')
        scrollStyle.element_create('Vertical.Scrollbar.grip', 'from', 'default')
        scrollStyle.layout('Vertical.TScrollbar',
            [
                ('Vertical.Scrollbar.trough', {'children':
                    [('Vertical.Scrollbar.leftarrow', {'side': 'left', 'sticky': ''}),
                    ('Vertical.Scrollbar.rightarrow', {'side': 'right', 'sticky': ''}),
                    ('Vertical.Scrollbar.thumb', {'unit': '1', 'children':
                        [('Vertical.Scrollbar.grip', {'sticky': ''})],
                    'sticky': 'nswe'})],
                    'sticky': 'we'}),
            ])
        scrollStyle.layout('Vertical.TScrollbar', [('Vertical.Scrollbar.trough', 
        {'children': [('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})], 'sticky': 'ns'})])
        scrollStyle.configure('Vertical.TScrollbar',
            troughcolor=FOLDERBAR,
            background=FOLDERBAR,
            arrowcolor=LIGHTERBG,
            gripcolor="white",
            thumbcolor="white")
        scrollStyle.map('Vertical.TScrollbar',
            background=[('pressed', '!disabled', LIGHTERBG), ('active', TOOLBAR)])

        yscrollTree = ttk.Scrollbar(folderbar, orient="vertical")
        xscrollTree = ttk.Scrollbar(folderbar, orient="horizontal")
        yscrollTree.place(x=FOLDERWIDTH+1, y=-1, anchor=NE, height=HEIGHT-MENUHEIGHT-12)
        xscrollTree.place(x=-1, y=HEIGHT-MENUHEIGHT+1, anchor=SW, width=FOLDERWIDTH+2)

        def fixed_map(option):
            return [elm for elm in treeStyle.map('Treeview', query_opt=option) if
            elm[:2] != ('!disabled', '!selected')]
        treeStyle.map('Treeview', 
            foreground=fixed_map('foreground'),
            background=fixed_map('background'))
        folderTree=ttk.Treeview(treeFrame, show='tree', yscrollcommand=yscrollTree.set,  xscrollcommand=xscrollTree.set)
        folderTree.heading('#0',text='directory:'+ directory,anchor='w')
        folderTree.heading('#0', text='Dir：'+directory, anchor='w')
        directory=os.path.abspath(directory)
        node=folderTree.insert('','end', text=os.path, open=True)
        def traverse_dir(parent, directory):
            for d in os.listdir(directory):
                full_path=os.path.join(directory,d)
                isdir = os.path.isdir(full_path)
                id=folderTree.insert(parent,'end',text=d,open=False, tags=tuple(map(str, full_path.split('%\%'))))
                if isdir:
                    traverse_dir(id,full_path)

        def delete_dir():
            for i in folderTree.get_children():
                folderTree.delete(i)

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
        def readFile(file, i=1):
            global filename
            try:
                line=file.readline()
                codingArea.insert(END,line)
                readFile(file, i+1)
            except:
                file.close()

        def saveFile(file, i=0):
            global filename
            try:
                file.write(codingArea.get("1.0",END))
            except:
                file.close()        

        def browseFiles():
            global filename
            filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Tagaplate",
                                                        "*.tpl*"),))
            if filename != "":
                codingArea.delete('1.0', END)
                openedFile["text"]=filename.split('/')[-1]+" - TagaPlate"
                file=open(filename,"r+")
                readFile(file)
                newCodeLine(1)
        
        def saveChanges():
            global filename
            try:
                file=open(filename,"r+")
                saveFile(file)
            except:
                saveAs()

        def saveAs():
            global filename
            files = [('Tagaplate', '*.tpl')]
            file = filedialog.asksaveasfile(filetypes = files, defaultextension = files)
            try:
                filename=file.name
                openedFile["text"]=filename.split('/')[-1]+" - TagaPlate"
                saveFile(file)
            except:
                pass
            delete_dir()
            directory=os.getcwd()
            node=folderTree.insert('','end', text=os.path, open=True)
            traverse_dir(node,directory)

        def onDoubleClick(e):
            global filename
            item = folderTree.selection()[0]
            codingArea.delete('1.0', END)
            try:
                filename = "".join(folderTree.item(item,"tags"))
                openedFile["text"]=folderTree.item(item,"text")+" - TagaPlate"
                file=open(filename,"r+")
                readFile(file)
                newCodeLine(1)
            except:
                codingArea.insert(END,"Error al abrir archivo")

        folderTree.bind("<Double-1>", onDoubleClick)

        exitImage = cargar_img("quitImage.png")
        exitButton = Button(self.ventana, image=exitImage, width=MENUHEIGHT, height=MENUHEIGHT-2, border=0, bg=MENUBAR)
        exitButton.place(x=WIDTH,y=0, anchor=NE)
        exitButton.bind("<Enter>", on_enterExit)
        exitButton.bind("<Leave>", on_leaveExit)
        exitButton.bind('<Button-1>', close)

        openImage = cargar_img("openImage.png")
        openButton = Button(toolbar, image=openImage, width=TOOLBWIDTH-2, height=TOOLBWIDTH, border=0, bg=TOOLBAR, command=browseFiles)
        openButton.place(x=0,y=0, anchor=NW)
        openButton.bind("<Enter>", on_enterOpen)
        openButton.bind("<Leave>", on_leaveOpen)

        saveImage = cargar_img("saveImage.png")
        saveButton = Button(toolbar, image=saveImage, width=TOOLBWIDTH-2, height=TOOLBWIDTH, border=0, bg=TOOLBAR, command=saveChanges)
        saveButton.place(x=0,y=1*BUTTONGRID, anchor=NW)
        saveButton.bind("<Enter>", on_enterSave)
        saveButton.bind("<Leave>", on_leaveSave)

        saveAsImage = cargar_img("saveAsImage.png")
        saveAsButton = Button(toolbar, image=saveAsImage, width=TOOLBWIDTH-2, height=TOOLBWIDTH, border=0, bg=TOOLBAR, command=saveAs)
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
        yscrollCode = ttk.Scrollbar(self.ventana, orient="vertical")
        xscrollCode = ttk.Scrollbar(self.ventana, orient="horizontal")
        yscrollCode.place(x=WIDTH, y=MENUHEIGHT, anchor=NE, height=HEIGHT-MENUHEIGHT-CONHEIGHT-13)
        xscrollCode.place(x=TOOLBWIDTH+FOLDERWIDTH+NUMBERSWIDTH, y=HEIGHT-CONHEIGHT+1, anchor=SW, width=WIDTH-TOOLBWIDTH-FOLDERWIDTH-NUMBERSWIDTH+2)

        codingArea= Text(mainPanel, background=BACKGROUND, highlightthickness=0, height=20, width=110, highlightcolor=BACKGROUND, fg= 'white', insertbackground='white', yscrollcommand=yscrollCode.set, xscrollcommand=xscrollCode.set, wrap="none")
        codingArea.place(x=-1,y=-1)
        codingArea.config(spacing1=SPACING)    # Spacing above the first line in a block of text
        font = tkfont.Font(font=codingArea['font'])
        tab_size = font.measure('    ')
        codingArea.config(tabs=tab_size)
        
        numbArea= Text(numBar, background=BACKGROUND, width=110, height=20, highlightthickness=0, highlightcolor=BACKGROUND, fg= LIGHTERBG, yscrollcommand=yscrollCode.set, wrap="none", borderwidth=0)
        numbArea.place(x=-1,y=-1)
        numbArea.config(spacing1=SPACING)    # Spacing above the first line in a block of text
        numbArea.config(state=DISABLED)

        xscrollCode.config(command=codingArea.xview)
        yscrollCode.config(command=multipleyView)

        def newCodeLine(event):
            cleanErrors()
            cleanLines()
            colorCode()
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

        def newConsoleLine(text):
            consoleArea.config(state=NORMAL)
            consoleArea.insert(END,text+"\n")
            consoleArea.config(state=DISABLED)

        def errorLine(error):
            index1 = str(float(str(error).split(" ")[4]))
            index2 = str(float(str(error).split(" ")[4])+1)
            codingArea.tag_remove("error", "1.0", END)
            codingArea.tag_remove("error", "1.0", END)
            codingArea.tag_add("error", index1, index2)
            codingArea.tag_config("error",
                foreground="#f14c4c",
                underline=True)
            numbArea.tag_add("error", index1, index2)
            numbArea.tag_config("error",
                background="#7d2828",
                foreground="white")

        def cleanErrors():
            codingArea.tag_remove("error", "1.0", END)
            codingArea.tag_remove("error", "1.0", END)
            numbArea.tag_add("error", '1.0', END)
            codingArea.tag_config("error",
                foreground="white")
            numbArea.tag_add("error", '1.0', END)
            numbArea.tag_config("error",
                background=BACKGROUND,
                foreground=LIGHTERBG)
        
        def cleanLines():
            for tag in codingArea.tag_names():
                codingArea.tag_remove(tag, "1.0", "end")

        def getColor(kind):
            if kind == 1:
                return "#43c9b0"
            elif kind == 2:
                return "#67cefe"
            elif kind == 3:
                return "#cb5923"
            elif kind>100 and kind<200:
                return "#c586c0"
            elif kind>200 and kind<216:
                return "#dcdcaa"
            elif kind>216 and kind<300:
                return "#499bd6"
            elif kind>300 and kind<400:
                return "#499bd6"
            else:
                return "white" 

        def lexTheToken(token, firstLine, firstChar, i, j, n):
            try:
                if token!="":
                    lexerVerif = Lexer(token)
                    lexedToken = lexerVerif.getToken()
                    kind = lexedToken.kind.value
                    color=getColor(kind)
                    codingArea.tag_add(str(n), str(firstLine)+"."+str(firstChar), str(i)+"."+str(j))
                    codingArea.tag_config(str(n),
                        foreground=color)
            except Exception as e:
                pass

        def colorCode():
            firstLine=0
            firstChar=0
            n=0
            i=1
            j=0
            token=""
            while i<=int(codingArea.index('end-1c').split('.')[0]):
                while j<len(codingArea.get(str(i)+".0", 'end-1c')):
                    if firstLine == 0 and firstChar == 0:
                        firstLine=i
                        firstChar=j;
                    char = codingArea.get(str(i)+"."+str(j), str(i)+"."+str(j+1))
                    if char == " " or char == "\n" or  char == "\t" or char == "\r" or char == ";":
                        lexTheToken(token, firstLine, firstChar, i, j, n)
                        token=""
                        firstLine=0
                        firstChar=0
                    elif char == "(" or char == ")":
                        lexTheToken(token, firstLine, firstChar, i, j, n)
                        n+=1
                        token=""
                        codingArea.tag_add(str(n), str(i)+"."+str(j), str(i)+"."+str(j+1))
                        codingArea.tag_config(str(n),
                            foreground="#c586c0")
                        firstLine=0
                        firstChar=0
                    else:
                        token+=char
                    
                    j+=1
                    n+=1
                i+=1
                n+=1
                j=0


        ########################## CONSOLA ###########################

        terminalLabel=Label(consolePanel, font=fnt, fg="#dedede", bg=BACKGROUND, text="Terminal")
        terminalLabel.place(x=5,y=5)
        fontToUnderline = tkfont.Font(terminalLabel, terminalLabel.cget("font"))
        fontToUnderline.configure(underline = True)
        terminalLabel.configure(font=fontToUnderline)

        yscrollConsole = ttk.Scrollbar(self.ventana, orient="vertical")
        xscrollConsole = ttk.Scrollbar(self.ventana, orient="horizontal")
        yscrollConsole.place(x=WIDTH, y=HEIGHT-CONHEIGHT, anchor=NE, height=CONHEIGHT-13)
        xscrollConsole.place(x=TOOLBWIDTH+FOLDERWIDTH, y=HEIGHT+1, anchor=SW, width=WIDTH-TOOLBWIDTH-FOLDERWIDTH+2)

        consoleArea= Text(consolePanel, background=BACKGROUND, highlightthickness=0, height=8, width=116, highlightcolor=BACKGROUND, fg= 'white', insertbackground='white', yscrollcommand=yscrollConsole.set, xscrollcommand=xscrollConsole.set, wrap="none", borderwidth=0)
        consoleArea.place(x=-1,y=30)
        consoleArea.config(spacing1=SPACING)    # Spacing above the first line in a block of text
        font = tkfont.Font(font=consoleArea['font'])
        tab_size = font.measure('    ')
        consoleArea.config(tabs=tab_size)
        consoleArea.insert(END,os.getcwd()+"\n")
        consoleArea.config(state=DISABLED)

        xscrollConsole.config(command=consoleArea.xview)
        yscrollConsole.config(command=consoleArea.yview)

        ########################## PROGRAMA ###########################
        def buildFile(e):
            try:
                lexer = Lexer(codingArea.get('1.0', END))
                emitter = Emitter("outputCompiled.py")
                parser = Parser(lexer, emitter)
                parser.program() 
                newConsoleLine("Complilation Completed")
            except Exception as n:
                try:
                    errorLine(n)
                except:
                    pass
                newConsoleLine(str(n))

        def runFile(e):
            buildFile(e)
            try:
                #os.system('outputCompiled.py')
                newConsoleLine(os.popen('outputCompiled.py').read())
            except Exception as n:
                errorLine(n)
                newConsoleLine(str(n))  

        buildButton.bind('<Button-1>',buildFile)
        runButton.bind('<Button-1>',runFile)

        #self.ventana.protocol("WM_DELETE_WINDOW",1)
        self.ventana.update_idletasks()
        self.ventana.withdraw()
        set_appwindow() 
        self.ventana.mainloop()

Interface() 