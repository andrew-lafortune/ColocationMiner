
'''

INPUT: A baseline set of locations (optional), an emergent set of locations (need dates)

STEPS:
1. Determine date/time range for emergence
    - allow option to duplicate plots for a certain time step and aggregate multiple steps
    - include start and end time as optional parameters
2. For each time step, add new events to data
    - Check colocation rules {new} => {old}, participation index should equal conditional probability(?)
    
OUTPUT:
Set of rules for emergent colocation, final plot of colocations, gif of evolution if specified


'''
import pandas as pd

from datetime import datetime
from classes import CascadeRule

def get_prevalent(T, theta):
    out = T
    counts = T[['new_cat','new_id']].drop_duplicates()['new_cat'].value_counts()
    grouped = T.groupby(by=['new_cat','old_cat'])
    for cats,_ in grouped:
        group = grouped.get_group(cats)
        if len(group) < counts[cats[0]] * theta:
            out = out.drop(group.index)
    return out

def get_colocations(new, old, relation, thold):
    out = pd.merge(new, old, how='cross')
    out.loc[:,'relation'] = relation(out['new_pos'],out['old_pos'], thold)
    out = out[out['relation'] == True].drop(['relation'],axis=1)
    return out

def get_rules(T, alpha):
    rules = []
    counts = T[['new_cat','new_id']].drop_duplicates()['new_cat'].value_counts()
    grouped = T.groupby(by=['new_cat','old_cat'])
    for cats,_ in grouped:
        group = grouped.get_group(cats)
        cpi = len(group['new_id'].unique()) / counts[cats[0]]
        if cpi > alpha:
            rules.append(CascadeRule(cats[0],cats[1], cpi))
    return rules
        
def colocate_emergent(E_old, E_new, grouper, theta, alpha, relation, thold):
    old = E_old
    T = {}

    all = pd.DataFrame(columns=['new_cat','new_id','new_pos','old_cat','old_id','old_pos'])

    group_by_time = E_new.groupby(grouper)
    for time,_ in group_by_time:
        new = group_by_time.get_group(time)
        merged = get_colocations(new, old, relation, thold)
        all = pd.concat([all, merged.drop(columns=['time'])])
        prevalent = get_prevalent(all, theta)
        T[time] = prevalent
        old.append(new, ignore_index=True)

    R = get_rules(prevalent,alpha)

    return T, R