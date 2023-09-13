#!/usr/bin/env python
# coding: utf-8

# In[1]:


from itertools import combinations,permutations
import pandas as pd 
import numpy as np


# In[2]:


def apriori(csv,min_support,min_confidence):
    df = pd.read_csv(csv,header = None).T
    dic = df.to_dict()
    items=[]
    trans = {}
    for key, value in dic.items():
        trans[key] = []
        for j in value:
            if(not pd.isnull(value[j])):
                trans[key].append(value[j])
                if(value[j] not in items):
                    items.append(value[j])
    min_support = len(trans)*min_support
    k= 1
    result = []
    L = items
    while(L != []):
        L = [','.join(i) for i in combinations(L, k)]
        C = pd.DataFrame(index = trans.keys(),columns=L)
        support_count = support(C,trans)
        support_count = support_count[support_count['Value'] >= min_support]
        L = []
        for l in support_count.index:
            hold = l.split(',')
            result.append(hold)
            for i in hold:
                if(i not in L):
                    L.append(i)
        k+=1
    association_rules = get_association_rules(result,trans,min_support,min_confidence)
        
    return [result,association_rules]


# In[3]:


def get_support(items,trans):
    count = 0
    for tran in trans.keys():
        flag = True
        for i in items:
            if(i not in trans[tran]):
                flag = False
        if(flag):
            count+=1
    return count


# In[4]:


def get_confidence(items1,items2,trans):
    support1 = get_support(items1,trans)
    support2 = get_support(items2,trans)
    if(support2 == 0):
        return 0
    conf = support1/support2
    return conf


# In[5]:


def support(df,trans):
    for item in df.columns:
        item_split = item.split(',')
        for key,items in trans.items():
            flag =0
            for i in item_split:
                if(i not in items):
                    flag = 1
            if(flag == 0):
                if(pd.isnull(df[item][key])):
                    df[item][key] = 1
                else:
                    df[item][key] += 1
    return pd.DataFrame(df.sum(),columns=['Value'])


# In[6]:


def get_association_rules(frequent_item_sets,trans,min_support,min_confidence):
    rules = {}
    for frequent_item_set in frequent_item_sets:
        if(len(frequent_item_set)>1):
            for i in range(1,len(frequent_item_set)):
                for j in [list(k) for k in combinations(frequent_item_set,i)]:
                    other = [z for z in frequent_item_set if z not in j]
                    conf1 = get_confidence(frequent_item_set,j,trans)
                    rule1 = str(j)+' -> '+str(other)
                    conf2 = get_confidence(frequent_item_set,other,trans)
                    rule2 = str(other)+' -> '+str(j)
                    if(rule1 not in rules.keys() and conf1>=min_confidence):
                        rules[rule1] = conf1
                    if(rule2 not in rules.keys() and conf2>=min_confidence):
                        rules[rule2] = conf2
    return rules


# In[ ]:


print("Welcome to Richards Apriori Algorithm.")
print("\t 1)  Amazon")
print("\t 2)  BestBuy")
print("\t 3)  Kmart")
print("\t 4)  Nike")
print("\t 5)  ESPN")
print("\t 6)  Custom")
dataset = int(input("\nPlease choose your dataset: "))
if(dataset == 1):
    file = 'amazon_transactions.csv'
elif(dataset == 2):
    file = 'bestbuy_transactions.csv'
elif(dataset == 3):
    file = 'kmart_transactions.csv'
elif(dataset == 4):
    file = 'nike_transactions.csv'
elif(dataset == 5):
    file = 'espn_transactions.csv'
elif(dataset == 6):
    file = input('Please enter your CSV files name:')
min_support = input('Please enter the minimum support(0<=minimum support<=1):')
min_confidence = input('Please enter the minimum confidence(0<=minimum confidence<=1):')
result = apriori(file,float(min_support),float(min_confidence))
print()
print('Under the minimum support of',min_support,'this is your frequent items list:')
for i in result[0]:
    print('\t'+str(i))
print()
print('Under the minimum support of',min_support,'and the minimum confidence of',min_confidence,'these are your association rules:')
for i in result[1].keys():
    print('\t'+i,'Confidence: '+str(result[1][i]))

