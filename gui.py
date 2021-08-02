import tkinter
# Lots of tutorials have from tkinter import *, but that is pretty much always a bad idea
from tkinter import ttk
from PIL import Image, ImageTk
import json
import abc
import os

class Menubar(ttk.Frame):
    """Builds a menu bar for the top of the main window"""
    def __init__(self, parent, *args, **kwargs):
        ''' Constructor'''
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.init_menubar()

    def on_exit(self):
        '''Exits program'''
        quit()

    def display_help(self):
        '''Displays help document'''
        pass

    def display_about(self):
        '''Displays info about program'''
        pass

    def init_menubar(self):
        self.menubar = tkinter.Menu(self.root)
        self.menu_file = tkinter.Menu(self.menubar) # Creates a "File" menu
        self.menu_file.add_command(label='Exit', command=self.on_exit) # Adds an option to the menu
        self.menubar.add_cascade(menu=self.menu_file, label='File') # Adds File menu to the bar. Can also be used to create submenus.

        self.menu_help = tkinter.Menu(self.menubar) #Creates a "Help" menu
        self.menu_help.add_command(label='Help', command=self.display_help)
        self.menu_help.add_command(label='About', command=self.display_about)
        self.menubar.add_cascade(menu=self.menu_help, label='Help')

        self.root.config(menu=self.menubar)

class Window(ttk.Frame):
    """Abstract base class for a popup window"""
    __metaclass__ = abc.ABCMeta
    def __init__(self, parent):
        ''' Constructor '''
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.resizable(width=False, height=False) # Disallows window resizing
        self.validate_notempty = (self.register(self.notEmpty), '%P') # Creates Tcl wrapper for python function. %P = new contents of field after the edit.
        self.init_gui()

    @abc.abstractmethod # Must be overwriten by subclasses
    def init_gui(self):
        '''Initiates GUI of any popup window'''
        pass

    @abc.abstractmethod
    def do_something(self):
        '''Does something that all popup windows need to do'''
        pass

    def notEmpty(self, P):
        '''Validates Entry fields to ensure they aren't empty'''
        if P.strip():
            valid = True
        else:
            print("Error: Field must not be empty.") # Prints to console
            valid = False
        return valid

    def close_win(self):
        '''Closes window'''
        self.parent.destroy()

class SomethingWindow(Window):
    """ New popup window """

    def init_gui(self):
        self.parent.title("New Window")
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(3, weight=1)

        # Create Widgets

        self.label_title = ttk.Label(self.parent, text="This sure is a new window!")
        self.contentframe = ttk.Frame(self.parent, relief="sunken")

        self.label_test = ttk.Label(self.contentframe, text='Enter some text:')
        self.input_test = ttk.Entry(self.contentframe, width=30, validate='focusout', validatecommand=(self.validate_notempty))

        self.btn_do = ttk.Button(self.parent, text='Action', command=self.do_something)
        self.btn_cancel = ttk.Button(self.parent, text='Cancel', command=self.close_win)

        # Layout
        self.label_title.grid(row=0, column=0, columnspan=2, sticky='nsew')
        self.contentframe.grid(row=1, column=0, columnspan=2, sticky='nsew')

        self.label_test.grid(row=0, column=0)
        self.input_test.grid(row=0, column=1, sticky='w')

        self.btn_do.grid(row=2, column=0, sticky='e')
        self.btn_cancel.grid(row=2, column=1, sticky='e')

        # Padding
        for child in self.parent.winfo_children():
            child.grid_configure(padx=10, pady=5)
        for child in self.contentframe.winfo_children():
            child.grid_configure(padx=5, pady=2)

    def do_something(self):
        '''Does something'''
        text = self.input_test.get().strip()
        if text:
            # Do things with text
            self.close_win()
        else:
            print("Error: But for real though, field must not be empty.")

class GUI(ttk.Frame):
    """Main GUI class"""
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.data = json.load(open('result.json'))
        self.probelabel = list(self.data.keys()) # contains all probe images
        self.current = 0
        self.maxPhotos = 5
        self.rank = 5
        self.curProbeImgWidget = []
        self.curRankPred = []         
        
        self.init_gui()
        
    def getPhotosFromDir(self, dir):
        res = []
        count = 0
        idx = 0
        lstdir = os.listdir(dir)
        while (idx < len(lstdir) and count < self.maxPhotos):
            if (lstdir[idx].endswith(('.jpeg', '.png', '.jpg', '.JPG'))):
                res.append(os.path.join(dir, lstdir[idx]))
                count += 1
            idx += 1
        return res
    
    def loadCurrentImage(self):
        curProbe = self.probelabel[self.current]
        
        # Loading Probes
        probeImages = self.getPhotosFromDir(curProbe)
        self.curProbeImgWidget = [ImageTk.PhotoImage(file=image) for image in probeImages]
        for i in range(len(self.curProbeImgWidget)):
            ttk.Label(self, image=self.curProbeImgWidget[i]).grid(row=i, column=0)
            
        # Loading Rank-5
        self.curRankPred = [[] for _ in range(self.rank)]
        for i in range(self.rank):
            galImages = self.getPhotosFromDir(self.data[curProbe]['scores'][i][0])
            self.curRankPred[i] = [ImageTk.PhotoImage(file=image) for image in galImages]
            for j in range(len(self.curRankPred[i])):
                ttk.Label(self, image=self.curRankPred[i][j]).grid(row=i, column=j+1)
    
    def next(self):
        if (self.current < len(self.probelabel) - 1):
            self.current += 1
            print(self.current)
            self.loadCurrentImage()
            
    def prev(self):
        if (self.current > 0):
            self.current -= 1
            print(self.current)
            self.loadCurrentImage()

    def init_gui(self):
        self.root.title('SealNet')
        self.root.geometry("700x600")
        self.grid(column=0, row=0, sticky='nsew')
        self.grid_columnconfigure(0, weight=1) # Allows column to stretch upon resizing
        self.grid_rowconfigure(0, weight=1) # Same with row
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.option_add('*tearOff', 'FALSE') # Disables ability to tear menu bar into own window
        
        # Menu Bar
        self.menubar = Menubar(self.root)
        
        # Check if there is no probe
        if (len(self.probelabel) == 0):
            ttk.Label(self, text="There are no probe images to display")
        else:
            self.loadCurrentImage()
        
        # self.bind("<KeyPress-KP_Right>", self.next)
        # self.bind("<KeyPress-KP_Left>", self.prev)

if __name__ == '__main__':
    root = tkinter.Tk()
    GUI(root)
    root.mainloop()


