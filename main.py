import functools                            #functools.partial in order to create unique functions and objects, way to avoid specific issues in the program
import tkinter as tk                        #GUI module

class Window(tk.Tk):
    def __init__(self):
        super(Window, self).__init__()

        self.title('Pw Manager')
        self.geometry('1000x500')
        self.config(background = '#000000')

        self.start = True
        self.position = 0
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
        self.mainborder = tk.Frame(self, height = 405, width = 805, bg = '#00ae0c', bd = 3, highlightcolor = "#adcbef")
        self.mainborder.pack(expand = 'True')
        self.mainframe = tk.Frame(self.mainborder, height = 400, width = 800, bg = '#000000', bd = 3, highlightcolor = "#adcbef")
        self.mainframe.pack(expand = 'True', fill = "both")

    def startmenu(self):
        self.newframe()

        gamelabel = tk.Label(self.mainframe, width = 80, height = 10 , bg = '#000000', text = "TYPING RACE!!!", font = (20), fg = "#00ae0c")
        gamelabel.grid(row = 0)

        startbutton = tk.Button(self.mainframe, width = 15, height = 5, bg = '#00ae0c', command = self.gamemenu)
        startbutton.grid(row = 1)

    def gamemenu(self):
        self.newframe()

        txt = "Le Conseil a exprimé le souhait que toutes les parties soutiennent l'accord en dix points pour la reprise des pourparlers intercommunautaires."

        textmessage = tk.Message(self.mainframe, width = 800, bg = '#000000', text = txt, font = (20), fg = "#00ae0c")
        textmessage.grid(row = 0)

        self.wordlabel = tk.Label(self.mainframe, width = 80, bg = '#000000', text = "word", fg = "#00ae0c")
        self.wordlabel.grid(row = 1, pady = 20)

        assertcommand = (self.register(self.assertion), "%s", "%S")

        self.wordentry = tk.Entry(self.mainframe, width = 80, bg = '#000000',  fg = "#00ae0c", validate = "key", validatecommand = assertcommand)
        self.wordentry.grid(row = 2, pady = 10)

    def assertion(self, typingword, letter):

        word = self.wordlabel.cget("text")
        typedword = typingword + letter


        if typedword == word + " " or typedword == word + ",":
            self.position = 0
            self.startmenu()
            return True

        elif letter == word[self.position]:
            self.position += 1
            return True

        else:
            return False

















window = Window()
window.mainloop()
