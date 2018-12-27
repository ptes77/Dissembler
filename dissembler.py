'''
The CS 1 final exam, Fall 2018, part 2.

The Dissembler puzzle game: Dissembler class.
'''

import locset as ls
import utils as u
import dissembler_rep as dr
import traceback as tb

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

def display_rep(nrows, ncols, rep, removed):
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

    s = '    ' + '0123456789'[:ncols] + '\n'
    s += '  +' + '-' * (ncols + 2) + '+\n'
    for row in range(nrows):
        s += f'{row} | '
        for col in range(ncols):
            loc = (row, col)
            # loc had better not be in both rep and removed.
            assert not (loc in rep and loc in removed)
            if loc in rep:
                s += rep[loc]
            elif loc in removed:
                s += removed[loc].upper()
            else:
                s += '.'
        s += ' |\n'
    s += '  +' + '-' * (ncols + 2) + '+\n'
    print(s)

def display_moves(moves):
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

    if moves == []:
        print('No moves are available!')
    else:
        print('Possible moves:\n')
        for i in range(len(moves)):
            s = f'{i}: '
            ((r1, c1), (r2, c2)) = moves[i]
            s += f'({r1}, {c1}) -- ({r2}, {c2})'
            print(s)
    print()

# ---------------------------------------------------------------------- 
# The Dissembler class.
# ---------------------------------------------------------------------- 

class Dissembler:
    '''
    Instances of this class allow users to play the Dissembler puzzle game
    with the computer interactively.
    '''

    def __init__(self):
        '''
        Initialize the game.
        '''

        # Dimensions of a puzzle.
        self.nrows = 0
        self.ncols = 0

        # Internal representations of a puzzle.
        self.rep     = {}
        self.removed = {}

        # Other bookkeeping information.
        self.history = []

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

        for row in lines:
            assert len(row) == self.ncols

        for row in range(self.nrows):
            for col in range(self.ncols):
                color = lines[row][col]
                if color == '.':
                    continue
                rep[(row, col)] = color
        self.rep = rep
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
        display_rep(self.nrows, self.ncols, self.rep, rem)
        if self.rep != {} and 'moves' in kw and kw['moves']:
            display_moves(self.possible_moves())

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

    def possible_moves(self):
        '''
        Return a set of all the possible moves.
        '''

        return dr.possible_moves(self.rep, self.nrows, self.ncols)

    def play(self):
        '''
        Interactively play a game.

        Arguments: none
        Return value: none
        '''

        while True:
            try:
                cmd = input('Command: ')
                print()

                if cmd == '':
                    continue
                elif cmd == 'q':
                    # Quit the self.
                    print('\nBye for now!')
                    return
                elif cmd == 'u':
                    # Undo a move.
                    print('Undoing move...')
                    print()
                    self.undo()
                    self.display(moves=True)
                elif cmd[0] == 'l':
                    # Load a puzzle.
                    n = int(cmd[1:])
                    self.load(u.puzzles[n])
                    self.display(moves=True)
                else:  
                    # This must be a move.
                    if cmd[0] == 'm':
                        # It's an indexed move.
                        n = int(cmd[1:])
                        moves = list(self.possible_moves())
                        moves.sort()
                        (loc1, loc2) = moves[n]
                    else:
                        # Assume it's a move identified by (row1, col1, row2, col2)
                        # coordinates in four digits.
                        if len(cmd) != 4:
                            raise InvalidMove(f'Invalid move: {cmd}')
                        (a, b, c, d) = cmd
                        ai = int(a)
                        bi = int(b)
                        ci = int(c)
                        di = int(d)
                        loc1 = (ai, bi)
                        loc2 = (ci, di)

                    self.make_move((loc1, loc2))

                    if self.removed == {}:
                        msg = 'Invalid move (no squares removed): ' + \
                                  f'{loc1} -- {loc2}'
                        raise InvalidMove(msg)

                    self.display(removed=True)
                    print('Hit <return> to continue... ', end='')
                    input()
                    print()
                    self.display(moves=True)
                    if self.rep == {}:
                        print('You win!\n')
                        return

            except ValueError as e:
                print(e)
                print()
                self.display(moves=True)

            except IndexError as e:
                print(e)
                print()
                self.display(moves=True)

            except InvalidMove as e:
                print(e)
                print()
                self.display(moves=True)

            except AssertionError as e:
                print()
                tb.print_exc()
                print()
                self.display(moves=True)


if __name__ == '__main__':
    game = Dissembler()
    game.play()

