# Name: Eugene Shao
# CMS cluster login: eyshao

'''
The CS 1 final exam, Fall 2018, part 2.

The Dissembler puzzle game: Dissembler class.
'''

import locset as ls
import utils as u
import dissembler_rep as dr
import traceback as tb
import random
import time
from math import floor
from math import inf
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

# ---------------------------------------------------------------------- 
# Exception class.
# ---------------------------------------------------------------------- 

class InvalidMove(Exception):
    '''
    Instances of this class represent invalid attempted moves.
    '''
    pass

# ---------------------------------------------------------------------- 
# Helper functions.
# ---------------------------------------------------------------------- 

def random_color():
    '''Returns a random color string hex code that is NOT black
    
    Arguments: none
    
    Return: a string that is a random color hex code
    '''
    s = '#'
    for i in range(6):
        s += random.choice('123456789abcdef')
    
    return s

def color_update(rep):
    '''Assigns a random hex code color to each element of a rep and removed for
    the dissembler game.
    
    Arguments: a rep of locations and colors
    
    Return Value: a dictionary mapping letters to color hex codes
    '''
    rep = dr.invert_rep(rep)
    repColors = list(rep.keys())
    colorOutputs = {}
    
    for color in repColors:
        if color not in colorOutputs:
            colorOutputs[color] = random_color()
    
    return colorOutputs

def clear_rect(game):
    '''Clears all rectangles'''
    for rect in game.rectangles:
        game.c.delete(rect)
    game.rectangles = []
    game.objectid = [[0] * (game.ncols + 2) for i in range(game.nrows + 2)]

def clear_text(game):
    '''Clears all text in the first canvas'''
    for text in game.texts:
        game.c.delete(text)
    game.texts = []
    game.textid = [[0] * (game.ncols + 2) for i in range(game.nrows + 2)]

def clear_movetext(game):
    '''Clears all possible move texts'''
    for text in game.movetexts:
        game.cm.delete(text)
    game.movetexts = []    
    
def display_rep(game, nrows, ncols, rep, removed, colors):
    '''
    Print the dictionary representation of a puzzle.
    It will print as a sequence of lines, with each row as one line.  
    Each character in a row is either the letter corresponding to
    the color, or '.' if there is nothing at that location.
    Highlight the removed locations (if any) by capitalizing them.

    Arguments:
      rep: a dictionary mapping locations to one-character strings
      removed: ditto

    Return value: 
      none
    '''    
    assert type(nrows) is int and type(ncols) is int
    assert 0 <= nrows
    assert 0 <= ncols
    assert u.is_rep(rep)
    assert u.is_rep(removed)
    
    # Side length of a square
    s = game.blockLength
    
    clear_rect(game)
    clear_text(game)
    
    # First and last line horizontal
    for i in range(ncols + 2):
        r = game.c.create_rectangle(s * i + 10, 10,
                               s * (i + 1) + 10, s + 10, outline='black')
        r1 = game.c.create_rectangle(s * i + 10, s * (nrows + 1) + 10, 
                                s * (i + 1) + 10, s * (nrows + 2) + 10, \
                                outline='black')
        game.rectangles.append(r)
        game.rectangles.append(r1)
        game.objectid[0][i] = r
        game.objectid[nrows + 1][i] = r1
        if i > 0 and i < ncols + 1:
            t = game.c.create_text(s / 2 + s * i + 10, s / 2 + 10, \
                              text = str(i - 1))
            game.texts.append(t)
            game.textid[0][i] = t

    # Rest of lines
    for row in range(nrows):
        
        # First column
        r = game.c.create_rectangle(10, s * (row + 1) + 10,
                               s + 10, s * (row + 2) + 10, outline='black')
        t = game.c.create_text(s / 2 + 10, s * (row + 1.5) + 10, text=row)
        game.rectangles.append(r)
        game.texts.append(t)
        game.objectid[row + 1][0] = r
        game.textid[row + 1][0] = t
        
        # Middle columns
        for col in range(ncols):
            loc = (row, col)
            assert not (loc in rep and loc in removed)
            game.c.delete(game.objectid[row + 1][col + 1])
            game.c.delete(game.textid[row + 1][col + 1])            
            if loc in rep:
                r = game.c.create_rectangle(s * (col + 1) + 10, s * (row + 1) + 10,\
                                       s * (col + 2) + 10, s * (row + 2) + 10,\
                                       fill=colors[rep[loc]], outline='black')
                t = game.c.create_text(s * (col + 1.5) + 10, s * (row + 1.5) + 10, \
                                  text=rep[loc])
            elif loc in removed:
                r = game.c.create_rectangle(s * (col + 1) + 10, s * (row + 1) + 10,\
                                       s * (col + 2) + 10, s * (row + 2) + 10,\
                                       fill=colors[removed[loc]], \
                                       outline='black', dash=(5, 5))
                t = game.c.create_text(s * (col + 1.5) + 10, s * (row + 1.5) + 10, \
                                  text=removed[loc].upper())
            else:
                r = game.c.create_rectangle(s * (col + 1) + 10, s * (row + 1) + 10,\
                                       s * (col + 2) + 10, s * (row + 2) + 10,\
                                       outline='black')
                t = 0
            game.rectangles.append(r)
            game.texts.append(t)
            game.objectid[row + 1][col + 1] = r
            game.textid[row + 1][col + 1] = t
            
            # Last Column
            r = game.c.create_rectangle(s * (ncols + 1) + 10, s * (row + 1) + 10, \
                                   s * (ncols + 2) + 10, s * (row + 2) + 10, \
                                   outline='black')
            game.rectangles.append(r)
            game.objectid[row + 1][ncols + 1] = r
            
def display_moves(game, moves):
    global moveslist
    '''
    Print the set of possible moves in a readable form.

    Arguments:
      moves -- a list of possible moves
    Return value: none
    '''

    assert type(moves) is set
    for move in moves:
        assert u.is_move(move)

    # Convert the moves into a list.
    moves = list(moves)
    moves.sort()
    moveslist = moves
    
    for text in game.movetexts:
        game.cm.delete(text)
    game.movetexts = []
    
    t = game.cm.create_text(50, 30, text='Possible Moves:')
    game.movetexts.append(t)
    
    if moves == []:
        messagebox.showwarning('Error', 'No moves are available!')
        t = game.cm.create_text(50, 50, text='None')
        game.movetexts.append(t)
    else:        
        for i in range(len(moves)):
            s = f'{i}: '
            ((r1, c1), (r2, c2)) = moves[i]
            s += f'({r1}, {c1}) -- ({r2}, {c2})'
            t = game.cm.create_text(50 + 100 * divmod(i, 15)[0], \
                                    50 + 20 * divmod(i, 15)[1], text=s)
            game.movetexts.append(t)
            
def clicked_undo():
    global undosmade
    rsp = messagebox.askyesno('To undo or not to undo - that is the question'\
                              , 'Are you sure you want to undo?')
    if rsp:
        game.undo()
        undosmade.set(undosmade.get() + 1)

def quit_game():
    rsp = messagebox.askyesno('Warning! ragequit detected!',\
                              'Are you sure you want to quit?')
    if rsp:
        m1 = messagebox.showinfo('Goodbye!', 'It was fun playing with you!')
        quit()

def new_puzzle():
    game.end = False
    
    if not game.firstTime:
        rsp = messagebox.askyesno('Are you bored?', 'Time for a new puzzle?')
    
    if game.firstTime or rsp:
        level = simpledialog.askstring('Welcome', 'Please enter a level ' + \
                                    'from 1 to 20 to start the game.')
        
        # Reset everything
        clear_rect(game)
        clear_text(game)
        clear_movetext(game)
        game.history = []
        game.rep = {}
        game.removed = {}
        game.colors = {}
        game.objectid = []
        game.textid = []
        movesmade.set(0)
        undosmade.set(0)        
        
        game.choose_level(level)
    
    game.firstTime = False

def make_the_move():
    try:
        n = choicevar.get()
        if type(n) is int:
            try:
                game.make_move(moveslist[n])
            except ValueError as e:
                m = messagebox.showerror('Error', e)            
                game.display(moves=True)
            except IndexError as e:
                m = messagebox.showerror('Error', e)
                game.display(moves=True)
            except InvalidMove as e:
                m = messagebox.showerror('Error', e)
                game.display(moves=True)
            
            if game.removed == {}:
                msg = 'Invalid move (no squares removed): ' + \
                          f'{loc1} -- {loc2}'
                raise InvalidMove(msg)
            
            game.display(removed=True)
            movesmade.set(movesmade.get() + 1)
            game.display(moves=True)
            
            if game.rep == {}:
                win_sequence(game)
                m = messagebox.showinfo('Congratulations!', 'You win! ' + \
                                        'Give yourself a pat on the back! :)')
                return        
    except:
        m = messagebox.showerror('Error', 'Please enter a valid move!')

def mix_colors():
    '''Mixes the colors on the board.'''
    if not game.end:
        game.colors = color_update(game.rep)
        game.display(moves=True)

def win_sequence(game):
    game.end = True
    for i in range(5):
        clear_rect(game)
        clear_text(game)
        clear_movetext(game)
        
        for row in range(game.nrows + 2):
            for col in range(game.ncols + 2):
                r = game.c.create_rectangle(10 + game.blockLength * col, \
                                            10 + game.blockLength * row, \
                                            10 + game.blockLength * (col + 1),\
                                            10 + game.blockLength * (row + 1),\
                                            fill=random_color(), \
                                            outline='black')
                game.rectangles.append(r)
                game.objectid[row][col] = r
        game.c.after(500)
        game.c.update()
    
    randx1 = random.randint(1, floor(game.ncols / 2) + 1)
    randy1 = random.randint(1, floor(game.nrows / 2) + 1)
    randx2 = random.randint(floor(game.ncols / 2) + 2, game.ncols + 1)
    randy2 = random.randint(floor(game.nrows / 2) + 2, game.nrows + 1)
    
    game.c.delete(game.objectid[randy1][randx1])
    game.c.delete(game.objectid[randy2][randx2])
    game.c.delete(game.textid[randy1][randx1])
    game.c.delete(game.textid[randy2][randx2])
    
    r = game.c.create_rectangle(10 + game.blockLength * randx1, \
                                10 + game.blockLength * randy1, \
                                10 + game.blockLength * (randx1 + 1), \
                                10 + game.blockLength * (randy1 + 1), \
                                fill='#FFD700', outline='#C0C0C0')
    r1 = game.c.create_rectangle(10 + game.blockLength * randx2, \
                                10 + game.blockLength * randy2, \
                                10 + game.blockLength * (randx2 + 1), \
                                10 + game.blockLength * (randy2 + 1), \
                                fill='#C0C0C0', outline='#FFD700')
    t = game.c.create_text(10 + game.blockLength * (randx1 + 0.5), \
                                10 + game.blockLength * (randy1 + 0.5), \
                                text='You')
    t1 = game.c.create_text(10 + game.blockLength * (randx2 + 0.5), \
                                10 + game.blockLength * (randy2 + 0.5), \
                                text='Win')
    game.rectangles.append(r)
    game.rectangles.append(r1)
    game.texts.append(t)
    game.texts.append(t1)
    game.objectid[randy1][randx1] = r
    game.objectid[randy2][randx2] = r1
    game.textid[randy1][randx1] = t
    game.textid[randy2][randx2] = t1
    
    if game.highscore > movesmade.get():
        game.highscore = movesmade.get()
        highscore.set(game.highscore)
        m = messagebox.showinfo('Wow', 'New High Score!')
# ---------------------------------------------------------------------- 
# The Dissembler class.
# ---------------------------------------------------------------------- 

class Dissembler:
    '''
    Instances of this class allow users to play the Dissembler puzzle game
    with the computer interactively.
    '''

    def __init__(self, canvas, canvasMoves):
        '''
        Initialize the game.
        '''

        # Dimensions of a puzzle.
        self.nrows = 0
        self.ncols = 0

        # Internal representations of a puzzle.
        self.rep = {}
        self.removed = {}
        self.firstTime = True
        self.blockLength = 40
        self.c = canvas
        self.cm = canvasMoves
        self.highscore = inf
        self.end = False

        # Other bookkeeping information.
        self.history = []
        self.colors = {}
        self.objectid = []
        self.textid = []
        self.rectangles = []
        self.texts = []
        self.movetexts = []

    def load(self, puzzle):
        '''
        Load a puzzle from a string representation of the puzzle.
        Convert the string representation into a dictionary representation
        mapping (row, column) coordinates to colors.

        Arguments:
          puzzle -- a string representing the puzzle

        Return value: none
        '''

        rep = {}
        lines = puzzle.split()
        self.nrows = len(lines)
        self.ncols = len(lines[0])
        self.objectid = [[0] * (self.ncols + 2) for i in range(self.nrows + 2)]
        self.textid = [[0] * (self.ncols + 2) for i in range(self.nrows + 2)]

        for row in lines:
            assert len(row) == self.ncols

        for row in range(self.nrows):
            for col in range(self.ncols):
                color = lines[row][col]
                if color == '.':
                    continue
                rep[(row, col)] = color
        self.rep = rep
        self.colors = color_update(self.rep)
        assert u.is_rep(self.rep)

    def display(self, **kw):
        '''
        Print the board representation in an easy-to-read format.

        Keyword arguments:
          removed -- if True, show the removed locations as capital letters
          moves   -- if True, show the possible moves

        Return value: none
        '''
        rem = {}
        if 'removed' in kw and kw['removed']:
            rem = self.removed
        display_rep(game, self.nrows, self.ncols, self.rep, rem, self.colors)
        self.c.after(500)
        self.c.update()
        self.remove_blocks(game.removed)
        if self.rep != {} and 'moves' in kw and kw['moves']:
            display_moves(game, self.possible_moves())
    
    def choose_level(self, level):
        if level == None:
            m = messagebox.showinfo('Goodbye', "You don't want to play? " \
                                       + 'See you later then!')
            quit()
        else:
            try:
                level = int(level)
                if level > 0 and level < 21:
                    self.load(u.puzzles[int(level) - 1])
                    self.display(moves=True)
                else:
                    m = messagebox.showerror('Error', 'Level must be ' + \
                                            'between 1 and 20! (There ' + \
                                            'are only 20 levels available ' + \
                                            'at the moment :\ ')
                    new_puzzle()                
            except:
                m = messagebox.showerror('Error', "Something's not right...")
                new_puzzle()
        
    def make_move(self, move):
        '''
        Make a move.  If no colors are removed, unmake the move.

        Arguments:
          move -- a 2-tuple of locations

        Return value: none
        '''
        
        assert u.is_move(move)
        (loc1, loc2) = move

        if not ls.is_adjacent(loc1, loc2):
            msg = f'Invalid move: non-adjacent locations: {loc1}, {loc2}'
            raise InvalidMove(msg)

        if not loc1 in self.rep:
            msg = f'Invalid move: unoccupied location: {loc1}'
            raise InvalidMove(msg)
        
        if not loc2 in self.rep:
            msg = f'Invalid move: unoccupied location: {loc2}'
            raise InvalidMove(msg)

        # Save previous representation in history.
        self.history.append(self.rep.copy())

        # Make the move.
        self.rep = dr.swap_locations(self.rep, loc1, loc2)
        (self.rep, self.removed) = dr.remove_connected_groups(self.rep)

        # Unmake the move if nothing was removed.
        if self.removed == {}:
            self.undo()

    def remove_blocks(self, removed):
        '''Remove the specified blocks from the canvas and replace with empty
        blocks.'''
        # Take locations of need-removal locations
        locations = list(removed.keys())
        
        for x, y in locations:
            self.c.delete(self.objectid[x + 1][y + 1])
            self.c.delete(self.textid[x + 1][y + 1])
            
            # Creates blank
            r = self.c.create_rectangle(10 + self.blockLength * (y + 1), \
                                   10 + self.blockLength * (x + 1), \
                                   10 + self.blockLength * (y + 2), \
                                   10 + self.blockLength * (x + 2), \
                                   outline='black')
            
            # Adds blank to system
            self.rectangles.append(r)
            self.objectid[x + 1][y + 1] = r
            self.textid[x + 1][y + 1] = 0
        
    def undo(self):
        '''
        Undo a move.

        Arguments: none
        Return value: none
        '''

        if self.history != []:
            self.rep = self.history.pop()
        self.removed = {}
        # Otherwise, do nothing.
        self.display(moves=True)

    def possible_moves(self):
        '''
        Return a set of all the possible moves.
        '''

        return dr.possible_moves(self.rep, self.nrows, self.ncols)

if __name__ == '__main__':
    root = Tk()
    # Counter variables + important variables
    movesmade = IntVar()
    undosmade = IntVar()
    highscore = IntVar()
    choicevar = IntVar()
    moveslist = []
    
    # Creating frames
    gamegrid = LabelFrame(root, bg='', width=400, height=400, padx=5, pady=5)
    movesgrid = LabelFrame(root, width=360, height=400, padx=25, pady=25)
    makemovegrid = LabelFrame(root, width=400, height=100, padx=25, pady=25)
    btgrid = LabelFrame(root, width=400, height=100, padx=35, pady=25)
    infogrid = LabelFrame(root, width=150, height=100, padx=25, pady=25)
    
    # Creating the canvases
    c = Canvas(gamegrid, width=400, height=400)
    cm = Canvas(movesgrid, width=360, height=400)
    
    # Creating the buttons and text
    psbmoves = Label(makemovegrid, text='Select a move:')
    moveinput = Entry(makemovegrid, textvariable=choicevar)
    moveBt = Button(makemovegrid, text='Make the Move!', command=make_the_move)
    
    undoBt = Button(btgrid, text='Undo', command=clicked_undo)
    newPuzzleBt = Button(btgrid, text='New puzzle', command=new_puzzle)
    quitBt = Button(btgrid, text='Quit', command=quit_game)
    colorBt = Button(btgrid, text='CLICK ME!', command=mix_colors)
    
    movestxt = Label(infogrid, text='Moves played')
    movesdisp = Entry(infogrid, textvariable=movesmade)
    undotxt = Label(infogrid, text='Undos used')
    undodisp = Entry(infogrid, textvariable=undosmade)
    highscoretxt = Label(infogrid, text='High score')
    highscoredisp = Entry(infogrid, textvariable=highscore)
    highscore.set(inf)
    
    # Placing everything on the screen
    # Grid 1
    gamegrid.grid(row=0, column=0, columnspan=2, sticky=N+W+E+S)
    c.grid(sticky=N+W+E+S)
    
    # Grid 2
    movesgrid.grid(row=0, column=2, sticky=N+W+E+S)
    cm.grid(sticky=N+W+E+S)
    
    # Grid 3
    btgrid.grid(row=1, column=0, sticky=N+W+E+S)
    undoBt.grid(row=0, column=0, sticky=W+E)
    newPuzzleBt.grid(row=0, column=1, sticky=N+S)
    quitBt.grid(row=0, column=2, sticky=N+S)
    colorBt.grid(row=1, columnspan=3, sticky=N+W+E+S)
    
    # Grid 4
    makemovegrid.grid(row=1, column=1, sticky=N+W+E+S)
    psbmoves.grid(row=0, sticky=N+W+E+S)
    moveinput.grid(row=1, sticky=N+W+E+S)
    moveBt.grid(row=2, sticky=N+W+E+S)    
    
    # Grid 5
    infogrid.grid(row=1, column=2, sticky=N+W+E+S)
    movestxt.grid(row=0, column=0, sticky=N+W+E+S)
    movesdisp.grid(row=1, column=0, sticky=N+W+E+S)
    undotxt.grid(row=0, column=1, sticky=N+W+E+S)
    undodisp.grid(row=1, column=1, sticky=N+W+E+S)
    highscoretxt.grid(row=0, column=2, sticky=N+W+E+S)
    highscoredisp.grid(row=1, column=2, sticky=N+W+E+S)
    
    # Starting game
    game = Dissembler(c, cm)
    intro = messagebox.showinfo('Welcome', "IT'S TIME TO " + \
                                'D-D-D-D-D-D-D-D-DISSEMBLER!!!!!')
    new_puzzle()
    
    root.mainloop()
