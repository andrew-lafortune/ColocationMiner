from builtins import isinstance
import pandas as pd
import geopandas as gpd
from datetime import datetime
from general_colocation.utils import generate_supersets, generate_subsets
from general_colocation.classes import Rule, Colocation

def generate_table_instances(C, T, P, k, relation, thold):
    if k == 2:
        out = pd.merge(T, T.rename(columns={'cat1':'cat2','id1':'id2','pos1':'pos2'}), how='cross')
    else:
        tup_list = list(zip(*T[['cat'+str(i) for i in range(1,k)]].values.T))       #list of category combinations of size k
        T_tmp = T[[t in P for t in tup_list]]                                       #only check prevalent combinations
        
        T_tmp1 = T_tmp.rename(columns={'cat' + str(k-1):'cat' + str(k),'id' + str(k-1):'id' + str(k),'pos' + str(k-1):'pos' + str(k)})
        out = pd.merge(T_tmp, T_tmp1, on=['id'+str(i) for i in range(1,k-1)]+['cat'+str(i) for i in range(1,k-1)])

        tup_list = list(zip(*out[['cat'+str(i) for i in range(1,k+1)]].values.T))   #new list of category combinations of size k+1
        out = out[[t in C for t in tup_list]]                                       #only keep combinations in the new candidate set

    out = out[out['cat'+str(k-1)] < out['cat'+str(k)]]
    out.loc[:,'relation'] = relation(out['pos'+str(k-1)],out['pos'+str(k)], thold)
    out = out[out['relation'] == True].drop(['relation','pos'+str(k-1)],axis=1)
    return out

def generate_candidate_colocation(P, k):
    out = set()
    c = set(generate_supersets(P[k-1].values(), k))
    for candidate in c:
        kminusone_sets = generate_subsets(candidate, k)  # generate list of unique k subsets
        if kminusone_sets.issubset(P[k-1].keys()):
            out.update([candidate])
    return out
       
def select_prevalent(thold, T, k, cat_count):
    out = {}
    grouped = T.groupby(['cat'+str(i) for i in range(1,k+1)])
    for colocation, _ in grouped:
        group = grouped.get_group(colocation)
        participation_indices = [len(group['id'+str(i)].unique()) / cat_count[colocation[i-1]] for i in range(1, k+1)]
        prevalence = min(participation_indices)
        if prevalence >= thold :
            out[colocation] = Colocation(colocation, group, prevalence)
    return out

def generate_rules(min_cp, T, P, k):
    rules = set()
    for p in P:
        for item in p:
            antecedent = list(p)
            cat_indexes = [j for j in range(1,k+2)]
            cat_indexes.remove(p.index(item)+1)
            antecedent.remove(item)
            antecedent = tuple(antecedent) if len(antecedent) > 1 else antecedent[0]
            Tk = T[k].groupby(['cat'+str(i+1) for i in range(k+1)])
            Tkminus1 = T[k-1].groupby(['cat'+str(i+1) for i in range(k)])
            num = len(Tk.get_group(p).drop_duplicates(subset=['id'+str(index) for index in cat_indexes]))
            cp = num / len(Tkminus1.get_group(antecedent))
            if cp > min_cp:
                antecedent = (antecedent,) if isinstance(antecedent,str) else antecedent
                rules.update([Rule(antecedent, item, P[p].prevalence, cp)])
    return rules

def colocate(E, pos_column, class_column, id_column, K, theta, alpha, relation, thold):
    ET = E[[class_column,id_column]].drop_duplicates()[class_column].value_counts()
    start = datetime.now()
    k = 1
    p_new = {(e,):Colocation((e,), E[E[class_column]==e], 1) for e,_ in ET.iteritems()}
    c_new = set([(e,) for e,_ in ET.iteritems()])
    t_new = E[[class_column,id_column,pos_column]].rename(columns={class_column:'cat1',id_column:'id1',pos_column:'pos1'}).sort_values(by='cat1')
    r_new = set()

    C = [c_new] # Candidate locations
    P = [p_new] # Prevalent locations
    T = [t_new] # Table instances
    R = r_new # Co-location rules

    while((len(p_new) > 0) and k < K):
        print('|C'+str(k)+'| = '+str(len(c_new))+', |P'+str(k)+'| = '+str(len(p_new))+', |R'+str(k)+'| = '+str(len(r_new))+', Rows in T'+str(k)+' = '+str(len(t_new))+', Elapsed Time: '+str(datetime.now()-start))
        c_new = generate_candidate_colocation(P, k)
        t_new = generate_table_instances(c_new, T[k-1], p_new, k+1, relation, thold)
        p_new = select_prevalent(theta, t_new, k+1, ET)

        T.append(t_new)
        r_new = generate_rules(alpha, T, p_new, k)

        C.append(c_new)
        P.append(p_new)
        R.update(r_new)
        k += 1

    print('|C'+str(k)+'| = '+str(len(c_new))+', |P'+str(k)+'| = '+str(len(p_new))+', |R'+str(k)+'| = '+str(len(r_new))+', Rows in T'+str(k)+' = '+str(len(t_new))+', Elapsed Time: '+str(datetime.now()-start))
    return T, R