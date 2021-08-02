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
        self.new_win = tkinter.Toplevel(self.root) # Set parent
        HelpWindow(self.new_win)

    def init_menubar(self):
        self.menubar = tkinter.Menu(self.root)
        
        self.menu_file = tkinter.Menu(self.menubar) # Creates a "File" menu
        self.menu_file.add_command(label='Exit', command=self.on_exit) # Adds an option to the menu
        self.menubar.add_cascade(menu=self.menu_file, label='File') # Adds File menu to the bar. Can also be used to create submenus.

        self.menu_help = tkinter.Menu(self.menubar) #Creates a "Help" menu
        self.menu_help.add_command(label='Help', command=self.display_help)
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

class HelpWindow(Window):
    """ New popup window """

    def init_gui(self):
        self.parent.title("Help")
        self.parent.geometry("700x150")

        # Create Widgets
        text = "This is a graphical user interface for SealNet. \n\nYou need to create a `result.json` file by running `python seenbefore.py` prior to opening the GUI.\n\nThis GUI will display the current probe seal to the left of the screen with its name in between the Previous \nbutton and the Next button. On the right, the GUI will display the top-5 prediction from our facial recognition \nmodel with its respective similarity score. You can manually choose the one that you think it's the right match."
        
        self.help_label = ttk.Label(self.parent, text=text)
        self.help_label.pack(padx=15, pady=15)

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
        
        self.init_gui()

    def init_gui(self):
        self.root.title('SealNet')
        self.root.geometry("1100x900")
        self.grid(column=0, row=0, sticky='nsew')
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.option_add('*tearOff', 'FALSE') # Disables ability to tear menu bar into own window
        
        # Menu Bar
        self.menubar = Menubar(self.root)

        # Button Bar
        self.buttonBar = ttk.Frame(self)
        self.buttonBar.grid(row=0, column=0, pady=15)

        self.buttonBarDict = {} # to easily access elements in buttonBar Fram
        self.buttonBarDict[(0,0)] = ttk.Button(self.buttonBar, text="Previous", command=self.prev)
        self.buttonBarDict[(0,1)] = ttk.Label(self.buttonBar, text="")
        self.buttonBarDict[(0,2)] = ttk.Button(self.buttonBar, text="Next", command=self.next)
        for x,y in self.buttonBarDict.keys():
            self.buttonBarDict[(x,y)].grid(row=x, column=y, padx=30, pady=5)

        # Main Frame
        self.mainFrame = ttk.Frame(self)
        self.mainFrame.grid(row=1, column=0)

        # Add Probe and Label title
        ttk.Label(self.mainFrame, text="Probe", font=('Arial', 25)).grid(row=0, column=0)
        ttk.Label(self.mainFrame, text="Label", font=('Arial', 25)).grid(row=0, column=1, columnspan=3+self.maxPhotos)
        # Add Probe Frame
        probeFrame = tkinter.Frame(self.mainFrame, highlightbackground="black", highlightthickness=1)
        probeFrame.grid(row=1, column=0, padx=15, pady=15)
        self.probeFrameDict = {}
        for i in range(self.maxPhotos):
            self.probeFrameDict[(i, 0)] = ttk.Label(probeFrame, image=None)
            self.probeFrameDict[(i, 0)].grid(row=i, column=0, padx=10, pady=10)
        # Add Gallery Frame
        galleryFrame = tkinter.Frame(self.mainFrame, highlightbackground="black", highlightthickness=1)
        galleryFrame.grid(row=1, column=1, pady=15, ipadx=15, ipady=15)
        self.galleryFrameDict = {}
        for i in range(self.rank):
            self.galleryFrameDict[(2*i, 0)] = ttk.Label(galleryFrame, text='Rank {}'.format(i+1))
            self.galleryFrameDict[(2*i, 0)].grid(row=2*i, column=0, rowspan=2, padx=(15,0))
            self.galleryFrameDict[(2*i, 1)] = ttk.Label(galleryFrame, text='Score: ')
            self.galleryFrameDict[(2*i, 1)].grid(row=2*i, column=1, rowspan=2, padx=15)
            self.galleryFrameDict[(2*i, 2)] = ttk.Label(galleryFrame, text='')
            self.galleryFrameDict[(2*i, 2)].grid(row=2*i, column=2, columnspan=self.maxPhotos)
            for j in range(self.maxPhotos):
                self.galleryFrameDict[(2*i+1,j+2)] = ttk.Label(galleryFrame, image=None)
                self.galleryFrameDict[(2*i+1,j+2)].grid(row=2*i+1, column=j+2, padx=5, pady=5)
                
        # Check if there is no probe
        if (len(self.probelabel) > 0):
            self.loadCurrentImage()
        
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
    
    # Loading the main frame of the GUI displaying the current probe result
    def loadCurrentImage(self):
        curProbe = self.probelabel[self.current]
        # Display the new probe names
        self.buttonBarDict[(0,1)].configure(text=curProbe[curProbe.rindex('/')+1:])
        
        # Loading Probes
        probeImages = self.getPhotosFromDir(curProbe)
        curProbeImgWidget = [ImageTk.PhotoImage(file=image) for image in probeImages]
        for i in range(len(curProbeImgWidget)):
            self.probeFrameDict[(i, 0)].configure(image=curProbeImgWidget[i])
            self.probeFrameDict[(i, 0)].image = curProbeImgWidget[i]
            
        # Loading Rank-5
        curRankPred = [[] for _ in range(self.rank)]
        for i in range(self.rank):
            curGal, curGalScore = self.data[curProbe]['scores'][i][0], self.data[curProbe]['scores'][i][1]
            galImages = self.getPhotosFromDir(curGal)
            curRankPred[i] = [ImageTk.PhotoImage(file=image) for image in galImages]
            self.galleryFrameDict[(2*i, 2)].configure(text=curGal[curGal.rindex('/')+1:])
            self.galleryFrameDict[(2*i, 1)].configure(text='Score: {:.3f}'.format(curGalScore))
            for j in range(len(curRankPred[i])):
                self.galleryFrameDict[(2*i+1,j+2)].configure(image=curRankPred[i][j])
                self.galleryFrameDict[(2*i+1,j+2)].image = curRankPred[i][j]
    
    # Iterate through next image
    def next(self):
        if (self.current < len(self.probelabel) - 1):
            self.current += 1
            self.loadCurrentImage()
    
    # Iterate through previous image
    def prev(self):
        if (self.current > 0):
            self.current -= 1
            self.loadCurrentImage()

if __name__ == '__main__':
    root = tkinter.Tk()
    if (os.path.exists('result.json')):
        GUI(root)
    else:
        HelpWindow(root)
    root.mainloop()


