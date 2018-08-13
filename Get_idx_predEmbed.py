# -*- coding: utf-8 -*-
"""
Created on Mon May  7 14:49:09 2018

@author: Danni
"""

import linecache
import numpy as np
import collections

# Build an ordered dictionary for all the English and Chinese words in pruned_mono_en_scaled.txt and 
# en-projected_new.txt to quickly retrieve corresponding line number
def Get_en_embed(vector_file='pruned_mono_en_scaled.txt'):
    mono_en = linecache.getlines(vector_file)
    en_embed = collections.OrderedDict()
    cnt = 0
    for line in mono_en:
        if cnt % 100000 == 0:
            print (cnt)
        fields = line.strip('\n').split(' ')
        en_word = fields[0]
        en_vec = np.asarray(fields[1:], dtype=np.float32)
        en_embed[en_word] = en_vec
        cnt += 1
    return en_embed

def Get_projected_embed(vector_file='en-projected_new.txt'):
    proj_zh = linecache.getlines(vector_file)
    proj_zh_embed = {}
    cnt = 0
    for line in proj_zh:
        if cnt % 100000 == 0:
            print (cnt)
        fields = line.strip('\n').split(' ')
        zh_vec = np.asarray(fields, dtype=np.float32)
        proj_zh_embed[cnt] = zh_vec
        cnt += 1
    return proj_zh_embed
    
# Convert proj_zh_embed into list for indexing
#project_zh_items = list(proj_zh_embed.items())
    
def main(test_dict='test_dict.txt'):
    en_embed = Get_en_embed()
    proj_zh_embed = Get_projected_embed()
    # Convert the keys of en_embed into list
    en_embed_list = list(en_embed.keys())
    
    # For each English word in test dictionary, get the translation from wordvectorAll.txt    
    with open(test_dict, 'r') as f0:
        test_lines = f0.read().split('\n')
    
    # write to file 'pred_embed.txt':
    #   test english word + index + projected embedding in 'en-projected_new.txt'  
    with open('pred_embed.txt', 'w') as f1:
        cnt = 0
        for line in test_lines:
            if cnt % 500 == 0:
                print (cnt)
            fields = line.split('\t')
            test_en_word = fields[1]
            # Get the index (line number in mono-en-scale) of the test English word
            idx = en_embed_list.index(test_en_word)
    #        print ('idx:', idx)
            # Find the corresponding projected embedding (Chinese embeddings in en-projected_new.txt)
            corr_embed = proj_zh_embed[idx]
            str_embed = ' '.join(str(x) for x in corr_embed)
            try:
                f1.write('%s %s %s\n' %(test_en_word, idx, str_embed))
            except:
                pass
            cnt += 1
    f1.close()

if __name__ == '__main__':
    main()