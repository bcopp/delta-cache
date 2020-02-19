from anytree import Node, RenderTree
from anytree.exporter import DotExporter
import logging as log
import copy

from data import *
from formulize import Formulize

class TreeRoot:
  def __init__(self, root, formula, prims):
    self.formula = formula
    self.root = root
    self.prims = prims

class OpTree:
  def __init__(self):
    self.caches = 1
    self.fragmentation = 100
    self.root = None

  # Receives an objectified formula and list of operators in order of priority
  # Returns a tree structure
  def new(self, formula):
    fm = copy.deepcopy(formula.fm)
    pl = copy.deepcopy(formula.pl)
    prims = {}
    node = None

    def get_highest_parent(chunk):
      p = chunk
      while p.parent != None:
        p = p.parent
      return p

    for l in pl:
      for mi in l:
        childs = []
        if mi - 1 >= 0:
          childs.append(fm[mi - 1])
        if mi + 1 < len(fm):
          childs.append(fm[mi + 1])
        node = Oper(fm[mi], ([get_highest_parent(chunk) for chunk in childs]))
        # HACK
        for c in node.children:
          if type(c) is not Oper:
            prims[c.fm_name] = c
        # Tree is immutable, update it with iters
        #node.children = itertools.chain(iter(node.children), [l_chunk])
        #node.children = itertools.chain(iter(node.children), [r_chunk])
        if mi - 1 > 0:
          fm[mi - 1] = node
        if mi + 1 < len(fm):
          fm[mi + 1] = node

    # No operators found, then grab primative
    if node == None:
      node = fm[0]
    
    return TreeRoot(node, formula, prims)
  
  def update(self, formula_meta, priority_list):
    pass

# =====================================
# ============== Testing ==============
# =====================================
def render_tree(root, name):
  DotExporter(root).to_picture(name + ".png")

# Printers
def pp_meta(fo):
  ns = []
  for n in fo:
    ns.append(str(n))
  print(ns)

def test_large():
  log.basicConfig(level=log.DEBUG)
  print("====== TEST LARGE =====")
  print()
  c = '"hello_" append sql(my_sql_statement) append "___" append redis(cmd=SET,key=number,val=10)'
  formula = test_formula(c)

  print("-----------------------") 
  print("------ TEST TREE ------")
  print("-----------------------") 
  tree_builder = OpTree()
  tree = tree_builder.new(formula)

  print(RenderTree(tree.root))
  render_tree(tree.root, "large")
  print("----------------------")
  pp_meta(tree.formula.fm)
  print("PL: " + str(formula.pl))
  print("----------------------")
  print(str(tree.root.eval()))

def test_formula(cmd):
  print("------ TEST FORM -----")
  #fo = "11 + 2 * 2 +900 * sql(my_sql_statement) + redis(cmd=SET,val1=number,val2=10)+2 + 9 + 30 * 3"
  #fo = '"hello"+"world"+"sup'
  print(cmd)
  f_builder = Formulize()
  cmd = f_builder.sterilize(cmd)
  f = f_builder.objectify_formula(cmd)
  pp_meta(f.fm)

  return f

'''
test_formula("-1000")
test_formula("1000")
'''
test_large()
bug_fo = "11 + + 900"