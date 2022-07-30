#!/usr/bin/env python
# coding: utf-8

# In[1]:


from platform import python_version
print(python_version())


# ### Bibliotecas
# * graphviz
# * pydot
# * re
# * pathlib
# * networkx

# In[9]:


# Python 3.10.3

import ControlFlow
import re
import pydot
import os
# from graphviz import Source, Digraph

import re
from pathlib import Path


# In[10]:


def create_image_graph(dot_txt, name_file):
    
    graph, = pydot.graph_from_dot_data(dot_txt)
    name_image = f'{name_file}.png'
    graph.write_png(name_image)

    return name_image


# ###  Making Path

# In[11]:


def cache_to_json(cache):
    nodes_graph = []
    for k,v in cache.items():
    
        dict_item = {'id':v.rid, 
                      'parents': [p.rid for p in v.parents], 
                      'children': [c.rid for c in v.children], 
                      'calls': v.calls, 
                      'at':v.lineno() ,
                      'ast':v.source()}

        nodes_graph.append(dict_item)
    return nodes_graph


# In[12]:


def at_return(code_line, dict_id, ident, key):

    global path_code, dicts_blocks    

    # Get the id and identation of the function that contains the return
    id_function, ident_function = [[k,v[0]] for k,v in dicts_blocks.items() if v[2] == "function"][-1]
    
    path_code = path_code + f"{ident}nos.append({dict_id})\n"  
    
    path_code = path_code + f"{ident}nos.append('{id_function}: exit')\n"  
    path_code = path_code + code_line            

    # If the identation of the def and the return are equals, the function ended
    if ident == ident_function + "    ":
        dicts_blocks[key][1] = True

def at_continue(code_line, dict_id, ident):
    global path_code

    id_loop = [k for k,v in dicts_blocks.items() if v[2] == "loop" and v[1] == False][-1]
                           
    path_code = path_code + f"{ident}nos.append({dict_id})\n"   
                
    path_code = path_code + f"{ident}nos.append({id_loop})\n"           
    path_code = path_code + code_line

def at_elif(code_line, dict_id, ident, nodes_graph):
    global path_code, dict_elifs

    len_ident = len(ident)

    try:
        ast_node = [dict_node for dict_node in nodes_graph if dict_node["at"] == dict_id][0]["ast"]

        if("_if:") in ast_node:

            elif_nodes = [dict_id]                
            path_code = path_code + code_line

            if len_ident not in dict_elifs.keys():
                dict_elifs[len_ident] = [True, elif_nodes]
            
            elif not dict_elifs[len_ident][0]:
                dict_elifs[len_ident] = [True, elif_nodes]
                    
            else:    
                elif_nodes =  dict_elifs[len_ident][1]
                elif_nodes.append(dict_id)

            ident_node = ident + "    "                        
            path_code = path_code + f"{ident_node}nos.extend({elif_nodes})\n"

            return 1

    except:
        
        return 0
    
def at_loop(ident, dict_id):
    global dicts_blocks 

    dicts_blocks[dict_id] = [ident, False,"loop"]
    dicts_blocks = dict(sorted(dicts_blocks.items(), reverse = True))

def check_end_elif(code_line, len_ident, ident):

    global path_code, dicts_blocks 
    ident_elif = ""

    if len(dict_elifs.keys()):

        elifs_true = {k:v for k,v in dict_elifs.items() if v[0]} 

        if "else" in code_line:

            if len_ident in elifs_true.keys():
                elif_nodes_dict = dict_elifs[len_ident][1]
                path_code = path_code + code_line
                ident_node = ident  + "    "
                path_code = path_code + f"{ident_node}nos.extend({elif_nodes_dict})\n"
                dict_elifs[len_ident] = [False, []] 
                return 1
        
        else:

            if len(elifs_true.keys()):
                last_key = list(elifs_true.keys())[-1]
                command_elif_dict = dict_elifs[last_key][0]
                

                if command_elif_dict:
                    if (len(ident) ==  last_key and "elif" not in code_line) or len(ident) <  last_key:                
                        elif_nodes_dict = dict_elifs[last_key][1]                        
                        path_code = path_code + f"{ident_elif}nos.extend({elif_nodes_dict})\n"
                        dict_elifs[last_key] = [False, []] 

    return 0

def check_end_function(code_line, ident):

    global path_code, dicts_blocks 

    for key in dicts_blocks.keys():

        ident_block = dicts_blocks[key][0]
        not_closed = dicts_blocks[key][1]            

        if not not_closed and len(ident) <= len(ident_block) and code_line != "":
            ident_block = ident_block + "    "
            dicts_blocks[key][1] = True
            if dicts_blocks[key][2] == "function":
                path_code = path_code + f"{ident_block}nos.append('{key}: exit')\n"
                
            else:
                path_code = path_code + f"{ident_block}nos.append({key})\n\n"

def check_functions_ended():
    
    global dicts_blocks, path_code
    
    
    for key in dicts_blocks.keys():

        ident_block = dicts_blocks[key][0] + "    "
        not_closed = dicts_blocks[key][1]     
        
        if not not_closed:
            dicts_blocks[key][1] = True

            if dicts_blocks[key][2] == "function":
                path_code = path_code + f"{ident_block}nos.append('{key}: exit')\n" 
            else:
                path_code = path_code + f"{ident_block}nos.append({key})\n\n"  

    


# In[13]:


def make_code_path(nodes_graph, code_lines):

    global path_code, dicts_blocks, dict_elifs

    dicts_blocks = {}
    dict_functions = {}
    dict_elifs = {}
    path_code = """nos = []\n"""

    for i in range(len(code_lines)):
        
        code_line = code_lines[i]
        ident = re.match(r"\s*", code_line).group() 
        len_ident = len(ident)
        dict_id = i + 1

        check_end_function(code_line, ident)
        if(check_end_elif(code_line, len_ident, ident)): continue  

        try:

            ast_node = [dict_node for dict_node in nodes_graph if dict_node["at"] == dict_id][0]["ast"]                  
                            
            if "return" in code_line:
                key = list(dicts_blocks.keys())[-1]
                at_return(code_line, dict_id, ident, key) 
                continue
        
            elif "continue" in code_line:
                at_continue(code_line, dict_id, ident)                       
                continue

            elif "elif " in code_line:
                if (at_elif(code_line, dict_id, ident, nodes_graph)): continue 
            
            
            elif "def" in code_line and "enter:" in ast_node:
                name_function = re.findall('def (.*)\(', code_line)[0]
                dict_functions[dict_id] = name_function
                dicts_blocks[dict_id] = [ident, False,"function"]
                
                path_code = path_code + code_line
                path_code = path_code + "    " + f"{ident}nos.append('{dict_id}: enter')\n" 

            else:
                path_code = path_code + f"{ident}nos.append({dict_id})\n"   
                path_code = path_code + code_line

                if "for" in code_line or "while" in code_line:
                    at_loop(ident, dict_id)

        except:
            path_code = path_code + code_line
               
    check_functions_ended()

    return path_code


# ### Making Files

# In[14]:


def get_nodes(nodes_graph):

    list_nodes = [[node["at"], node["ast"]]  for node in nodes_graph]
    list_nodes = [node[0] if not any(word in node[1] for word in ["enter", "exit"]) 
    else str(node[0]) + ": " + node[1].split(":")[0] for node in list_nodes]

    return list_nodes

def get_edges(graph, nodes_graph):

    dict_nodes = {node["id"]: [node["at"], node["ast"]]  for node in nodes_graph}

    m = re.findall('\t(.+?) -> (.+?)[\n\[]',str(graph))
    m = [(int(n1), int(n2)) for (n1,n2) in m if (n1 != "0" and n2 != "0")]
    new_m = [(dict_nodes[n1][0], n2) if not any(word in dict_nodes[n1][1] for word in ["enter", "exit"]) 
    else (str(dict_nodes[n1][0]) + ": " + dict_nodes[n1][1].split(":")[0], n2) for (n1,n2) in m ]
    
    new_m = [(n1, dict_nodes[n2][0]) if not any(word in dict_nodes[n2][1] for word in ["enter", "exit"]) 
    else (n1, str(dict_nodes[n2][0]) + ": " + dict_nodes[n2][1].split(":")[0]) for (n1,n2) in new_m ]

    new_m = [(n1,n2) for (n1,n2) in new_m if n1 != n2]

    return new_m


# In[15]:


def get_pair_edges(edges):
    
    pair_edges = []
    for edge in edges:
        source = edge[0]
        dest = edge[1]

        edges_n1 = [n2 for (n1,n2) in edges if n1 == dest and n1 != n2]

        pair_edges_source_dest = [(source,dest,sec_dest) for sec_dest in edges_n1]
        pair_edges.extend(pair_edges_source_dest)

    return pair_edges


# In[16]:


def make_file_nodes(name_file_export, path_code,nodes_covered, num_cond):


    script = f"""# Script Teste Cobertura de Nós
TR_nos = set({list(nodes_covered)})"   
"""  

    path_code = os.linesep.join([s for s in path_code.splitlines() if s])
    path_code = path_code.replace("\n", "\n    ")

    code_function = f"""

def code_graph():
    {path_code}
    
    return nos
"""
    script = script + code_function

    code_test = r"""
# Teste de nós
nos_testes = set([])
n_teste = 1

print(f"\n\033[38;5;87mTR Cobertura de Nós: \033[0;0m\n{TR_nos} \033[0;0m\n")

while(1):

    print(f"\033[38;5;39mTeste {n_teste}: \033[0;0m", end = "")
    n_teste += 1

    nos = code_graph()
    prev = object()
    nos = [prev:=v for v in nos if prev!=v]

    print(f"\n\033[38;5;11mCaminho:\033[0;0m\n{nos}\n")
    nos_testes = nos_testes.union(set(nos))

    print(f"\033[38;5;11mNós percorridos: \033[0;0m\n{list(set(nos))}\n")

    print(f"\033[38;5;47mRequisitos já satisfeitos: \033[0;0m \n{nos_testes}\n")

    # print(TR_nos - nos_testes)
    if (nos_testes == TR_nos):
        print(f'\033[48;5;42m\033[38;5;16m \033[1m TODOS OS REQUISITOS SATISFATÍVEIS FORAM ABRANGIDOS. \033[0;0m\n')
        break

    msg = f"\033[38;5;208mFalta passar pelos nós: {TR_nos - nos_testes} \033[0;0m"
    print(msg)"""


    script = script + code_test

    code_print = rf"""

    if n_teste > {num_cond*2}:
        print(f"\033[2;31mHá chances dos nós não serem alcançáveis. Verifique o grafo.\033[0;0m")
    
    print("\033[2;34m" + "-" * 75 + "\033[0;0m")
"""
    script = script + code_print
    
    return script
    


# In[17]:


def make_file_edges(name_file_export, path_code,edges, num_cond):

    script = f"""# Script Teste Cobertura de Arcos
arcos = {list(edges)}
TR_arcos = set(sorted(arcos, key=lambda x: int(str(x[0]).split(':')[0])))
"""  

    edges = [(str(n1), str(n2)) for (n1,n2) in edges] 

    path_code = os.linesep.join([s for s in path_code.splitlines() if s])
    path_code = path_code.replace("\n", "\n    ")
        
    code_function = f"""

def code_graph():
    {path_code}
    return nos
"""
    script = script + code_function

    code_test = r"""
# Teste de arcos
arcos_testes = set([])
n_teste = 1

print(f"\n\033[38;5;87mTR Cobertura de Arcos: \033[0;0m\n{TR_arcos} \033[0;0m\n")

while(1):
   
    print(f"\033[38;5;39mTeste {n_teste}: \033[0;0m", end = "")
    n_teste += 1
    nos = code_graph()

    print(f"\n\033[38;5;11mCaminho:\033[0;0m\n{nos}\n")

    arcos = []
    for i in range(len(nos)-1):  
        arcos.append((nos[i], nos[i+1]))

    arcos = [(str(n1), str(n2)) for (n1,n2) in arcos]    

    arcos_print = sorted(set(arcos))
    arcos_testes = arcos_testes.union(arcos)
    
    print(f"\033[38;5;11mArcos percorridos: \033[0;0m \n{arcos_print}\n")

    print(f"\033[38;5;47mRequisitos já satisfeitos: \033[0;0m \n{arcos_testes}\n")

    if (arcos_testes == TR_arcos):
        print(f'\033[48;5;42m\033[38;5;16m \033[1m TODOS OS REQUISITOS SATISFATÍVEIS FORAM ABRANGIDOS. \033[0;0m\n')
        break

    msg = f"\033[38;5;208mFalta passar pelos arcos: {TR_arcos - arcos_testes} \033[0;0m"
    print(msg) 
"""
    script = script + code_test

    code_print = rf"""

    if n_teste > {num_cond*2}:
        print(f"\033[2;31mHá chances dos arcos não serem alcançáveis. Verifique o grafo.\033[0;0m")
    
    print("\033[2;34m" + "-" * 75 + "\033[0;0m") 
"""
    script = script + code_print

    return script


# In[18]:


def make_file_pair_edges(name_file_export, path_code,pair_edges, num_cond):

    script = f"""# Script Teste Cobertura de Pares de Arcos
pares_arcos = {list(pair_edges)}
TR_arcos = set(sorted(pares_arcos, key=lambda x: int(str(x[0]).split(':')[0])))
"""  

    pair_edges = [(str(n1), str(n2), str(n3)) for (n1,n2,n3) in pair_edges] 
    
    path_code = os.linesep.join([s for s in path_code.splitlines() if s])
    path_code = path_code.replace("\n", "\n    ")
        
    code_function = f"""

def code_graph():
    {path_code}
    return nos
"""

    script = script + code_function

    code_test = r"""
# Teste de arcos
pares_arcos_testes = set([])
n_teste = 1

print(f"\n\033[38;5;87mTR Cobertura de Pares de Arcos: \033[0;0m\n{TR_pares_arcos} \033[0;0m\n")

while(1):
   
    print(f"\033[38;5;39mTeste {n_teste}: \033[0;0m", end = "")
    n_teste += 1
    nos = code_graph()

    print(f"\n\033[38;5;11mCaminho:\033[0;0m\n{nos}\n")

    pares_arcos = []
    for i in range(len(nos)-2):  
        pares_arcos.append((nos[i], nos[i+1],nos[i+2]))

    pares_arcos = [(str(n1), str(n2), str(n3)) for (n1,n2,n3) in pares_arcos]  

    set_pares_arcos = sorted(set(pares_arcos))
    pares_arcos_testes = pares_arcos_testes.union(set_pares_arcos)

    pares_arcos_print = [list(item) for item in set_pares_arcos]
    print(f"\033[38;5;11mPares de arcos percorridos: \033[0;0m \n{pares_arcos_print}\n")

    print(f"\033[38;5;47mRequisitos já satisfeitos: \033[0;0m \n{pares_arcos_testes}\n")

    if (pares_arcos_testes == TR_pares_arcos):
        print(f'\033[48;5;42m\033[38;5;16m \033[1m TODOS OS REQUISITOS SATISFATÍVEIS FORAM ABRANGIDOS. \033[0;0m\n')
        break

    msg = f"\033[38;5;208mFalta passar pelos pares de arcos: {TR_pares_arcos - pares_arcos_testes} \033[0;0m"
    print(msg)


    if n_teste > 14:
        print(f"\033[2;31mHá chances dos pares de arcos não serem alcançáveis. Verifique o grafo.\033[0;0m")
    
    print("\033[2;34m" + "-" * 75 + "\033[0;0m")
"""

    script = script + code_test

    code_print = rf"""

    if n_teste > {num_cond*2}:
        print(f"\033[2;31mHá chances dos pares de arcos não serem alcançáveis. Verifique o grafo.\033[0;0m")
    print("\033[2;34m" + "-" * len(msg) + "\033[0;0m") 
"""

    script = script + code_print

    return script


# ### Class Graph

# In[19]:


class graph_testing():

    def __init__(self, name_file):
        self.name_file = name_file

        code = Path(self.name_file, encoding="utf-8",errors='ignore').read_text() + "\n"

        # Name Files:
        name_without_ext = self.name_file.split(".")[0]
        name_file_only = name_without_ext.replace('uploads', 'outputs')
        file_path = f"static\IMG\{name_file_only}"
        

        name_file_nodes_export = f"{name_without_ext}_NODES"
        name_file_arcs_export = f"{name_without_ext}_ARCS"
        name_file_pair_arcs_export = f"{name_without_ext}_PAIR_ARCS"
        name_image_export = f"{file_path}_GRAPH"

        # Creating Graph
        self.cache = ControlFlow.gen_cfg(code)
        self.graph= ControlFlow.to_graph(self.cache)
        self.image_file = create_image_graph(str(self.graph), name_image_export)


        # Creating Code with nodes
        code_lines = re.findall('([^\n]*\n)', code)
        self.nodes_graph = cache_to_json(self.cache)
        self.path_code =  make_code_path(self.nodes_graph, code_lines)
        self.num_cond = len([node for node in self.nodes_graph if any(word in node["ast"] for word in ["_if:", "while:", "for:"])])

        self.nodes = get_nodes(self.nodes_graph)
        self.edges = get_edges(self.graph, self.nodes_graph)
        self.pair_edges = get_pair_edges(self.edges)
                                
           
        # Creating Files for tests
        self.script_nodes = make_file_nodes(name_file_nodes_export, self.path_code, self.nodes, self.num_cond)
        print(f"Arquivo {name_file_nodes_export}.py salvo com sucesso. Para executá-lo rode o código:")
        print(f"\033[2;34m %run {name_file_nodes_export}.py\033[0;0m \n")

        self.script_arcs = make_file_edges(name_file_arcs_export, self.path_code, self.edges, self.num_cond)
        print(f"Arquivo {name_file_arcs_export}.py salvo com sucesso. Para executá-lo rode o código:")
        print(f"\033[2;34m %run {name_file_arcs_export}.py\033[0;0m \n")

        self.script_pair_arcs = make_file_pair_edges(name_file_pair_arcs_export, self.path_code, self.pair_edges, self.num_cond)
        print(f"Arquivo {name_file_pair_arcs_export}.py salvo com sucesso. Para executá-lo rode o código:")
        print(f"\033[2;34m %run {name_file_pair_arcs_export}.py\033[0;0m \n")