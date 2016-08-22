"""

PiDeF Ebook downloader
Version 1.0
Coded in Python 2.7

Modules used:
    Tkinter – For designing GUI interface
    Json – For decoding json files
    Urllib – for downloading pdf files
    Sqllite3 – for handling databases
    Googleapiclient – API connect for Google search

Features:
    Searches for PDF files in Google using Google API with advanced filtering using Google dorks
    Neatly designed GUI with proper user interfacing
    Varied number of search results
    Allows us to save a set of results in a database which can be retrieved easily from it

Future scope:
    Integration of download progress bar and status bar into the application
    PDF Preview and Information of the PDF to be displayed before downloading
    Using OCR to extract title of books from images and Auto-search based on it. ( Using camera or images )

Credits:
    Web scraping - Anirudh M
    API connect,JSON decoding,DBMS and integration into GUI - Arul Thileeban S
    GUI design - Daniel Jeswin Nallathambi
    Download functionality-Dheepthaa
"""
from Tkinter import *
import urllib,sqlite3 as sql
from API_connect import *
from decode_json import *

title_dict={}#Dictionary to store Titles and Links

def decode_store(no_files):
    """Function to store decoded json in a dictionary"""
    global title_dict
    title_dict=decode_json(no_files)

class RadioButtons(Radiobutton):
    def __init__(self, master, text, side, anchor, padx, pady, variable, value, command=None):
        """Initializes a set of Radiobuttons with integer values for each button"""

        b=Radiobutton(master, text=text, value=value, command=command, variable=variable)
        if(value==1):
            b.select()
        else:
            b.deselect()
        b.pack(side=side, anchor=anchor, pady=pady, padx=padx)

class List_Box(Listbox):
    def __init__(self, master, mode, height, width=62, command=None):
        """Initializes a listbox with scrollbar to scroll along the y-axis"""
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT, fill=Y)
        Listbox.__init__(self, master, selectmode=mode, height=height, width=width, yscrollcommand=scrollbar.set, command=command)
        self.pack(fill=X)
        scrollbar.config(command=self.yview)             
    def setSide(self, side):
        """Function to set the value of the side where the widget is to be positioned"""
        self.pack(side=side)
    def setAnchor(self, anchor):
        """Function to set the values of anchor"""
        self.pack(anchor=anchor)
    def setPads(self, padx, pady):
        """Function to set values of padx and pady"""
        self.pack(padx=padx, pady=pady)
    def add_val(self,Title):
        self.insert(END,Title)
        self.yview(END)

    

class TextBox(Entry):
    def __init__(self, master, width=50, text=None, command=None):
        """Initializes an entry widget with default text"""
        Entry.__init__(self, master=master, width=width, font=('Helvetica', 10), command=command)
        self.insert(0, text)
        self.firstclick=True#Check if entry is clicked for the first time to clear the default text
        self.pack(fill=X)
    def setSide(self, side):
        """Function to set the value of the side where the widget is to be positioned"""
        self.pack(side=side)
    def setAnchor(self, anchor):
        """Function to set the values of anchor"""
        self.pack(anchor=anchor)
    def setPads(self, padx, pady):
        """Function to set values of padx and pady"""
        self.pack(padx=padx, pady=pady)
        
    
    def on_entry_click(self, event):
        """Function to clear default text in the Entry on the first click of the mouse"""
        if self.firstclick: 
            self.firstclick = False
            self.delete(0, "end") 

       


class Buttons(Button):
    def __init__(self, master, text, command=None):
        """Initializes a button with the text on the master widget"""
        Button.__init__(self, master=master, text=text, height=1, command=command)
    def setSide(self, side):
        """Function to set the value of the side where the widget is to be positioned"""
        self.pack(side=side)
    def setAnchor(self, anchor):
        """Function to set the values of anchor"""
        self.pack(anchor=anchor)
    def setPads(self, padx, pady):
        """Function to set values of padx and pady"""
        self.pack(padx=padx, pady=pady)
    
    
class Layout(Frame):
  
    def __init__(self, parent):
        """Initializes overall frame for the dialog box"""
        Frame.__init__(self, parent)   
         
        self.parent = parent
        self.initUI()

        
    def initUI(self):
        """Initializes the various components of the frame"""
        self.parent.title("Ebook Downloader")
        
        #Seperate frame for the main widgets of the dialog box   
        frame = Frame(self, relief=RAISED, borderwidth=1)
    
        frame.pack(fill=BOTH, expand=True)
        self.pack(fill=BOTH, expand=True)

        #Button to view a preview of the pdf
        #Disabled for now
        '''previewButton=Buttons(self, text="Preview")
        previewButton.setSide(RIGHT)
        previewButton.setPads(5, 5)'''
        
        
        #Entry to get input from the user
        inputTextBox=TextBox(frame, width=75, text='Enter PDF to be searched')
        inputTextBox.setAnchor(NW)
        inputTextBox.setSide(TOP)
        inputTextBox.setPads(10, 10)
        inputTextBox.bind('<FocusIn>', inputTextBox.on_entry_click) #Delete the default text once the user clicks the box for the first time

        i=IntVar() #Variable which stores the option selected by the radiobutton

        #Radio buttons to limit the search results
        OptionRadioButton1=RadioButtons(frame, '10 per', side=TOP, anchor=NW, pady=0, padx=5, variable=i, value=1)
        OptionRadioButton2=RadioButtons(frame, '20 per', side=TOP, anchor=NW, pady=0, padx=5, variable=i, value=2)
        OptionRadioButton3=RadioButtons(frame, '30 per', side=TOP, anchor=NW, pady=0, padx=5, variable=i, value=3)

        #List box in which the search results are to be displayed

        ResultsListbox=List_Box(frame, mode=SINGLE, height=11)
        ResultsListbox.setAnchor(NW)
        ResultsListbox.setSide(TOP)
        ResultsListbox.setPads(10, 5)

        def get_val():
            """Function to search the input and list them"""
            global title_dict
            get_string=inputTextBox.get()
            get_val=v.get()
            scrap(str(get_string),int(get_val))
            decode_store(int(get_val))
            ResultsListbox.delete(0,END)
            for i in title_dict.iterkeys():
                ResultsListbox.add_val(i)

        def download_file():
            """Function to download the selected file"""
            global title_dict
            title=ResultsListbox.get(ResultsListbox.curselection())
            link=title_dict[title]
            file_dl=urllib.URLopener()
            file_dl.retrieve(link,str(title)+".pdf")

        def save_results():
            """Function to save the current list"""
            global title_dict
            conn=sql.connect('output.db')
            conn.execute("DELETE FROM OUTPUT")
            for k,v in title_dict.iteritems():
                conn.execute("INSERT INTO OUTPUT VALUES (?,?);",(k,v))
            conn.commit()
            conn.close()

        def get_results():
            """Function to get the saved list"""
            global title_dict
            title_dict.clear()
            conn=sql.connect('output.db')
            for i,j in conn.execute("SELECT TITLE,LINK FROM OUTPUT;"):
                title_dict[i]=j
            conn.close()
            ResultsListbox.delete(0,END)
            for i in title_dict.iterkeys():
                ResultsListbox.add_val(i)

        #Button to initiate search
        SearchButton = Buttons(frame, text="Search",command=get_val)
        SearchButton.setSide(TOP)
        SearchButton.setPads(10, 0)    
        SearchButton.setAnchor(NE)

        #Buttons at the bottom of the dialog box
        downloadButton = Buttons(self, text="Download",command=download_file)
        downloadButton.setSide(RIGHT)
        downloadButton.setPads(5, 5)

        #Button to save the results of the current search
        SaveButton = Buttons(self, text="Save results",command=save_results)
        SaveButton.setSide(RIGHT)
        SaveButton.setPads(5, 5)

        #Button to show the previously saved search results
        viewButton=Buttons(self, text="Show saved results",command=get_results)
        viewButton.setSide(RIGHT)
        viewButton.setPads(5, 5)

def main():
    #Dialog box
    root = Tk()
    root.geometry("400x370")
    
    root.resizable(width=False, height=False)#Disabling maximize button
    root.update_idletasks()
    
    #Setting the dialog box at the center of the screen
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    size = tuple(int(_) for _ in root.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    root.geometry("%dx%d+%d+%d" % (size + (x, y)))

    
    #Initializing the various components of the dialog box
    app = Layout(root)
    root.mainloop()

main()
