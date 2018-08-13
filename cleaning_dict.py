# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 11:47:50 2017

@author: Danni
"""

import codecs
import re
import json

# clean up the original dictionary
def Parse_dict(dict_file='cedict_1_0_ts_utf-8_mdbg.txt'):
    dict_file = codecs.open(dict_file, encoding='utf-8')
    
    # Save parsed dictionary
    with open('newCEdict.txt', 'w') as f: 
        for line in dict_file:
            try:
                if line.startswith(("#", "#!")): # several comment lines at first
                    continue
                fields = line.split('/')
                chinese = fields[0].split(' ')
                zh_simp = chinese[1]
                for i in range(1, len(fields)): # iterate among definitions
                    translation = fields[i].strip()
                    if not translation == '':
                        # delete parenthesis and the contents within
                        b = re.sub(r'\([^)]*\)', '', translation).strip()
                        # we only need definitions with a sinlge word
                        # delete some definitions which contain Chinese characters starting with 'CL:'
                        if not ' ' in b and not b == '' and not 'CL:' in b:
                            f.write(zh_simp+'\t'+b+'\n')
                            print (zh_simp, '\t', translation)
            except:
                pass
       
# Construct a dictionary named 'zh_w2v_dict' to store all the Chinese words that have embeddings as keys        
def Chinese_vectors(zh_vector_file='wordvectorAll.txt'):
    mono_zh = open('wordvectorAll.txt', 'r')
    zh_w2v_dict = {}
    for line in mono_zh:
        try:
            fields = line.split(' ')
            zh_word = fields[0]
            zh_w2v_dict[zh_word] = 1
        except:
            pass
#    print (zh_w2v_dict.keys())
    return zh_w2v_dict

# Construct a dictionary named 'en_w2v_dict' to store all the English words that have embeddings as keys
def English_vectors(en_vector_file='mono-en-scaled'):
    mono_en = open('mono-en-scaled', 'r')
    en_w2v_dict = {}
    for line in mono_en:
        try:
            fields = line.split(' ')
            en_word = fields[0]
            en_w2v_dict[en_word] = 1
        except:
            pass
#    print (en_w2v_dict.keys())
    return en_w2v_dict

'''
# make sure that all the words appearing in dictionary also in Chinese word2vec
#new_dict_file = codecs.open('newCEdict.txt', encoding='utf-8')
zh_dict_file = codecs.open('zhdict.txt', encoding='utf-8')
#
#with open('zh_w2v_dict.json', 'r') as fp1:
#    zh_w2v_dict = json.load(fp1)
#fp1.close()
    
with open('en_w2v_dict.json', 'r') as fp2:
    en_w2v_dict = json.load(fp2)
fp2.close()
'''

# make sure that all the words appearing in dictionary also in Chinese word2vec
def Cleaned_dict(zh_w2v_dict, en_w2v_dict, new_dict='newCEdict.txt'):
    new_dict_file = codecs.open(new_dict, encoding='utf-8')
    # Open a new file for cleaning up dictionary
    with open('w2vdict.txt', 'w') as f: 
        for line in new_dict_file:
            try:
                fields = line.split('\t')
                chinese = fields[0]
                english = fields[1]
                if chinese in zh_w2v_dict.keys():
                    if english in en_w2v_dict.keys():
                        f.write(chinese+'\t'+english+'\n')
                        print (chinese, english)
            except:
                pass

'''
# Open a new file for cleaning up dictionary
with open('w2vdict.txt', 'w') as f: 
    for line in zh_dict_file:
        try:
            fields = line.split('\t') 
            chinese = fields[0]
            print ('chinese:', chinese)
            english = fields[1].strip('\n')
            print ('english:', english)
            if english in en_w2v_dict.keys():
                print ('find English!\n')
#            if chinese in zh_w2v_dict.keys():
#                print ('find Chinese!')
                f.write(chinese+'\t'+english+'\n')
        except:
            pass
f.close()
'''

def main():
    Parse_dict()
    zh_w2v_dict = Chinese_vectors()
    with open('zh_w2v_dict.json', 'w') as fp:
        json.dump(zh_w2v_dict, fp)
    en_w2v_dict = English_vectors()    
    with open('en_w2v_dict.json', 'w') as fp:
        json.dump(en_w2v_dict, fp)
    Cleaned_dict(zh_w2v_dict, en_w2v_dict)
    
if __name__ == '__main__':
    main()