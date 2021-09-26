import os
import re
import tkinter
import wikipedia
from tkinter import *
from tkinter import ttk, font
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
    __TextArea = Text(__root)
    __Scrollbar = Scrollbar(__TextArea)
    __file = None

    def __init__(self, **kwargs):
        try:
            self.__root.wm_iconbitmap("notes.ico")
        except:
            pass
        try:
            self.__Width = kwargs['width']
        except KeyError:
            pass
        try:
            self.__Height = kwargs['height']
        except KeyError:
            pass
        self.__root.title("Untitled - Notepad")
        screenWidth = self.__root.winfo_screenwidth()
        screenHeight = self.__root.winfo_screenheight()
        left = (screenWidth / 2) - (self.__Width / 2)
        top = (screenHeight / 2) - (self.__Height / 2)
        self.__root.geometry('%dx%d+%d+%d' % (self.__Width, self.__Height, left, top))
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)
        self.__TextArea.grid(sticky=N + E + S + W)
        self.__FMenu.add_command(label="New", compound=LEFT, accelerator='Ctrl+N', command=self.__newf)
        self.__FMenu.add_command(label="Open", compound=LEFT, accelerator='Ctrl+O', command=self.__open)
        self.__FMenu.add_command(label="Save", compound=LEFT, accelerator='Ctrl+S', command=self.__savef)
        self.__FMenu.add_command(label="Exit", compound=LEFT, accelerator='ALt+Q', command=self.__ext)
        self.__Menu.add_cascade(label="File", menu=self.__FMenu)
        self.__EMenu.add_command(label="Cut", compound=LEFT, accelerator='Ctrl+X', command=self.__cut)
        self.__EMenu.add_command(label="Copy", compound=LEFT, accelerator='Ctrl+C', command=self.__copy)
        self.__EMenu.add_command(label="Paste", compound=LEFT, accelerator='Ctrl+P', command=self.__paste)
        self.__EMenu.add_command(label="Left Align", compound=LEFT, accelerator='Ctrl+L', command=self.__lalign)
        self.__EMenu.add_command(label="Center Align", compound=LEFT, accelerator='Ctrl+J', command=self.__calign)
        self.__EMenu.add_command(label="Right Align", compound=LEFT, accelerator='Ctrl+R', command=self.__ralign)
        self.__EMenu.add_command(label='Clear All', compound=LEFT, accelerator='Ctrl+ALt+C', command=self.__clr)
        self.__Menu.add_cascade(label="Edit", menu=self.__EMenu)
        self.__TMenu.add_command(label="Font", compound=LEFT, accelerator='Ctrl+ALt+F',  command=self.__fonf)
        self.__TMenu.add_command(label="Font Color", compound=LEFT, accelerator='Ctrl+ALt+B', command=self.__fcolor)
        self.__TMenu.add_command(label="Background Color", compound=LEFT, accelerator='Ctrl+B', command=self.__bcolor)
        self.__Menu.add_cascade(label="Appearance", menu=self.__TMenu)
        self.__OMenu.add_command(label="Local", compound=LEFT, accelerator='Ctrl+F', command=self.__lsrch)
        self.__OMenu.add_command(label="Web", compound=LEFT, accelerator='Ctrl+W', command=self.__wsrch)
        self.__Menu.add_cascade(label="Search", menu=self.__OMenu)
        self.__root.config(menu=self.__Menu)
        self.__Scrollbar.pack(side=RIGHT, fill=Y)
        self.__Scrollbar.config(command=self.__TextArea.yview)
        self.__TextArea.config(yscrollcommand=self.__Scrollbar.set)
        self.__root.bind("<Control-n>", self.__newf)
        self.__root.bind("<Control-o>", self.__open)
        self.__root.bind("<Control-s>", self.__savef)
        self.__root.bind("<Alt-q>", self.__ext)
        self.__root.bind("<Control-x>", self.__cut)
        self.__root.bind("<Control-c>", self.__copy)
        self.__root.bind("<Control-p>", self.__paste)
        self.__root.bind("<Control-l>", self.__lalign)
        self.__root.bind("<Control-j>", self.__calign)
        self.__root.bind("<Control-r>", self.__ralign)
        self.__root.bind("<Control-Alt-c>", self.__TextArea.delete(1.0,END))
        self.__root.bind("<Control-Alt-f>", self.__fonf)
        self.__root.bind("<Control-Alt-b>", self.__fcolor)
        self.__root.bind("<Control-b>", self.__bcolor)
        self.__root.bind("<Control-f>", self.__lsrch)
        self.__root.bind("<Control-w>", self.__wsrch)

    def __open(self, _event=None):
        self.__file = askopenfilename(defaultextension=".txt",
                                      filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if self.__file == "":
            self.__file = None
        else:
            self.__root.title(os.path.basename(self.__file) + " - Notepad")
            self.__TextArea.delete(1.0, END)
            file = open(self.__file, "r")
            self.__TextArea.insert(1.0, file.read())
            file.close()

    def __newf(self, _event=None):
        self.__root.title("Untitled - Notepad")
        self.__file = None
        self.__TextArea.delete(1.0, END)

    def __savef(self, _event=None):
        if self.__file == None:
            self.__file = asksaveasfilename(initialfile='Untitled.txt',defaultextension=".txt",
                                            filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
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

    def __ext(self, _event=None):
        if tkinter.messagebox.askokcancel("Quit?", "Do you want to QUIT for sure?\nMake sure you've saved your current work."):
            self.__root.destroy()

    def __cut(self, _event=None):
        self.__TextArea.event_generate("<<Cut>>")

    def __copy(self, _event=None):
        self.__TextArea.event_generate("<<Copy>>")

    def __paste(self, _event=None):
        self.__TextArea.event_generate("<<Paste>>")

    def __clr(self, _event=None):
        self.__TextArea.delete(1.0,END)

    def __lalign(self, _event=None):
        text_content = self.__TextArea.get(1.0, 'end')
        self.__TextArea.tag_config('left',justify=LEFT)
        self.__TextArea.delete(1.0,END)
        self.__TextArea.insert(INSERT,text_content,'left')

    def __calign(self, _event=None):
        text_content = self.__TextArea.get(1.0, 'end')
        self.__TextArea.tag_config('center',justify=CENTER)
        self.__TextArea.delete(1.0,END)
        self.__TextArea.insert(INSERT,text_content,'center')

    def __ralign(self, _event=None):
        text_content = self.__TextArea.get(1.0, 'end')
        self.__TextArea.tag_config('right',justify=RIGHT)
        self.__TextArea.delete(1.0,END)
        self.__TextArea.insert(INSERT,text_content,'right')

    def __fcolor(self, _event=None):
        fcolor = askcolor(title="Font Color Chooser")
        self.__TextArea.configure(foreground=fcolor[1])

    def __bcolor(self, _event=None):
        bcolor = askcolor(title="Background Color Chooser")
        self.__TextArea.configure(background=bcolor[1])

    def __fonf(self, _event=None):
        win = Toplevel()
        win.title("Font & Size")
        font_tuple = font.families()
        font_family = StringVar()
        font_box = ttk.Combobox(win, width=20, textvariable=font_family, state='readonly')
        font_box['values'] = font_tuple
        font_box.current(font_tuple.index('Arial'))
        font_box.grid(row=0, column=0, padx=5)
        size_var = IntVar()
        font_size = ttk.Combobox(win, width=14, textvariable=size_var)
        font_size['values'] = tuple(range(8,80,2))
        font_size.current(3)
        font_size.grid(row=0, column=1, padx=5)
        current_font_family = font_box.get()
        current_font_size = font_size.get()
        def change_font(event=None):
            self.__TextArea.tag_add("font 1", 1.0, END)
            global current_font_family
            current_font_family = font_box.get()
            self.__TextArea.config(font=(current_font_family, current_font_size))

        def change_size(event=None):
            self.__TextArea.tag_add("font 1", 1.0, END)
            global current_font_size
            current_font_size = font_size.get()
            self.__TextArea.config(font=(current_font_family, current_font_size))
        
        def change_bold():
            text_property = font.Font(font=self.__TextArea['font'])
            if text_property.actual()['weight']=='normal' :
                self.__TextArea.configure(font=(current_font_family,current_font_size,'bold'))
            if text_property.actual()['weight']=='bold' :
                self.__TextArea.configure(font=(current_font_family,current_font_size,'normal'))

        def change_italic():
            text_property = font.Font(font=self.__TextArea['font'])
            if text_property.actual()['slant']=='roman' :
                self.__TextArea.configure(font=(current_font_family,current_font_size,'italic'))
            if text_property.actual()['slant']=='italic' :
                self.__TextArea.configure(font=(current_font_family,current_font_size,'normal'))

        def underline():
            text_property = font.Font(font=self.__TextArea['font'])
            if text_property.actual()['underline']==0 :
                self.__TextArea.configure(font=(current_font_family,current_font_size,'underline'))
            if text_property.actual()['underline']==1 :
                self.__TextArea.configure(font=(current_font_family,current_font_size,'normal'))

        def reset_all():
            self.__TextArea.configure(font=('Arial','14','normal'))
            font_box.current(font_tuple.index('Arial'))
            font_size.current(font_size.index('14'))

        rest_btn = Button (win, text="R", command=reset_all)
        bold_btn = Button (win, text="B", command=change_bold)
        italic_btn = Button (win, text="I", command=change_italic)
        underline_btn = Button (win, text="U", command=underline)
        rest_btn.grid(row=0, column=2, sticky='nesw')
        bold_btn.grid(row=1, column=0, sticky='nesw')
        italic_btn.grid(row=1, column=1, sticky='nesw')
        underline_btn.grid(row=1, column=2, sticky='nesw')
        font_box.bind("<<ComboboxSelected>>",change_font)
        font_size.bind("<<ComboboxSelected>>",change_size)
        win.mainloop()

    def __lsrch(self, _event=None):
        def find():
            word = find_input.get()
            self.__TextArea.tag_remove('match', '1.0', END)
            matches = 0
            if word:
                start_pos = '1.0'
                while True:
                    start_pos = self.__TextArea.search(word, start_pos, stopindex=END)
                    if (not start_pos):
                        break
                    end_pos = f"{start_pos}+{len(word)}c"
                    self.__TextArea.tag_add('match', start_pos, end_pos)
                    matches += 1
                    start_pos = end_pos
                    self.__TextArea.tag_config('match', foreground='', background='yellow')

        def replace():
            word = find_input.get()
            replace_text = replace_input.get()
            content = self.__TextArea.get(1.0, END)
            new_content = content.replace(word, replace_text)
            self.__TextArea.delete(1.0, END)
            self.__TextArea.insert(1.0, new_content)
		
        win = Toplevel()
        win.title("Find & Replace")
        win.resizable(0, 0)
        find_frame = LabelFrame(win, text='Find/Replace')
        find_frame.pack(pady=20)
        text_find_label = Label(find_frame, text='Find :')
        text_replace_label = Label(find_frame, text='Replace')
        find_input = Entry(find_frame, width=30)
        replace_input = Entry(find_frame, width=30)
        find_button = Button(find_frame, text='Find:', command=find)
        replace_button = Button(find_frame, text='Replace:', command=replace)
        text_find_label.grid(row=0, column=0, padx=4, pady=4)
        text_replace_label.grid(row=1, column=0, padx=4, pady=4)
        find_input.grid(row=0, column=1, padx=4, pady=4)
        replace_input.grid(row=1, column=1, padx=4, pady=4)
        find_button.grid(row=2, column=0, padx=8, pady=4)
        replace_button.grid(row=2, column=1, padx=8, pady=4)
        win.mainloop()

    def __wsrch(self, _event=None):
        def get_me():
            ev = entry.get()
            answer.delete(1.0, END)
            try:
                av = wikipedia.summary(ev)
                answer.insert(INSERT, av)
            except:
                answer.insert(INSERT, "No Internet")

        win = Toplevel()
        win.title("Search For")
        topframe = Frame(win)
        entry = Entry(topframe)
        entry.pack()
        button = Button(topframe, text="Search", command=get_me)
        button.pack()
        topframe.pack(side=TOP)
        bottomframe = Frame(win)
        scroll = Scrollbar(bottomframe)
        scroll.pack(side=RIGHT, fill=Y)
        answer = Text(bottomframe, width=30, height=10, yscrollcommand=scroll.set, wrap=WORD)
        scroll.config(command=answer.yview)
        answer.pack()
        bottomframe.pack()
        win.mainloop()

    def run(self):
        self.__root.mainloop()

notepad = Notepad(width=1200, height=800)
notepad.run()

