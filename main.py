import functools                            #functools.partial in order to create unique functions and objects, way to avoid specific issues in the program
import tkinter as tk                        #GUI module
import time
import threading                            #allows the program to run two or more tasks simultaneously (eg. timer)
import sqlite3                              #will store scores in sql3 database
import os.path                              #will check if the database exists or not
import matplotlib.pyplot as plt             #will draw graphs, to show stats on typing pace enhancements

#check if the sql database exists, creates it if not and sets up the variables "FICHIER" "CONN" and "CUR"
if os.path.isfile("testbd.sq3"):
    FICHIER = "testbd.sq3"
    CONN = sqlite3.connect(FICHIER)
    CUR = CONN.cursor()
else:
    FICHIER = "testbd.sq3"
    CONN = sqlite3.connect(FICHIER)
    CUR = CONN.cursor()
    CUR.execute("CREATE TABLE scores (try INTEGER, wordperminute REAL)")


class Window(tk.Tk):
    def __init__(self):
        super(Window, self).__init__()

        #Window's config
        self.title('Pw Manager')
        self.geometry('1000x500')
        self.config(background = '#f2f2f2')

        #variables
        self.start = True
        self.position = 0
        self.txt = "Le Conseil a exprimé le souhait."
        self.string = self.txt.split(' ')
        self.count = 0
        self.words_per_minute = 0.0

        #go to start menu
        self.startmenu()

    def newframe(self):
        """
        destroys the old frame and its content, sets a new, blank and standadized frame
        """

        #if it is the first time we need a frame, we skip to the frame creation step
        if self.start:
            self.start = False
            pass

        #if the mainframe has already been created, we destroy it in order to create a blank frame
        elif not self.start:
            self.mainframe.destroy()
            self.mainborder.destroy()

        #creation of the blank frame
        self.mainborder = tk.Frame(self, height = 405, width = 805, bg = '#a97acc', bd = 3, highlightcolor = "#adcbef")
        self.mainborder.pack(expand = 'True')
        self.mainframe = tk.Frame(self.mainborder, height = 400, width = 800, bg = '#f2f2f2', bd = 3, highlightcolor = "#adcbef")
        self.mainframe.pack(expand = 'True', fill = "both")

    def startmenu(self):
        """
        main menu, displays the title and a button to start the game
        """
        self.newframe()

        #title of the game
        tk.Label(self.mainframe, width = 80, height = 10 , bg = '#f2f2f2', text = "TYPING RACE!!!", font = (20), fg = "#a97acc").grid(row = 0, columnspan = 2)

        #button to start the game
        tk.Button(self.mainframe, width = 15, height = 5, text = "game", bg = '#a97acc', command = self.gamemenu).grid(row = 1, column = 0)

        #button to show the stats
        tk.Button(self.mainframe, width = 15, height = 5, text = "stats", bg = '#a97acc', command = self.stats).grid(row = 1, column = 1)

    def gamemenu(self):
        """
        Game window, displays:
        - a timer which starts once the window is opened and stops when the sentence is completed
        -
        """
        #timer
        self.timertext = tk.StringVar(self, "0:00")
        self.timerlabel = tk.Label(self, textvariable = self.timertext, font = 20, bg ="#3EA64C")
        self.timerlabel.pack(pady = 50, padx = 50, anchor = "ne")

        self.newframe()

        #entire sentence
        textmessage = tk.Message(self.mainframe, width = 800, bg = '#f2f2f2', text = self.txt, font = (20), fg = "#a97acc")
        textmessage.grid(row = 0)

        #the word that needs to be typed
        self.word = tk.StringVar(self, self.string[self.count])
        self.wordlabel = tk.Label(self.mainframe, width = 80, bg = '#f2f2f2', textvariable = self.word, fg = "#a97acc")
        self.wordlabel.grid(row = 1, pady = 20)

        #entry, incorporates a validation command
        self.assertcommand = (self.register(self.assertion), "%s", "%S")
        self.wordentry = tk.Entry(self.mainframe, width = 40, bg = '#f2f2f2',  fg = "#a97acc", validate = "key", validatecommand = self.assertcommand)
        self.wordentry.grid(row = 2, pady = 10)

        #temporaire
        self.SVl = tk.StringVar(self, self.position)
        self.l = tk.Label(self.mainframe, textvariable = self.SVl)
        self.l.grid(row = 1, column = 2, pady = 20)

        #allows the timer to run alongside the program
        self.threadtimer = threading.Thread(self.timer()).start()

    def startgame(self):
        pass

    def assertion(self, typingword, letter):
        """
        entry's validation command. Allows to type the correct letter by returning True, or blocks it by returning False.
        """

        #'word' determines the word that needs to be typed, typedword contains the word already typed in the entry + the enter that will be evaluated
        word = self.string[self.count]
        typedword = typingword + letter

        #temporaire
        self.SVl.set(self.position)
        self.l.update()

        #avoid IndexError
        try:
            word[self.position]
        except IndexError:
            self.position -= 1

        #if the word is complete + ' ', we go to the next word in the sentence
        if typedword == word + " " or typedword == (word + ","):
            self.position = 0
            self.count += 1
            self.nextword()
            return True

        #if the word is complete and correspond to the last word of the sentence
        elif typedword == self.string[-1]:
            self.stoptimer()
            return True

        #if the letters correspond to the good letter
        elif letter == word[self.position]:
            self.position += 1
            return True

        #if the letter is not valid
        else:
            return False




    def nextword(self):
        """
        picks the next word that needs to be typed in the sentence,
        also destroys the entry to recreate it immediately because the validation command is buggy if it remains untouched.
        """

        #recreation of the entry, set focus on it
        self.wordentry.destroy()
        self.wordentry = tk.Entry(self.mainframe, width = 40, bg = '#f2f2f2',  fg = "#a97acc", validate = "key", validatecommand = self.assertcommand)
        self.wordentry.grid(row = 2, pady = 10)
        self.wordentry.focus()

        #go to next word and displays it
        self.word.set(self.string[self.count])
        self.wordlabel.update()

    def timer(self):
        """
        once called, it runs a timer until the timer is stopped with self.stoptimer() (when the sentence is completed)
        """
        #set variables
        timer = time.time()
        chrono = 0.0

        #infinite loop
        while True:
            time.sleep(0.01)
            a = time.time()
            chrono = a - timer
            chrono = str(chrono)
            self.timertext.set(str(chrono[:4]))
            chrono = float(chrono)
            self.timerlabel.update()

    def stoptimer(self):

        score = float(self.timertext.get())
        self.wordentry.delete(0, "end")

        self.words_per_minute = (60/score) * len(self.string)

        self.SVl.set(str(score))
        self.l.update()

        self.store_in_database()

    def store_in_database(self):
        """
        store the new score in the sql database. in the db, we access the 'scores' table which contains:
        - try(the number of times the game has been completed)
        - wordperminute (the ratio of word/minute)
        """

        #getting the max number of trials from the db, adding one to it and prepare to store it in db
        max_tries = CUR.execute("SELECT MAX(try) from scores") #returns a None object if the score table is empty
        result = max_tries.fetchall()

        if not result[0][0]:
            tries = 1
        else:
            tries = result[0][0] + 1

        #store in db
        newscore = f"({tries}, {self.words_per_minute})"
        command = "INSERT INTO scores (try, wordperminute) VALUES " + newscore
        CUR.execute(command)
        CONN.commit()

    def stats(self):
        x = []
        y = []

        CUR.execute("SELECT try from scores")
        x_datas = CUR.fetchall()
        for index, data in enumerate(x_datas):
            x.append(x_datas[index][0])

        CUR.execute("SELECT wordperminute from scores")
        y_datas = CUR.fetchall()
        for index, data in enumerate(y_datas):
            y.append(y_datas[index][0])

        #create the graph
        plt.plot(x, y)

        plt.xlabel("tries")
        plt.ylabel("word/minute")

        plt.show()





window = Window()
window.mainloop()

