# Name: Eugene Shao
# CMS cluster login: eyshao

import dissembler as d
import sys

def print_moves(moveSeq):
    '''Prints move sequence for solving the Dissembler puzzle.
    
    Arguments: a list containing the move sequence
    
    Return Value: none
    '''
    print('This puzzle is solvable!')
    for i in range(1, len(moveSeq)):
        s = f'\nStep {i}: '
        ((r1, c1), (r2, c2)) = moveSeq[i]
        s += f'({r1}, {c1}) -- ({r2}, {c2})'
        print(s)

def undo_location(game, moves, moveSeq, location):
    '''Undos a move/goes upwards in the tree.
    
    Arguments: a moves graph;
                a dictionary containing the edges and vertices of the graph;
                a list containing the current sequence of moves
                the location of the next move
    Return Value: none
    '''
    moveSeq.pop()
    game.undo()
    moves.pop(location)
    go_to_node(game, moves, moveSeq, moveSeq[-1])

def go_to_node(game, moves, moveSeq, nextMove):
    '''Goes to a node in the tree. 
    
    Arguments: a moves graph;
                a dictionary containing the edges and vertices of the graph;
                a list containing the current sequence of moves
                the location of the next move
    
    Return Value: none
    '''
    if game.rep == {}:
        print_moves(moveSeq)
        return (-1, -1, -1, -1)
    
    if nextMove not in moves:
        children = game.possible_moves()
        
        if len(children) == 0:                          # No possible moves
            moveSeq.pop()
            game.undo()
            return (game, moves, moveSeq, moveSeq[-1])
            # go_to_node(game, moves, moveSeq, moveSeq[-1])            
        
        moves[nextMove] = set()
        for move in children:
            moves[nextMove].add(move)
    
    if moves[nextMove] == set():
        if len(moveSeq) == 1:
            print('There are no solutions to this Dissembler puzzle!')
            return (-1, -1, -1, -1)
        moveSeq.pop()
        game.undo()
        moves.pop(nextMove)
        return (game, moves, moveSeq, moveSeq[-1])
        # go_to_node(game, moves, moveSeq, moveSeq[-1])        
    
    nextMove = moves[nextMove].pop()
    moveSeq.append(nextMove)
    game.make_move(nextMove)
    
    return (game, moves, moveSeq, nextMove)
    # go_to_node(game, moves, moveSeq, nextMove)


if len(sys.argv) != 2:
    print('Please enter two arguments: one for this file and one for ' + \
          'the puzzle file!')
    
game = d.Dissembler()
moves = {}
moveSeq = ['initial']
output = (0, 0, 0, 0)

try:
    with open(sys.argv[1], 'r') as f:
        puzzle = f.read().rstrip()
        game.load(puzzle)
    output = go_to_node(game, moves, moveSeq, 'initial')
    while output != (-1, -1, -1, -1):
        output = go_to_node(output[0], output[1], output[2], output[3])    
except FileNotFoundError:
    print('Cannot find file!')