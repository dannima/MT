# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 15:36:25 2018

@author: Danni
"""
from scipy import spatial
import linecache
import numpy as np
import collections

# For each word in Chinese, we search in projected English embeddings to find one with the highest cosine
# similarity, and that one is the top-1 translation candidate.
'''
mono_proj = linecache.getlines('en-projected_new.txt')
proj_dict = {}
for idx, line in enumerate(mono_proj):
    fields = line.strip('\n').split(' ')
    proj_vec = np.asarray(fields, dtype=np.float32)
    proj_dict[idx] = proj_vec

zh_ts = linecache.getlines('zh_ts_embed.txt')
for line in zh_ts:
    fields = line.strip('\n').split(' ')
    ≈ = fields[0]
    zh_vec = np.asarray(fields[1:], dtype=np.float32)
'''    

# Build a dictionary for all Chinese word vectors we have (all the possible translation candidates)
# zh_wordvector = 'wordvectorAll.txt'
def build_zh_dict(zh_wordvector):
    mono_zh = linecache.getlines(zh_wordvector)
    zh_embed = collections.OrderedDict()
    cnt = 0
    for line in mono_zh[1:]:
        if cnt % 100000 == 0:
            print (cnt)
        fields = line.split(' ')
        zh_word = fields[0]
        fields[-1] = fields[-1].strip('\n')
        zh_vec = np.asarray(fields[1:], dtype=np.float32)
        zh_embed[zh_word] = zh_vec
        cnt += 1
    print ('Finished building Chinese Dictionary!')
    zh_embed_key_list = list(zh_embed.keys())
    zh_embed_value_list = list(zh_embed.values())
    
    return zh_embed_key_list, zh_embed_value_list
    
    ## The list of values (Chinese word embeddings after conversion)
    #zh_embed_value_list_cvt = []
    #
    #for zh_vec in zh_embed_value_list:
    #    str_zh_vec = ' '.join(str(x) for x in zh_vec)
    #    zh_embed_value_list_cvt.append(str_zh_vec)
    
def main():
    zh_embed_key_list, zh_embed_value_list = build_zh_dict('wordvectorAll.txt')
    with open('pred_embed.txt', 'r') as f2:
        data = f2.readlines()

    # Get the predicted label  
    cnt = 0
    with open('pred_label_all.txt', 'w') as f3:
        for line in data:
            print (cnt)
            # Get the top-10 prediction
            top10 = []
            fields = line.strip('\n').split(' ')
            test_en_word = fields[0]
            proj_embed = np.asarray(fields[2:], dtype=np.float32).tolist()
            for word_idx, zh_word_embed in enumerate(zh_embed_value_list):
                zh_vec = zh_word_embed.tolist()
                cos_sim = 1 - spatial.distance.cosine(proj_embed, zh_vec)
                if word_idx < 10:
                    top10.append((word_idx, cos_sim))
                    top10.sort(key=lambda a: a[1], reverse=True)
                else:
                    if cos_sim > top10[-1][1]:
                        top10.append((word_idx, cos_sim))
                        top10.sort(key=lambda a: a[1], reverse=True)
                        top10 = top10[:10]
      
            f3.write(test_en_word+'\t')
            print (test_en_word)
            for i in top10[:9]:
                label = zh_embed_key_list[i[0]]
                print (label,)
                f3.write(label+'\t'+str(i[1])+', ')
            f3.write(zh_embed_key_list[top10[-1][0]]+'\t'+str(top10[-1][-1])+'\n')
            
            cnt += 1
            
if __name__ == '__main__':
    main()