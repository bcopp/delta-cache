# DeltaCache
An extensible FSM parser for translating user defined formulas into cachable tree structures.

## How it works
* Define a formula
* Specify its priority (think pemdas)
* Specify its resulting function call
* Write a formula with arbitrary grammer

## Showcase

```
formula = '1000 + 20 + 10 power 60 + reverse(123) - 20' 
t = tree_builder.new(formula)
render(t)
```
![tree1](https://raw.githubusercontent.com/bcopp/delta-cache/master/tree1.png)
A tree structure is created. The ordering of its nodes corrisponds to priority in which operatrions are evaluated.

### Update Tree and Partial Caching

```
formula2 = '1000 + 20 + 10 * 60 + reverse(123)'
t.update(formula2)
render(t)
```
![tree2mod](https://raw.githubusercontent.com/bcopp/delta-cache/master/tree2mod.png)

The tree structure caches on its partially evaluated branches and is intelligent enough to save those caches which persist and wipe those which do not. (Persistant circled in Red) 

## How it works

*Given a formula* `1000 + 20 + power 60 + times_by_x(123) - 20`

*Write operator rules for it:*
```
op_func_map = {   
  "+": OP.add,
  "-": OP.sub,           
  "*": OP.mul,
  "power": OP.pow,
}
op_priority_map = {
  "+": 3,
  "-": 2,
  "*": 1,
  "power": 0,
}
prim_func_map = {
  "reverse": reverse_number, # Reverse number is a custom function.
} 
```

*Parse formula into intermediate datastructure*
```
['1000', '+', '20', '+', '10', 'power', '60', '+', "reverse(['123']): 4", '-']
```

*Parse intermediate datastructure into cachable tree*
```
<data.Oper object at 0x7f4cccda6f50>
├── <data.Oper object at 0x7f4cccda6150>
│   ├── <data.Oper object at 0x7f4cccda6510>
│   │   ├── <data.PrimValue object at 0x7f4cccda6dd0>
│   │   └── <data.PrimValue object at 0x7f4cccda6a50>
│   └── <data.Oper object at 0x7f4cccda6cd0>
│       ├── <data.PrimValue object at 0x7f4cccda6b90>
│       └── <data.PrimValue object at 0x7f4cccda6890>
└── <data.Oper object at 0x7f4cccda6650>
    └── <data.PrimFunc object at 0x7f4cccda68d0>
```

## Contributing to DeltaCache
To contribute to DeltaCache, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`. 
3. Make your changes and commit them: `git commit -m '<commit_message>'
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request.

Alternatively see the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## Contact 

If you want to contact me you can reach me at bcopp.oss@gmail.com
