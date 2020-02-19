import itertools 
from itertools import tee
from enum import Enum
import re
#from statemachine import StateMachine, State

from data import *

'''
Building Tree with Parens

use stack to find delim, then build a fm and pl for that area.
build tree from it, receiving root
add root to main fm
then build larger tree using that root.


Spotting PrimFunc's 
use regex to spot fn
'''
class Formula:
  def __init__(self, fm, pl):
    self.fm = fm
    self.pl = pl
    self.prims = None

class State(Enum):
  RUNNING = 1
  CONSUMED = 2
  PRIORITY_PAREN = 3
  FUNC_ARGS = 4

class Formulize:
  def __init__(self):
    pass

  def run(self, cmd):
    cmd = self.sterilize(cmd)
    return self.objectify_formula(cmd)

  def sterilize(self, cmd):
    cmd = ''.join(cmd.split())
    return cmd

  def objectify_formula(self, cmd) -> Formula:
    fm = [] # Formula Meta

    mut_obj = [] # Shared object, is only added when func returns true
    state = State(State.RUNNING)

    command_enum = enumerate(iter(cmd))
    i,c = next(command_enum)
    flow = consumer_flow(i, c, cmd, mut_obj)

    for i, c in command_enum:
      state, roll = flow(i,c,state)

      if state == State.CONSUMED:
        if roll == -1: # If op then rollback
          command_enum = itertools.chain([(i,c)], command_enum) # Repair iter after peekahead
        fm.append(mut_obj[0]) # Chunk
        mut_obj = []

        # Initialize next flow before loop
        try:
          i,c = next(command_enum)
        except:
          break
        flow = consumer_flow(i, c, cmd, mut_obj)
      elif state == State.PRIORITY_PAREN:
        # TODO
        pass

    # Possibly add string error or int consumption
    if state == State.FUNC_ARGS:
      raise Exception("Error, function not delimited correctly")
    elif state == State.RUNNING:
      pass
      #raise Exception("Hmmm... still in running mode")
    return Formula(fm, make_priority_list(fm))

def make_priority_list(fm):
  pl = [[] for x in op_priority_map.keys()] # Priority List
  for i, o in enumerate(fm):
    p = op_priority_map.get(o)
    if p != None:
      pl[p].append(i)
  return pl

def consumer_flow(i_start, c_start, cmd, mut_obj):
  _err = lambda msg, i, c, fo: Exception("(%s) Error at, %d, char was %s, \nFormula, %s",(msg, i, c, fo))
  # If a primative then shortcircut
  if c_start == '"':
    return string_consumer(i_start, cmd, mut_obj)
  if c_start.isdigit():
    return int_consumer(i_start, cmd, mut_obj)
  
  # Special parse open bracket
  if c_start == "(":
    raise Exception("OH SHIT A PAREN")
    return State.PRIORITY_PAREN, 0
  
  # If first char matches nothing in trie then short
  if op_priority_trie.has_node(c_start) != 0 and prim_func_trie.has_node(c_start) != 0: #Either delim or invalid
    raise _err("NOMATCH SHORT", i_start, c_start, cmd)

  # Parse either a function or an operator
  chars = [c_start]
  _consume_before = before_consumer(')')
  def f(i, c, state):
    nonlocal _err
    # Function Arguments
    if state == State.FUNC_ARGS:
      func_args = _consume_before(i,c)
      if func_args == None:
        return State.FUNC_ARGS, 0
      else:
        prefix = ''.join(chars)
        mut_obj.append(consume_func_prim(prefix, func_args))
        return State.CONSUMED, 0

    # Function
    s1 = ''.join(chars)
    if c == '(': # Function delim
      if prim_func_trie.has_node(s1) > 0:
        return State.FUNC_ARGS, 0
      else:
        raise _err("PRIMFUNC", i, s1, cmd)
        
    # Operator
    chars.append(c)
    s2 = ''.join(chars)
    if op_priority_trie.has_node(s2) == 0 and prim_func_trie.has_node(s2) == 0: # Invalid or operator delim
      if op_priority_trie.has_node(s1) > 0: # 
        mut_obj.append(s1)
        return State.CONSUMED, -1
      else:
        raise _err("OPERATOR TRIE MISS", i, s1, cmd)
    return State.RUNNING, 0
  return f

# ======= FUNC_TXT TO FUNC_OBJ CONVERSION ======= 

# ========== CONSUMERS ========== 
def before_consumer(delim):
  chars = []
  def f(i, c):
    nonlocal chars
    chars.append(c)
    if chars[len(chars)-1] == delim:
      s = ''.join(chars[0:-1])
      return s
    return None
  return f

def string_consumer(i_start, cmd, mut_obj):
  def f(i,c,state):
    if c == '"':
      mut_obj.append(PrimValue(cmd[i_start+1:i])) # keep outer quote
      return State.CONSUMED, 0
    return State.RUNNING, 0
  return f

def int_consumer(i_start, cmd, mut_obj):
  def f(i,c,state):
    if not c.isdigit() :
      mut_obj.append(PrimValue(int(cmd[i_start:i]))) 
      return State.CONSUMED, -1
    return State.RUNNING, 0
  return f

def consume_func_prim(prefix, args):
  args_iterable = parse_func_args(args)
  f = map_lazify_func(prefix, args_iterable)
  return PrimFunc(prefix, args_iterable, f)

# Returns a double pointer to a list of arguments
def parse_func_args(args: str):
  if args == '':
    return []
  items = re.split(',', args)

  parsed_args = []
  isKeyVal = False
  if items[0].find("=") != -1:
    parsed_args = {}
    isKeyVal = True
  for item in items:
    key_val = item.split("=")

    if (isKeyVal and len(key_val) == 1) or (not isKeyVal and len(key_val) == 2) :
      raise Exception("Cannont mix keyed and non-keyed declarations")
    if len(key_val) > 2:
      raise Exception("Limit one key value per delimiter: "+item)

    if isKeyVal:
      parsed_args[key_val[0]] = key_val[1]
    else:
      parsed_args.append(item)

  return parsed_args

def map_lazify_func(prefix, args):
    def f():
      f1 = prim_func_map[prefix]
      if type(args) == list:
        return f1(*args)
      else:
        return f1(**args)
    return f
# END FLOW