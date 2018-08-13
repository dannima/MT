# -*- coding: utf-8 -*-
"""
Created on Wed May  9 14:48:12 2018

@author: Danni
"""

import codecs
import csv
import numpy as np
import matplotlib.pyplot as plt


def Get_dicts(dictfile='newCEdict.txt', csvfile='ecdict.csv'):
    # Translation ground truth dictionary
    gt_dict = {}
    new_dict_file = codecs.open(dictfile, encoding='utf-8')
    for line in new_dict_file:
        try:
            fields = line.split('\t')
            chinese = fields[0]
            english = fields[1].strip('\n')
            if english not in gt_dict:
                gt_dict.setdefault(english, [])
                gt_dict[english].append(chinese)
            else:
                gt_dict[english].append(chinese)
        
        except:
            pass
    return gt_dict

def Get_ecdict(dictfile='test_dict.txt', csvfile='ecdict.csv'):
    csv_dict = {}
    new_dict_file = codecs.open(dictfile, encoding='utf-8')
    f = open(csvfile, 'r')
    csv_file = csv.reader(f)
    cnt = 0
    print ('Finish loading test dictionary!')
    for line in new_dict_file:
        cnt += 1
        if cnt%10 == 0:
            print (cnt)
        try:
            fields = line.split('\t')
            english = fields[1].strip('\n')

            # Build dict from en-zh dictionary
            f.seek(0)
            for row in csv_file:
                if row[0] == english:
                    if english not in csv_dict:    
                        csv_dict.setdefault(english, [])
                        csv_dict[english].append(row[3])
                    else:
                        csv_dict[english].append(row[3])
                    break
        except:
            pass
    return csv_dict


# Get top-k translations from predicted labels
def Get_translations(gt_dict, csv_dict, k, predfile='pred_label_all.txt'):
    predictions = open(predfile, 'r').readlines()
    N = len(predictions)
    cnt = 0
    Total_scores = []
    Translations = []
    Hit_score = []
    Ranks = []
    Correct_trans = []
    
    for i, line in enumerate(predictions):
        line = line.strip()
        fields = line.split(', ')
        first_entry = fields[0].split('\t')
        english = first_entry[0]
        Chinese_candidates = []
        Scores = []
        
        # Get k Chinese translation options for one English word
        for j, trans in enumerate(fields[:k]):
            if j == 0:
                Chinese_candidates.append(first_entry[1])
                Scores.append(float(first_entry[-1]))
            else:
                Chinese_candidates.append(trans.split('\t')[0])
                Scores.append(float(trans.split('\t')[1]))
        Total_scores.append(Scores)
        Translations.append(Chinese_candidates)
        flag = 1
        
        # Look up k candidates in both dictionaries
        for p, chinese in enumerate(Chinese_candidates):
            if chinese in gt_dict[english]:
                flag = 0
            else:
                try:
                    for entry in csv_dict[english]:
                        if chinese in entry:
                            flag = 0
                except:
                    pass
            if not flag: 
                Correct_trans.append(chinese)
                cnt += 1
                Hit_score.append(Scores[p])
                Ranks.append(p+1)
                break
        if flag:
            Correct_trans.append(None)
            Hit_score.append(0)
            Ranks.append(0)
                
    precision = cnt/N
    return precision, Hit_score, Ranks

def Plot_acc(Acc):
    plt.plot(list(range(1, 11)), Acc)
#    plt.title('Accuracy with Top-k Translations')
    plt.xlabel('k')
    plt.ylabel('Acc')
    plt.xlim(1, 10)
    plt.show()

def Plot_hits(Hits):
    # Calculate the average score of all correct translations
    avg_scores = []
    for i in Hits:
        new_score = []
        for j in i:
            if j:
              new_score.append(j)
        avg_scores.append(np.mean(new_score))
    
    plt.plot(list(range(1, 11)), avg_scores)
#    plt.title('Top-k Average Score of All Correct Translations')
    plt.xlabel('k')
    plt.ylabel('Avg Score');
    plt.xlim(1, 10)
    plt.show()  
    
def Plot_rank(Ranks):
    labels, counts = np.unique(Ranks, return_counts=True)
    print (labels, counts)
    plt.bar(labels, counts, align='center')
    plt.gca().set_xticks(labels)
#    plt.title("Rank Histogram with Top-10 Translation")
    plt.xlabel("Rank")
    plt.ylabel("Frequency")
    plt.xlim(0.5, 10.5)
    plt.ylim(0, 1500)
    plt.show()

def Plot_MMR(Total_Ranks):
    All_mmr = []
    for rank in Total_Ranks:
        mmr = MMR(rank)
        All_mmr.append(mmr)
        
    plt.plot(list(range(1, 11)), All_mmr)
    plt.xlabel('k')
    plt.ylabel('MMR');
    plt.xlim(1, 10)
    plt.show()  
    
def MMR(Ranks):
    new_rank = []
    for i in Ranks:
        if i > 0:
            new_rank.append(1/i)
        else:
            new_rank.append(0)
    return np.mean(new_rank)

def main():
    gt_dict = Get_dicts()
    csv_dict = Get_ecdict()
    
    Acc = []
    Hits = []
    Total_Ranks = []
    for i in range(1, 11):
        precision, Hit_score, Ranks = Get_translations(gt_dict, csv_dict, i)
        Acc.append(precision)
        Hits.append(Hit_score)
        Total_Ranks.append(Ranks)
        
    # Generate plots
    Plot_acc(Acc)
    Plot_hits(Hits)
    Plot_rank(Ranks)
    Plot_MMR(Total_Ranks)
    
if __name__ == '__main__':
    main()