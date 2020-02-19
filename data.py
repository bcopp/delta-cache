import operator as OP 
import pygtrie as trie
from anytree import NodeMixin
ID = 0

def redis_func(cmd, key, val):
  return "COMMAND:%s, KEY:%s, VAL:%s"%(cmd, key, val)

func_params = '"k1"=$n,"k2"=$s,"k3"=$s'
func_data = 'f("k1"=10,"k2"=whats up my dude,"k3"=suh)'
prim_func_map = {
  "sql": lambda item1: "%s" % (item1),
  "sql2": lambda item1, item2: "%s,%s" % (item1, item2),
  "redis": redis_func
}
op_func_map = {
  "+": OP.add,
  "-": OP.sub,
  "/": OP.floordiv,
  "*": OP.mul,
  "**": OP.mul,
  "**-": OP.mul,
  "**-+": OP.mul,
  "append": OP.add,
  "^": OP.pow,
}
op_priority_map = {
  "+": 4,
  "append": 4,
  "-": 3,
  "*": 2,
  "**": 2,
  "**-": 2,
  "**-+": 2,
  "***/": 2,
  "/": 1,
  "^": 0,
}
i_priority_map = {key: val for val, key in op_priority_map.items()}

print("====== TEST DATA ======")
op_priority_trie = trie.CharTrie()
for k, v in op_priority_map.items():
  op_priority_trie[k] = v
print("OPERATOR_TRIE: "+str(op_priority_trie))

prim_func_trie = trie.CharTrie()
for k, v in prim_func_map.items():
  prim_func_trie[k] = v
print("PRIM_FUN_TRIE: "+str(prim_func_trie))
print()

# DATATYPES
class Oper(NodeMixin):
  def __init__(self, op, children=[]):
    # Anytree Options
    global ID
    self.name = str(op)+":"+str(ID)
    self.children = children

    self.op = op
    ID +=1

  def eval(self):
    if len(self.children) == 0:
      raise Exception("Operator must have children")
    op = op_func_map[self.op]
    val = self.children[0].eval()
    for v in self.children[1:]:
      v2 = v.eval()
      val = op(val, v.eval())
    return val
  
  def set_children(self, child):
    self.children.append(child)

  def __str__(self):
    return str(self.op)

class PrimValue(NodeMixin):
  def __init__(self, val):
    global ID
    self.name = str(val)+":"+str(ID)
    self.fm_name = str(val)
    self.val = val
    self.children = []
    ID += 1

  def eval(self):
    return self.val

  def __str__(self):
    s = str(self.val)
    return s

class PrimFunc(NodeMixin):
  def __init__(self, prefix, args, func):
    global ID
    self.name = "%s(%s): %s"%(prefix,args,str(ID))
    self.fm_name = "%s(%s)"%(prefix,args)
    self.func = func
    self.children = []
    ID += 1

  def eval(self):
    return self.func()

  def __str__(self):
    return self.name
# END DATATYPES
