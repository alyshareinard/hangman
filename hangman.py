#-----------------------------------------------------
#                          
#   hangman.py                   
#----------------------------------------------------- 
#                          
#   Loads a random word from a list of allowed    
#   words, specified in an input file, and starts 
#   the game for you!  
#   This game is made for smaller children, who aren't as
#   good at the game and mostly only know short words, so the
#   game removes 5 letters at a time for the last two turns
#   making it easier to win.
#
#   Feel free to use/modify as you like.
#               
#   Author: Alysha Reinard (alysha.reinard@gmail.com)        
#                           
#-------------------------------------------------------

# Import our required libraries and functions
from random import randint
try:
    from tkinter import *
except ImportError:
    from Tkinter import *
import os
from random import randint

# getInfile()
#
# Gets a text file containing words to be chosen by the Hangman program
def getInfile():

    current_dir=os.getcwd()
    infile_name=current_dir+"/wordlist.txt"

    try:
        # First, we check for a file called "wordlist.txt". If it exists in the same directory
        #   as the Hangman program, then we use this file as our word list automatically    
        with open(infile_name, 'r'): infile_name = 'wordlist.txt'
    except IOError:
        if sys.version_info[0] < 3:
            infile_name = raw_input('Please specify a text file containing a list of words for the Hangman game to choose from (include the full file path if the file is in a different directory than the Hangman program): ')
        else:
            infile_name = input('Please specify a text file containing a list of words for the Hangman game to choose from (include the full file path if the file is in a different directory than the Hangman program): ')
        found_file = False
        while found_file == False:
            print(infile_name)
            print(os.getcwd())
                # If the user specifies a file name of a file that cannot be found, we keep asking for
            #   a valid input file until a valid one is specified
            while not(found_file):
                try:
                    with open(infile_name, 'r'): found_file = True
                except IOError:
                    infile_name = input('\n{0} was not found!\n\nPlease try again, or specify a different file (include the full file path if the file is in a different directory than the Hangman program): '.format(infile_name))

    return infile_name


# Chooses a word randomly from the list of words taken from the input file
def chooseWord(infile_name):
    infile = open(infile_name, 'r')
    wordlist = infile.readlines()
    total_words = len(wordlist)
    random_num = randint(0, total_words - 1)

    chosen_word = wordlist[random_num].replace('\n', '')
    chosen_word=chosen_word.replace(" ", '')
    word_len = len(chosen_word)
    return chosen_word, word_len


class Hangman(Frame):
    def __init__(self):
        self.root=Tk()
        self.root.geometry("1000x500")
        Frame.__init__(self, self.root)
        self.root.bind('<Key>', self.key)
        self.hmd=Canvas(self.root, width=200, height=300) #hangman drawing
        self.hmd.pack()
        self.answer_display=Label(self.root, text=self.grid)
        self.answer_display.pack()
        self.message=Label(self.root, text="")
        self.message.pack(pady=20)
        self.letters_text=Label(self.root, text="")
        self.letters_text.pack()
        self.letters_display=Label(self.root, text="")
        self.letters_display.pack()
        
        self.create_widgets()
        
    def quit(self):
        self.root.destroy()

        
    def create_widgets(self):

        self.hmd.create_line(20, 280, 190, 280)

        self.infile_name = getInfile()

        # Choose a word at random from the acquired word list
        self.word, self.word_len = chooseWord(self.infile_name)

        # Build the grid of empty spaces, one space for each letter of the chosen word
        self.grid = '__'
        for i in range(self.word_len - 1):
            self.grid = self.grid + ' __'

        self.answer_display.configure(text=self.grid)

        self.message.configure(text="Let's play! Guess a letter to see if it's in the word.")


        #Initialize the letters
        self.letters=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        self.letters_text.configure(text="Remaining letters")

        self.letters_display.configure(text=self.letters)

        self.guessed_letters=[]
        self.strikes=0
        self.game_over=0



    def drawPiece(self):

        if self.strikes == 1:
            # Strike 1: Draw the post
            self.hmd.create_line(120, 280, 120, 80)
            self.hmd.create_line(120, 80, 50, 80)
            self.hmd.create_line(50, 80, 50, 100)
            
        elif self.strikes == 2:
            # Strike 2: Draw the head
            self.hmd.create_oval(35, 100, 65, 130)

        elif self.strikes == 3:
            # Strike 3: Draw the right eye
            self.hmd.create_oval(43, 108, 48, 113)
            
        elif self.strikes == 4:
            #Strike 4: Draw the left eye
            self.hmd.create_oval(52, 108, 57, 113)
        elif self.strikes == 5:
            #Strike 5: Draw the nose
            self.hmd.create_oval(48, 115, 52, 120)

        elif self.strikes == 6:
            #Strike 4: Draw the mouth
            self.hmd.create_line(45, 123, 55, 123)
        elif self.strikes == 7:
            # Strike 3: Draw the torso
            self.hmd.create_line(50, 130, 50, 200)            
        elif self.strikes== 8:
            # Strike 4: Draw the left arm
            self.hmd.create_line(50, 150, 70, 170) 
        elif self.strikes== 9:
            # Strike 5: Draw the right arm
            self.hmd.create_line(50, 150, 30, 170)
        elif self.strikes== 10:
            # Strike 6: Draw the left leg
            self.hmd.create_line(50, 200, 70, 240)
        elif self.strikes == 11:
            # Strike 7: Draw the right leg
            self.hmd.create_line(50, 200, 30, 240)
            self.game_over=1
            self.win=0
            game=self.end_game()

    def end_game(self):
        self.hmd.delete("all")

        if self.win==1:

            # Draw winning picture
            self.hmd.create_oval(10, 50, 160, 200, fill="green")
            self.hmd.create_oval(55, 90, 75, 115, fill="black")
            self.hmd.create_oval(95, 90, 115, 115, fill="black")
            self.hmd.create_oval(80, 120, 90, 130, fill="black")
            self.hmd.create_arc(40, 100, 130, 180, start=180, extent=180, style=ARC, fill="black")
        if self.win==0:
            # draw losing picture
            self.hmd.create_oval(10, 50, 160, 200, fill="grey")
            self.hmd.create_oval(55, 90, 75, 115, fill="black")
            self.hmd.create_oval(95, 90, 115, 115, fill="black")
            self.hmd.create_oval(80, 120, 90, 130, fill="black")
            self.hmd.create_arc(40, 150, 130, 210, start=0, extent=180, style=ARC, fill="black")

        self.answer_display.configure(text=self.word)
        self.message.configure(text="Nice job! Thanks for playing.")
        self.message.pack()

        self.letters_text.configure(text="Play again? Y/N")
        self.letters_text.pack()

        self.letters_display.configure(text=" ")
        self.letters_display.pack()


        return 0
        
    def key(self, event):

        if event.char == event.keysym:
            self.guess=event.char

            if (self.game_over == 1):
                if self.guess=="Y" or self.guess=="y":

                    play_again="Y"
                    self.hmd.delete("all")
                    self.create_widgets()
                elif self.guess=="N" or self.guess=="n":
                    play_again="N"

                    self.quit()
                                       
            elif ((self.guess in self.word.lower()) and (self.guess.upper() in self.letters)): #if the guessed letter is in the word
                self.guessed_letters.append(self.guess)

                self.letters.remove(self.guess.upper())

                self.letters_display.pack_forget()
                self.letters_display.configure(text=self.letters)
                self.letters_display.pack()
                textval=self.guess.upper() + " was in the word! Good job! Guess again."
                self.message.configure(text=textval)

                self.grid=self.word
                for letter in self.word:
                    if (letter not in self.guessed_letters):
                        self.grid = self.grid.replace(letter, ' __ ')
                self.answer_display.configure(text=self.grid)


                        
                if self.grid == self.word:
                    self.game_over=1
                    self.win=1
                    game=self.end_game()

            elif ((self.guess not in self.word.lower()) and (self.guess.upper() in self.letters)): #if the guessed letter is not in the word, but is a possible letter

                self.letters.remove(self.guess.upper())
                self.guessed_letters.append(self.guess)
                textval="Too bad. "+self.guess.upper()+" is not in the word. Guess again."
                self.message.configure(text=textval)                
                self.strikes=self.strikes+1
                val=self.drawPiece()
                if self.strikes>8:
                    k=0
                    while len(self.letters)>len(self.word) and k<5:

                        val = randint(0, len(self.letters)-1)

                        if self.letters[val].lower() not in self.word:
                            self.guessed_letters.append(self.letters[val].lower())

                            self.letters.remove(self.letters[val])
                            k=k+1
                            
                self.letters_display.pack_forget()
                self.letters_display.configure(text=self.letters)
                self.letters_display.pack()
                
            elif (self.guess in self.guessed_letters): #if the guessed letter was already guessed
                textval=self.guess.upper() +" is not in the remaining letters. Check below and guess again."
                self.message.configure(text=textval)


    def start(self):
        self.root.mainloop()



Hangman().start()




