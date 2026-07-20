import os
import json

def rewrite_template(unused_file_name, funname, local_list, returnnum):
    """clear"""
    
    return_string = ''
    if returnnum > 0:
        for i in range(returnnum):
            return_string = return_string + 'return{},'.format(i)
        return_string = return_string[:-1] + '='
    LOC = ''
    # if 'wjfwjf' not in globals().keys():
    #     import gzip
    #     with gzip.open('gzipinfo.txt', 'r') as fin:
    #         globals()['wjfwjf'] = json.loads(fin.read().decode('utf-8'))
        
    
    # LOC = globals()['wjfwjf'][unused_file_name]
    # added for improvement
    if 'group_index_loaded' not in globals().keys():
        with open('group_index.json', 'r') as f:
            globals()['group_index_loaded'] = json.load(f)
    
    group_id = globals()['group_index_loaded'][unused_file_name]
    
    if group_id not in globals().keys():
        with open('{}.json'.format(group_id), 'r') as f:
            globals()[group_id] = json.load(f)
    
    LOC = globals()[group_id][unused_file_name]
    
    LOC = '{}\n'.format(LOC) + return_string + '{}'.format(funname)
    exec(LOC, local_list, globals())
    
    if returnnum > 0:
        if returnnum == 1:
            return globals()['return0']
        if returnnum == 2:
            return (globals()['return0'], globals()['return1'])
        if returnnum == 3:
            return (globals()['return0'], globals()['return1'], globals()['return2'])
        if returnnum == 4:
            return (globals()['return0'], globals()['return1'], globals()['return2'], globals()['return3'])
        if returnnum == 5:
            return (globals()['return0'], globals()['return1'], globals()['return2'], globals()['return3'], globals()['return4'])
        if returnnum == 6:
            return (globals()['return0'], globals()['return1'], globals()['return2'], globals()['return3'], globals()['return4'], globals()['return5'])
        if returnnum == 7:
            return (globals()['return0'], globals()['return1'], globals()['return2'], globals()['return3'], globals()['return4'], globals()['return5'], globals()['return6'])
        if returnnum == 8:
            return (globals()['return0'], globals()['return1'], globals()['return2'], globals()['return3'], globals()['return4'], globals()['return5'], globals()['return6'], globals()['return7'])
        if returnnum == 9:
            return (globals()['return0'], globals()['return1'], globals()['return2'], globals()['return3'], globals()['return4'], globals()['return5'], globals()['return6'], globals()['return7'], globals()['return8'])

