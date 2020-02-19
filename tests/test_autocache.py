import unittest

# Import from parent folder
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from data import *
from formulize import *
from treeify import *


class TestFormulizeParse(unittest.TestCase):
  def setUp(self):
    self.fo = Formulize()
  
  def test_single_primatives(self):
    assert(self.fo.run('1000'), [1000])








'''
def test_formula(fo, filename=None):
  form = Formulize()
  fo = form.sterilize(fo)
  (fm, pr) = form.objectify_formula(fo)
  print(fo)
  pp_meta(fm)
  print("====FORMULIZE TEST COMPLETE====")
  print()
  tree = OpTree()
  root = tree.build_tree(fm, pr)
  print(str(root.eval()))
  print(RenderTree(root))
  if filename != None:
    render_tree(root, filename)
'''