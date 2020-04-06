# MT
This is a python implementation of my independent study in 2017 Fall. Below is the description of our pipelined system. All generated files are in `output/` folder.

## Cleaning Dictionary
The original Chinese-English dictionary, Chinese word embeddings `wordvecetorAll.txt` and English scaled word embeddings `mono-en-scaled` are in `data/` folder.

Run `python cleaning_dict.py`, we will get two dictionaries `newCEdict.txt` and `w2vdict.txt`. `newCEdict.txt` contains all the valid entries. While `w2vdict.txt` only have pairs that both Chinese and English words appear in embedding files in `data/`

## Preparing data

Run `python mapping.py`, `w2vdict.txt` will be divided to `train_dict.txt`, `dev_dict.txt` and `test_dict.txt`

We also get embeddings for training, dev and test data (both languages). They are stored as `en_tr_embed.txt`, `en_dev_embed.txt`, `en_ts_embed.txt`, `zh_tr_embed.txt`, `zh_dev_embed.txt` and `zh_ts_embed.txt`

## Training
Run `python nnlinreg4xv.py --traininput en_tr_embed.txt --trainoutput`<br>`zh_tr_embed.txt --testinput en_dev_embed.txt --testoutput zh_dev_embed.txt`<br>`--verbose True --num_epochs 10000 --num_hidden 10000 --project`<br>`pruned_mono_en_scaled.txt --towrite en-projected_new.txt`

where `pruned_mono_en_scaled.txt` has the same content as `mono-en-scaled` except skipping the first line headers. `en-projected_new.txt` is the predicted translation embeddings for English test words.

## Translating
Run `python Get_idx_predEmbed.py`, we will get `pred_embed.txt`. Each line of this file contains: a test english word + index + projected embedding in `en-projected_new.txt`. Index is the line number of the test word's embedding in `pruned_mono_en_scale.txt`

Run `python Get_pred.py`, we will get `pred_label_all.txt`, which contains top-10 translation candidates and corresponding cosine similarity with predicted embedding.

## Evaluation
Run `python Eval.py` to get some stats and plots of the results. We also consult `ecdict.csv` to check the accuracy of translation.

PS: These files are not pushed due to file size:
`mono-en-scaled`, `wordvectorAll.txt`, `en_tr_embed.txt`, `zh_tr_embed.txt`, `en-projected_new.txt` and `ecdict.csv`
