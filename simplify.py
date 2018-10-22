# ========================================================================================================================================
import random
from copy import deepcopy
def dfasimplify(G): # Hopcroft算法
    cins                   = set( G['cins'] )
    termination_states     = set( G['termination_states'] ) 
    total_states           = set( G['total_states'] )
    state_transition_map   = G['state_transition_map']
    not_termination_states = total_states - termination_states

    def get_source_set( target_set, char ):
        source_set = set()
        for state in total_states:
            try:
                if state_transition_map[state][char] in target_set:
                    source_set.update( state )
            except KeyError:
                pass
        return source_set

    P = [ termination_states, not_termination_states ]
    W = [ termination_states, not_termination_states ]

    while W:
        
        A = random.choice( W )
        W.remove( A )

        for char in cins:
            X = get_source_set( A, char )
            P_temp = []
            
            for Y in P:
                S  = X & Y
                S1 = Y - X
                
                if len( S ) and len( S1 ):
                    P_temp.append( S )
                    P_temp.append( S1 )
                    
                    if Y in W:
                        W.remove( Y )    
                        W.append( S )
                        W.append( S1 )
                    else:
                        if len( S ) <= len( S1 ):
                            W.append( S )
                        else:
                            W.append( S1 )
                else:
                    P_temp.append( Y )
            P = deepcopy( P_temp )
    return P
'''dfa化简测试数据'''
# 数据格式
state_graph = {
    'total_states': [ 'A', 'B', 'C', 'D', 'E', 'F', 'S' ],
    'initial_states': [ 'A' ],
    'termination_states': [ 'C', 'D', 'E', 'F' ],
    'state_transition_map': {
        'S': { 'a': 'A', 'b': 'B' },
        'A': { 'a': 'C', 'b': 'B' },
        'B': { 'a': 'A', 'b': 'D' },
        'C': { 'a': 'C', 'b': 'E' },
        'D': { 'a': 'F', 'b': 'D' },
        'E': { 'a': 'F', 'b': 'D' },
        'F': { 'a': 'C', 'b': 'E' },
    },
    'cins': [ 'a', 'b' ],    
}
print("化简后的有限自动机子集划分：")
print(dfasimplify(state_graph))