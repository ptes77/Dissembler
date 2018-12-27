# Name: Eugene Shao
# CMS cluster login name: eyshao

'''
The CS 1 final exam, Fall 2018, part 1.

Functions on locations and sets of locations.
'''

import string
from utils import *

def is_adjacent(loc1, loc2):
    '''
    Arguments:
      loc1, loc2 -- (row, column) locations

    Return value: 
      True if two locations are orthogonally adjacent, otherwise False.
    '''

    assert is_loc(loc1)
    assert is_loc(loc2)
    
    xDif = abs(loc1[0] - loc2[0])
    yDif = abs(loc1[1] - loc2[1])
    
    if xDif == 1:
        if yDif == 0:
            return True
    elif yDif == 1:
        if xDif == 0:
            return True
    
    return False

def adjacent_to_any(loc, locset):
    '''
    Arguments:
      loc -- a (row, column) location
      locset -- a set of locations

    Return value:
      True if `loc` is not in `locset` and at least one location 
      in `locset` is adjacent to `loc`, otherwise False.

    The set `locset` is not altered.
    '''

    assert is_loc(loc)
    assert is_locset(locset)
    
    if loc in locset:
        return False
    else:
        for location in locset:
            if is_adjacent(loc, location):
                return True

    return False    

def collect_adjacent(locset, target_set):
    '''
    Arguments:
      locset -- a set of (row, column) locations
      target_set -- another set of (row, column) locations

    Return value: 
      A set of all the locations in `locset` that are adjacent 
      to any location in `target_set`.

    The sets `locset` and `target_set` are not altered.
    '''

    assert is_locset(locset)
    assert is_locset(target_set)
    
    similar = set()
    
    for loc in locset:
        if adjacent_to_any(loc, target_set.difference({loc})):
            similar.add(loc)
    
    return similar

def collect_connected(loc, locset):
    '''
    Arguments:
      loc -- a (row, column) location
      locset -- a set of locations

    Return value: 
      A set of all the locations in `locset` which are connected to `loc` 
      via a chain of adjacent locations. Include `loc` in the resulting set.

    The set `locset` is not altered.
    '''

    assert is_loc(loc)
    assert is_locset(locset)
    
    connected = {loc}
    copyLocset = locset.copy()
    while len(collect_adjacent(copyLocset, connected)) != 0:
        connected = connected.union(collect_adjacent(copyLocset, connected))
        copyLocset = copyLocset.difference(connected)
    
    return connected
    
def partition_connected(locset):
    '''
    Partition a set of locations based on being connected via a chain of
    adjacent locations.  The original locset is not altered.
    Return a list of subsets.  The subsets must all be disjoint i.e.
    the intersection of any two subsets must be the empty set.

    Arguments:
      locset -- a set of (row, column) locations

    Return value: 
      The list of partitioned subsets.

    The set `locset` is not altered.
    '''

    assert is_locset(locset)
    
    copyLocset = locset.copy()
    partition = []
    while len(copyLocset) != 0:
        loc = copyLocset.pop()
        focusSet = collect_connected(loc, copyLocset)
        for element in focusSet.difference({loc}):
            copyLocset.remove(element)
        partition.append(focusSet)
    
    return partition

def filter_locset(locset):
    '''
    Given a locset, partition it into subsets which are connected via a
    chain of adjacent locations.  Compute two sets:
      -- the union of all partitions whose length is < 3 
      -- the union of all partitions whose length is >= 3 
    and return them as a tuple of two sets (in that order).  

    Arguments:
      locset -- a set of (row, column) locations

    Return value:
      The two sets as described above.

    The set `locset` is not altered.
    '''

    assert is_locset(locset)
    
    partition = partition_connected(locset)
    setLong = set()
    setShort = set()
    for element in partition:
        if len(element) >= 3:
            setLong = setLong.union(element)
        else:
            setShort = setShort.union(element)
    
    return (setShort, setLong)