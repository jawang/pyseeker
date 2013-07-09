import Tkinter as tk
import os
import csv
import tkFileDialog
import ScrolledText
from datetime import *
import re

class block:
    def __init__(self):
        self.message = ''
        self.color = ''
        self.status = ''
        self.linenumber = 0
        self.time = ''
        self.application = ''
        self.opcode = 0
        self.machine = ''

class Application(tk.Frame):
    def __init__(self,master=None):

        tk.Frame.__init__(self,master)

        self.grid()
        self.blocks = []
        self.createWidgets()

    def createWidgets(self):
        # SEARCH BOX #############################
        self.searchBox = tk.LabelFrame(self,width=275,height=225,
                                  padx=10,pady=10,relief='sunken',bd=1,
                                       text='Search Box')
        self.searchBox.grid_propagate(0)
        self.searchBox.grid(row=0,column=0)
        
        # ITX INPUT
        self.itxText = tk.Label(self.searchBox,text='ITX: ')
        self.itxText.grid(column=0,row=0)

        self.itx = tk.StringVar()
        self.itxBox = tk.Entry(self.searchBox,textvariable=self.itx)
        self.itxBox.grid(column=1,row=0,sticky=tk.W)

        tk.Frame(self.searchBox,height=20).grid(row=1,column=0)

        # FILE CHOOSER
        self.bChoose = tk.Button(self.searchBox,text='Choose file',
                                 command=self.getFile)
        self.bChoose.grid(column=0,row=2,sticky=tk.W+tk.N,padx=5)

        self.fileText = tk.Text(self.searchBox,
                                          width=20,height=3)
        self.fileText.grid(column=1,row=2)

        tk.Frame(self.searchBox,height=20).grid(row=3,column=0)

        # INTERVAL
        self.choices = tk.StringVar()
        self.optionslist = ["12AM - 2AM","2AM - 4AM"," 4AM - 6AM",
                       " 6AM - 8AM"," 8AM - 10AM"," 10AM - 12PM",
                       "12PM - 2PM"," 2PM - 4PM"," 4PM - 6PM",
                       " 6PM - 8PM"," 8PM - 10PM"," 10PM - 12AM"]
        
        self.optionsdict = {}

        for i in range(len(self.optionslist)):
            self.optionsdict[self.optionslist[i]] = 2*i

        #print self.optionsdict
        
        self.choices.set(self.optionslist[0])
        self.interval = tk.OptionMenu(self.searchBox,
                                      self.choices,
                                      *tuple(self.optionslist))
        
        self.interval.grid(column=0,row=4,columnspan=2)
        
        tk.Frame(self.searchBox,height=20).grid(row=5,column=0)

        # GO BUTTON
        self.go = tk.Button(self.searchBox,text='Search',
                            command=self.go)
        self.go.grid(row=6,column=0,columnspan=2)

        # FILTER BOX #############################
        self.filterBox = tk.LabelFrame(self,width=275,height=225,
                                  padx=10,pady=10,relief='sunken',bd=1,
                                       text='Filter Box')
        self.filterBox.grid_propagate(0)
        self.filterBox.grid(row=1,column=0)

        # KEYWORD FILTER #########################
        self.keyText = tk.Label(self.filterBox,text='Keyword: ')
        self.keyText.grid(column=0,row=0)

        self.filterword = tk.StringVar()
        self.keyBox = tk.Entry(self.filterBox,textvariable=self.filterword)
        self.keyBox.grid(column=1,row=0,sticky=tk.W,columnspan=2)

        tk.Frame(self.filterBox,height=20).grid(row=1,column=0)

        # OPCODE FILTER ##########################
        self.var1 = tk.IntVar()
        self.var1.set(1)
        tk.Checkbutton(self.filterBox, text="Opcode 1,2",
                       variable=self.var1).grid(row=2, column=0)
        self.var2 = tk.IntVar()
        self.var2.set(1)
        tk.Checkbutton(self.filterBox, text="Opcode 3,4,5",
                       variable=self.var2).grid(row=2, column=1)
        self.var3 = tk.IntVar()
        self.var3.set(1)
        tk.Checkbutton(self.filterBox, text="Other",
                       variable=self.var3).grid(row=2, column=2)

        tk.Frame(self.filterBox,height=20).grid(row=3,column=0)

        # MAIN/BACKUP FILTER #####################
        self.varA = tk.IntVar()
        self.varA.set(1)
        tk.Checkbutton(self.filterBox, text="A",
                       variable=self.varA).grid(row=4, column=0,sticky=tk.W)
        self.varB = tk.IntVar()
        self.varB.set(1)
        tk.Checkbutton(self.filterBox, text="B",
                       variable=self.varB).grid(row=4, column=1,sticky=tk.W)
        
        tk.Frame(self.filterBox,height=20).grid(row=5,column=0)

        # FILTER BUTTON
        self.filter = tk.Button(self.filterBox,text='Filter',
                            command=self.filterboxes)
        self.filter.grid(row=6,column=0,columnspan=3)

        # QUICK VIEW #############################
        self.quickview = tk.LabelFrame(self,width=520,height=300,
                                  padx=10,pady=10,relief='sunken',bd=1,
                                       text='Quickview')
        self.quickview.grid_propagate(0)
        self.quickview.grid(row=0,column=1)
        self.scrollview = tk.Canvas(self.quickview,width=475,height=250)
        self.scrollview.grid(row=0,column=0)
        
        self.scrollframe = tk.Frame(self.scrollview)
        self.scrollview.create_window(0,0,window=self.scrollframe,anchor='nw')
        self.scrollY = tk.Scrollbar(self.quickview,orient=tk.VERTICAL,
                                    command=self.scrollview.yview)

        self.scrollview['yscrollcommand'] = self.scrollY.set
        
        # DETAILED INFO ##########################
        self.info = tk.LabelFrame(self,width=520,height=290,
                                  padx=10,pady=10,relief='sunken',bd=1,
                                  text='Message View')
        self.info.grid_propagate(0)
        self.info.grid(row=1,column=1)
        self.info.grid_rowconfigure(0, weight=1)
        self.info.grid_columnconfigure(0, weight=1)
        
        # INFO BOX ###############################
        #self.infotext = tk.StringVar()
        self.infobox = tk.Text(self.info)
        self.infobox.grid(sticky=tk.W+tk.E+tk.S+tk.N)

    def filterboxes(self):
        self.clearboxes()
        self.drawboxes()
        
    def clearboxes(self):
        self.scrollframe.destroy()
        self.scrollframe = tk.Frame(self.scrollview)
        self.scrollview.create_window(0,0,window=self.scrollframe,anchor='nw')
        try:
            del self.buttons
        except Exception:
            ''
        self.buttons = []

    def drawboxes(self):
        for j in range(len(self.blocks)):
            # filter keyword
            if self.filterword.get().lower() in self.blocks[j].message.lower():
                # filter opcode
                if (self.blocks[j].opcode == 0 and self.var3.get()) or \
                   (self.blocks[j].opcode == 1 and self.var1.get()) or \
                   (self.blocks[j].opcode == 3 and self.var2.get()):
                    # filter main/backup
                    if ('A' in self.blocks[j].machine and self.varA.get()) or \
                       ('B' in self.blocks[j].machine and self.varB.get()):
                        self.buttons.append(
                            tk.Button(self.scrollframe,text=self.blocks[j].time,
                                         command=lambda j=j:self.displayinfo(j),
                                      bg=self.blocks[j].color))

        for j in range(len(self.buttons)):
            self.buttons[j].grid(row=j/7,column=j%7,sticky=tk.E+tk.W)

        self.scrollframe.update_idletasks()
        self.scrollview.configure(scrollregion=self.scrollview.bbox(tk.ALL))
        self.scrollY.grid(row=0,column=1,sticky=tk.N+tk.S+tk.E)
        
    def go(self):
        self.infobox.delete(1.0,tk.END)
        del self.blocks
        self.blocks = []
        self.clearboxes()

        # open csv file in reader
        i = 1
        with open(self.filename,'rb') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                self.process(line,i)

                i += 1
                #if i == 2000:
                    #break

            # display blocks
            self.drawboxes()

    def displayinfo(self,j):
        self.infotext = 'Application: ' + self.blocks[j].application +\
                          '\n\nWorkstation: ' + self.blocks[j].machine +\
                          '\n\nMessage: ' + self.blocks[j].message
        self.infobox.delete(1.0,tk.END)
        self.infobox.insert(tk.INSERT,self.infotext)
        
    def getFile(self):
        self.filename=tkFileDialog.askopenfilename(#initialdir='C:\\',
                                                   title='Log File')
        self.fileText.delete(1.0,tk.END)
        self.fileText.insert(tk.INSERT,self.filename)

    def process(self,line,i):
        # filter for ITX and SCTE
        if len(line) == 8 and \
           'ITX'+self.itx.get() in line[2] and \
           ('SCTE' in line[5] or 'take initiated' in line[5].lower() or\
            'take next sequence' in line[5].lower()):
            
            pattern = '([0-2][0-9]\:[0-5][0-9]\:[0-9]{2}\.[0-9]{1,2})'
            prog = re.compile(pattern)
            time = prog.findall(line[5])[0]
            
            # Filter for time
            if int(time[0:2]) - self.optionsdict[self.choices.get()] == 0 or\
               int(time[0:2]) - self.optionsdict[self.choices.get()] == 1:
            
                # Make block
                newblock = block()
                newblock.time = time
                newblock.message = line[5]
                newblock.line = i
                newblock.application = line[1]
                newblock.machine = line[2]
                if 'op code 0' in newblock.message or \
                   'Opcode 0' in newblock.message:
                    newblock.color = 'gray'
                    newblock.opcode = 0
                elif 'op code 1' in newblock.message or \
                   'Opcode 1' in newblock.message:
                    newblock.color = 'green'
                    newblock.opcode = 1
                elif 'op code 2' in newblock.message or \
                   'Opcode 2' in newblock.message:
                    newblock.color = 'green'
                    newblock.opcode = 1
                elif 'op code' in newblock.message or \
                   'Opcode' in newblock.message:
                    newblock.color = 'red'
                    newblock.opcode = 3
                else:
                    if 'ignored' in newblock.message.lower():
                        newblock.color = 'gray'
                        newblock.opcode = 0
                    elif 'take initiated' in newblock.message.lower():
                        newblock.color = 'yellow'
                        newblock.opcode = 1
                    elif 'take next sequence' in newblock.message.lower():
                        newblock.color = 'yellow'
                        newblock.opcode = 1
                    elif 'addauxelement' in newblock.message.lower():
                        newblock.opcode = 1
                        newblock.color = 'yellow'
                    else:
                        newblock.color = 'gray'
                        newblock.opcode = 0
                if 'ignor' in newblock.message.lower():
                        newblock.color = 'gray'
                        newblock.opcode = 0
                        
                self.blocks.append(newblock)

# MAIN PROCESS
root = tk.Tk()
root.geometry('800x600')
root.resizable(0,0)

app = Application()

app.master.title('SCTE Seeker')

app.mainloop()
