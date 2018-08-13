# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 17:48:32 2018

@author: Danni
"""
import random
import linecache

# Randomly partition dictionary into training, development and testing data
# with proportion of 81%, 9% and 10%
def Partition(dict_file='w2vdict.txt'):
    
    num_lines = sum(1 for line in open(dict_file))
    num_tr = int(0.81*num_lines)
    num_dev = int(0.09*num_lines)
    
    with open(dict_file, "r") as f:
        data = f.read().split('\n')
    
    random.shuffle(data)
    
    train_data = data[:num_tr]
    dev_data = data[num_tr:num_tr+num_dev]
    test_data = data[num_tr+num_dev:]
    
    # Create two "training" and "testing" dictionaries
    with open('test_dict.txt', 'w') as f: 
        for i in test_data:
            try:
                f.write(i+'\n')
            except:
                pass
    f.close()
    
    with open('dev_dict.txt', 'w') as f1: 
        for i in dev_data:
            try:
                f1.write(i+'\n')
            except:
                pass
    f1.close()
    
    with open('train_dict.txt', 'w') as f0: 
        for i in train_data:
            try:
                f0.write(i+'\n')
            except:
                pass
    f0.close()
    return train_data, dev_data, test_data

'''
# Read files with already generated training and testing data
# This is alternative
tr_pairs = open('train_dict.txt', 'r').readlines()
dev_pairs = open('dev_dict.txt', 'r').readlines()
ts_pairs = open('test_dict.txt', 'r').readlines()

'''

def main():
    train_data, dev_data, test_data = Partition()
    # Store training and testing words in both languages into lists
    zh_ts_embed = []
    en_ts_embed = []
    zh_tr_embed = []
    en_tr_embed = []
    zh_dev_embed = []
    en_dev_embed = []
    for i in test_data:
        tuples = i.split('\t')
        chinese = tuples[0]
        english = tuples[1]
        zh_ts_embed.append(chinese)
        en_ts_embed.append(english)
    for j in train_data:
        tuples = j.split('\t')
        chinese = tuples[0]
        english = tuples[1]
        zh_tr_embed.append(chinese)
        en_tr_embed.append(english)
    for k in dev_data:
        tuples = k.split('\t')
        chinese = tuples[0]
        english = tuples[1]
        zh_dev_embed.append(chinese)
        en_dev_embed.append(english)
    
    mono_zh = linecache.getlines('wordvectorAll.txt')
    with open("zh_ts_embed.txt", "w") as f1:
        count = 0
        for j in zh_ts_embed:
            count += 1
            if count%100 == 0:
                print (count)
            for line in mono_zh:
                fields = line.split(' ')
                zh_word = fields[0]
                if j == zh_word:
                    f1.write(line)
                    break
    f1.close()
    
    mono_en = linecache.getlines('mono-en-scaled')[1:]
    with open("en_ts_embed.txt", "w") as f2:
        for j in en_ts_embed:
            for line in mono_en:
                fields = line.split(' ')
                en_word =  fields[0]
                if j == en_word:
                    print (j)
                    f2.write(line)
                    break
    f2.close()
    
    with open("zh_dev_embed.txt", "w") as f3:
        count = 0
        for j in zh_dev_embed:
            count += 1
            if count%100 == 0:
                print (count)
            for line in mono_zh:
                fields = line.split(' ')
                zh_word = fields[0]
                if j == zh_word:
                    f1.write(line)
                    break
    f3.close()
    
    with open("zh_tr_embed.txt", "w") as f4:
        count = 0
        for j in zh_tr_embed:
            count += 1
            if count%100 == 0:
                print (count)
            for line in mono_zh:
                fields = line.split(' ')
                zh_word = fields[0]
                if j == zh_word:
                    f2.write(line)
                    break
    f4.close()
    
    with open("en_dev_embed.txt", "w") as f5:
        count = 0
        for j in en_dev_embed:
            count += 1
            if count%100 == 0:
                print (count)
            for line in mono_en:
                fields = line.split(' ')
                en_word =  fields[0]
                if j == en_word:
    #                print (j)
                    f3.write(line)
                    break
    f5.close()
    
    with open("en_tr_embed.txt", "w") as f6:
        count = 0
        for j in en_tr_embed:
            count += 1
            if count%100 == 0:
                print (count)
            for line in mono_en:
                fields = line.split(' ')
                en_word = fields[0]
                if j == en_word:
                    f4.write(line)
                    break
    f6.close()
    
if __name__ == '__main__':
    main()