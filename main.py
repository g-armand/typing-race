import functools                            #functools.partial in order to create unique functions and objects, way to avoid specific issues in the program
import tkinter as tk                        #GUI module
import time
import threading

class Window(tk.Tk):
    def __init__(self):
        super(Window, self).__init__()

        self.title('Pw Manager')
        self.geometry('1000x500')
        self.config(background = '#f2f2f2')

        self.start = True
        self.position = 0
        self.txt = "Le Conseil a exprimé le souhait."
        self.string = self.txt.split(' ')
        self.count = 0

        #go to start menu
        self.startmenu()

    def newframe(self):

        #if it is the first time we need a frame, we skip to the frame creation step
        if self.start:
            self.start = False
            pass

        #if the mainframe has already been created, we destroy it in order to create a blank frame, ready to be used
        elif not self.start:
            self.mainframe.destroy()
            self.mainborder.destroy()

        #creation of the blank frame
        self.mainborder = tk.Frame(self, height = 405, width = 805, bg = '#a97acc', bd = 3, highlightcolor = "#adcbef")
        self.mainborder.pack(expand = 'True')
        self.mainframe = tk.Frame(self.mainborder, height = 400, width = 800, bg = '#f2f2f2', bd = 3, highlightcolor = "#adcbef")
        self.mainframe.pack(expand = 'True', fill = "both")

    def startmenu(self):
        self.newframe()

        gamelabel = tk.Label(self.mainframe, width = 80, height = 10 , bg = '#f2f2f2', text = "TYPING RACE!!!", font = (20), fg = "#a97acc")
        gamelabel.grid(row = 0)

        startbutton = tk.Button(self.mainframe, width = 15, height = 5, bg = '#a97acc', command = self.gamemenu)
        startbutton.grid(row = 1)

    def gamemenu(self):

        self.timertext = tk.StringVar(self, "0:00")
        self.timerlabel = tk.Label(self, textvariable = self.timertext, font = 20, bg ="#3EA64C")
        self.timerlabel.pack(pady = 50, padx = 50, anchor = "ne")
        self.newframe()

        textmessage = tk.Message(self.mainframe, width = 800, bg = '#f2f2f2', text = self.txt, font = (20), fg = "#a97acc")
        textmessage.grid(row = 0)

        self.word = tk.StringVar(self, self.string[self.count])
        self.wordlabel = tk.Label(self.mainframe, width = 80, bg = '#f2f2f2', textvariable = self.word, fg = "#a97acc")
        self.wordlabel.grid(row = 1, pady = 20)

        self.assertcommand = (self.register(self.assertion), "%s", "%S")


        self.wordentry = tk.Entry(self.mainframe, width = 40, bg = '#f2f2f2',  fg = "#a97acc", validate = "key", validatecommand = self.assertcommand)
        self.wordentry.grid(row = 2, pady = 10)

        self.SVl = tk.StringVar(self, self.position)
        self.l = tk.Label(self.mainframe, textvariable = self.SVl)
        self.l.grid(row = 1, column = 2, pady = 20)

        self.threadtimer = threading.Thread(self.timer()).start()

    def startgame(self):
        pass

    def assertion(self, typingword, letter):


        word = self.string[self.count]
        typedword = typingword + letter

        self.SVl.set(self.position)
        self.l.update()

        try:
            word[self.position]
        except IndexError:
            self.position -= 1


        if typedword == word + " " or typedword == (word + ","):
            self.position = 0
            self.count += 1
            self.nextword()
            return True

        elif typedword == self.string[-1]:
            self.stoptimer()
            #self.wordentry.configure(validate = "none")
            return True

        elif letter == word[self.position]:
            self.position += 1
            return True


        else:
            return False




    def nextword(self):

        self.wordentry.destroy()
        self.wordentry = tk.Entry(self.mainframe, width = 40, bg = '#f2f2f2',  fg = "#a97acc", validate = "key", validatecommand = self.assertcommand)
        self.wordentry.grid(row = 2, pady = 10)
        self.wordentry.focus()

        self.word.set(self.string[self.count])
        self.wordlabel.update()

    def timer(self):

        timer = time.time()
        chrono = 0.0

        while True:
            time.sleep(0.01)
            a = time.time()
            chrono = a - timer
            chrono = str(chrono)
            self.timertext.set(str(chrono[:4]))
            chrono = float(chrono)
            self.timerlabel.update()

    def stoptimer(self):
            score = self.timertext.get()
            self.wordentry.delete(0, "end")
            self.timerlabel.destroy()
            self.SVl.set(score)
            self.l.update()





window = Window()
window.mainloop()
