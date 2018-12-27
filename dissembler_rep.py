# Name: Eugene Shao
# CMS cluster login name: eyshao
'''
The CS 1 final exam, Fall 2018, part 2.

The Dissembler puzzle game.
'''

from utils import *
import locset as ls

# ---------------------------------------------------------------------- 
# Functions on board representations.
# ---------------------------------------------------------------------- 

def invert_rep(rep):
    '''
    Invert the board representation which maps locations to colors.
    The inverted representation will map colors to sets of locations.

    Arguments:
      rep -- a dictionary mapping locations to one-character strings
             representing colors

    Return value:
      a dictionary mapping one-character strings (representing colors)
      to sets of locations

    The input dictionary 'rep' is not altered.
    '''

    assert is_rep(rep)
    
    rep2 = {}
    repkeys = list(rep.keys())
    repvalues = list(rep.values())
    for i in range(len(repkeys)):
        if repvalues[i] not in rep2:
            rep2[repvalues[i]] = {repkeys[i]}
        else:
            rep2[repvalues[i]].add(repkeys[i])
    
    return rep2

def revert_rep(inverted):
    '''
    Invert the board representation which maps colors to sets of 
    locations.  The new representation will map locations to colors.

    Arguments:
      inverted -- a dictionary mapping one-character strings 
                  (representing colors) to sets of locations

    Return value:
      a dictionary mapping locations to one-character strings
      representing colors

    The input dictionary 'inverted' is not altered.
    '''

    assert is_inverted_rep(inverted)

    rep2 = {}
    invertedKeys = list(inverted.keys())
    for i in range(len(inverted)):
        for element in inverted[invertedKeys[i]]:
            rep2[element] = invertedKeys[i]
    
    return rep2

def swap_locations(rep, loc1, loc2):
    '''
    Exchange the contents of two locations.

    Arguments:
      rep -- a dictionary mapping locations to one-character strings
             representing colors
      loc1, loc2 -- adjacent locations which are in the board rep

    Return value:
      a new dictionary with the same structure of 'rep' with the
      specified locations having each others' contents

    The input dictionary 'rep' is not altered.
    '''

    assert is_rep(rep)
    assert is_loc(loc1)
    assert is_loc(loc2)
    assert ls.is_adjacent(loc1, loc2)
    assert loc1 in rep
    assert loc2 in rep
    
    repCopy = rep.copy()
    
    tempLocValue = repCopy[loc1]
    repCopy[loc1] = repCopy[loc2]
    repCopy[loc2] = tempLocValue
    
    return repCopy
    
def remove_connected_groups(rep):
    '''
    Remove all connected color groups covering at least three squares
    from a board representation.

    Arguments: 
      rep -- a dictionary mapping locations to one-character strings
             representing colors

    Return value:
      a tuple of two dictionaries of the same kind as the input
      (i.e. a mapping between locations and color strings);
      the first contains the remaining locations only, 
      and the second contains the removed locations only 

    The input dictionary 'rep' is not altered.
    '''

    assert is_rep(rep)
    
    repShort = {}
    repLong = {}
    invertedRep = invert_rep(rep)
    locations = list(invertedRep.keys())
    
    for element in locations:
        tempFilter = ls.filter_locset(invertedRep[element])
        for element in tempFilter[0]:
            repShort[element] = rep[element]
        for element in tempFilter[1]:
            repLong[element] = rep[element]
    
    return (repShort, repLong)
    
def adjacent_moves(nrows, ncols):
    '''
    Create and return a set of all moves on a board with 'nrows' rows and
    'ncols' columns.  The moves consist of two adjacent (row, column)
    locations.

    Arguments:
      nrows -- the number of rows on the board
      ncols -- the number of columns on the board

    Return value:
      the set of moves, where each move is a pair of adjacent locations
      and each location is a (row, column) pair; also the two locations
      are ordered in the tuple (the "smallest" comes first)

    Note that the moves are independent of the contents of any board
    representation; we aren't considering whether the moves would actually 
    change anything on a board or whether the locations of each move are 
    occupied by color squares.
    '''

    assert type(nrows) is int and type(ncols) is int
    assert nrows > 0 and ncols > 0
    
    moves = set()
    
    for i in range(nrows):
        for j in range(ncols - 1):
            moves.add(((i, j), (i, j + 1)))
    for j in range(ncols):
        for i in range(nrows - 1):
            moves.add(((i, j), (i + 1, j)))
    
    return moves
    
    
def possible_moves(rep, nrows, ncols):
    '''
    Compute and return a set of all the possible moves.  A "possible move"
    is a move where:
    -- both locations of the move are adjacent
    -- both locations on the board rep are occupied by colors 
    -- making the move will cause some locations to be vacated

    Arguments: 
      rep -- a dictionary mapping locations to one-character strings
             representing colors
      nrows -- the number of rows on the board
      ncols -- the number of columns on the board

    Return value: 
      the set of possible moves

    The input dictionary 'rep' is not altered.
    '''

    assert is_rep(rep)
    assert type(nrows) is int and type(ncols) is int
    assert nrows > 0 and ncols > 0
    
    possMoves = set()
    if rep != {}:
        locs = list(rep.keys())
        xLocs = [locs[i][0] for i in range(len(rep.keys()))]
        yLocs = [locs[i][1] for i in range(len(rep.keys()))]
        totalMoves = adjacent_moves(max(xLocs) + 1, max(yLocs) + 1)
        
        for loc1, loc2 in totalMoves:
            if (loc1 in locs) and (loc2 in locs):
                temp = remove_connected_groups(swap_locations(rep, loc1, loc2))
                if len(temp[1]) != 0:
                    possMoves.add((loc1, loc2))
    
    return possMoves