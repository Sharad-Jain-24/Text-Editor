import os
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter.colorchooser import *


class Notepad:

    __root = Tk()
    __Width = 500
    __Height = 500
    __Menu = Menu(__root)
    __FMenu = Menu(__Menu, tearoff=0)
    __EMenu = Menu(__Menu, tearoff=0)
    __TMenu = Menu(__Menu, tearoff=0)
    __OMenu = Menu(__Menu, tearoff=0)
    __TextArea = Text(__root, wrap=WORD, font=Font(family="Times New Roman", size=12))                # -------------------------------
    __Scrollbar = Scrollbar(__TextArea)
    __file = None
    __temp = 0

    def __init__(self, **kwargs):
        try:
            self.__root.wm_iconbitmap("notes.ico")
        except tkinter.TclError:                                # ---------------------
            print("error icon")
        try:
            self.__Width = kwargs['width']
        except KeyError:
            print("key error - width")
        try:
            self.__Height = kwargs['height']
        except KeyError:
            print("key error - height")
        self.__root.title("Untitled - Notepad")
        screenWidth = self.__root.winfo_screenwidth()
        screenHeight = self.__root.winfo_screenheight()
        left = (screenWidth / 2) - (self.__Width / 2)
        top = (screenHeight / 2) - (self.__Height / 2)
        self.__root.geometry('%dx%d+%d+%d' % (self.__Width, self.__Height, left, top))
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)
        self.__TextArea.grid(sticky=N + E + S + W)
        self.__FMenu.add_command(label="New", command=self.__newf)
        self.__FMenu.add_command(label="Open", command=self.__open)
        self.__FMenu.add_command(label="Save", command=self.__savef)
        self.__Menu.add_cascade(label="File", menu=self.__FMenu)
        self.__EMenu.add_command(label="Cut", command=self.__cut)
        self.__EMenu.add_command(label="Copy", command=self.__copy)
        self.__EMenu.add_command(label="Paste", command=self.__paste)
        self.__Menu.add_cascade(label="Edit", menu=self.__EMenu)
        self.__TMenu.add_command(label="Font", command=self.__fon)
        self.__TMenu.add_command(label="Font Color", command=self.__fcolor)
        self.__TMenu.add_command(label="Background Color", command=self.__bcolor)
        self.__Menu.add_cascade(label="Appearance", menu=self.__TMenu)
        self.__OMenu.add_command(label="Find", command=self.__fnd)
        self.__Menu.add_cascade(label="Tools", menu=self.__OMenu)
        self.__root.config(menu=self.__Menu)
        self.__Scrollbar.pack(side=RIGHT, fill=Y)
        self.__Scrollbar.config(command=self.__TextArea.yview)
        self.__TextArea.config(yscrollcommand=self.__Scrollbar.set)

    def __open(self):
        self.__file = askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if self.__file == "":
            self.__file = None
        else:
            self.__root.title(os.path.basename(self.__file) + " - Notepad")
            self.__TextArea.delete(1.0, END)
            file = open(self.__file, "r")
            self.__TextArea.insert(1.0, file.read())
            file.close()

    def __newf(self):
        self.__root.title("Untitled - Notepad")
        self.__file = None
        self.__TextArea.delete(1.0, END)

    def __savef(self):
        if self.__file is None:
            self.__file = asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
            if self.__file == "":
                self.__file = None
            else:
                file = open(self.__file, "w")
                file.write(self.__TextArea.get(1.0, END))
                file.close()
                self.__root.title(os.path.basename(self.__file) + " - Notepad")
        else:
            file = open(self.__file, "w")
            file.write(self.__TextArea.get(1.0, END))
            file.close()

    def __cut(self):
        self.__TextArea.event_generate("<<Cut>>")

    def __copy(self):
        self.__TextArea.event_generate("<<Copy>>")

    def __paste(self):
        self.__TextArea.event_generate("<<Paste>>")

    def __fcolor(self):
        fcolor = askcolor(title="Font Color Chooser")
        self.__TextArea.configure(foreground=fcolor[1])

    def __bcolor(self):
        bcolor = askcolor(title="Background Color Chooser")
        self.__TextArea.configure(background=bcolor[1])

    # def __fon(self):
    #     win = Tk()
    #     win.title("Font Selector")
    #     win.geometry('185x185')
    #     n = tkinter.StringVar()
    #     cmb = ttk.Combobox(win, width=27, state="readonly", textvariable=n)
    #     cmb['values'] = ("Times New Roman", "Cooper", "Algerian", "Arial Black", "Georgia", "Franklin Gothic Heavy")
    #     cmb.grid(column=1, row=5)
    #     txt = cmb.get()
    #     self.__TextArea.tag_configure('bold_italics', font=txt)
    #     cmb = tkinter.Button(win, text="Done", command=win.destroy)
    #     cmb.grid(row=10, column=1)
    #     print("Hi")

    def __fon(self):
        win = Tk()
        win.title("Font Selector")
        win.geometry('185x185')
        n = tkinter.StringVar()
        style = Label(win, text="Select Font:")
        style.grid(row=0, column=0, sticky=W)
        cmb = ttk.Combobox(win, width=27, state="readonly", textvariable=n)
        cmb['values'] = font.families()
        cmb.grid(column=0, row=1)
        cmb.set("Times New Roman")

        cmb2 = tkinter.Button(win, text="Done", command=lambda: self.__font_change(cmb.get()))
        cmb2.grid(row=2, column=0)

    def __font_change(self, txt):
        self.__temp += 1
        # self.__TextArea.tag_remove("font" + str(self.__temp), 1.0, END)
        try:
            self.__TextArea.tag_add("font" + str(self.__temp), SEL_FIRST, SEL_LAST)
        except tkinter.TclError:
            self.__TextArea.tag_add("font" + str(self.__temp), 1.0, END)
        my_font = Font(family=txt)
        self.__TextArea.tag_configure("font" + str(self.__temp), font=my_font)
        # self.__TextArea.tag_remove("font 1", SEL_FIRST, SEL_LAST)

    def __fnd(self):
        win = Tk()
        win.title("Search For")
        print("this")

    def run(self):
        self.__root.mainloop()


notepad = Notepad(width=820, height=450)
notepad.run()
