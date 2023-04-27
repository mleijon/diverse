from gensim.models import LdaMulticore
from gensim.corpora import mmcorpus, Dictionary
from pyLDAvis import save_html
import pyLDAvis.gensim_models as gensim_vis
import os
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
        '--noplot',
        action='store_true'
    )

DICT_PATH = os.path.join('corpus', 'corpus_dict')
CORP_PATH = os.path.join('corpus', 'full_corpus.mm')

def train_and_save():
    args = parser.parse_args()

    num_topics = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1500]
    alpha = ['asymmetric', 'symmetric']
    eta = ['auto', 'symmetric']

    dictionary = Dictionary.load_from_text(DICT_PATH)
    corpus = mmcorpus.MmCorpus(CORP_PATH)
    with open('debug.txt', 'w') as handle:
        handle.write(f'Trying to pre-load corpus into ram.\n')
    corpus = [doc for doc in corpus]
    tot_it = len(num_topics)*len(alpha)*len(eta)
    i = 0
    for t in num_topics:
        for a in alpha:
            for e in eta:
                tic = time.perf_counter()

                model_name = f"model_{t}_{a}_{e}"
                output_path = os.path.join('models', model_name)

                with open('debug.txt', 'w') as handle:
                    handle.write(f'Trying to train {model_name}.\n')
                model = LdaMulticore(corpus, id2word=dictionary, chunksize=4096, decay=0.5, offset=64,
                            num_topics=t, eta=e, alpha=a, workers=60)
                
                with open('debug.txt', 'a') as handle:
                    handle.write(f'Successfully trained {model_name} -> Trying to save it to {output_path}\n')
                model.save(output_path)

                if not args.noplot:
                    with open('debug.txt', 'a') as handle:
                        handle.write(f'Successfully saved {model_name} -> Trying to prepare .html with plots\n')
                    p = gensim_vis.prepare(model, corpus, dictionary)

                    html_oppath = os.path.join('plots', model_name + '.html')
                    with open('debug.txt', 'a') as handle:
                        handle.write(f'Successfully prepared .html -> Trying to save it to {html_oppath}.\n')

                    with open(html_oppath, 'w') as f:
                        save_html(p, f)
                    
                    with open('debug.txt', 'a') as handle:
                        handle.write(f'Successfully saved .html -> Trying to log info.\n')
                else:
                    with open('debug.txt', 'a') as handle:
                        handle.write(f'Successfully saved {model_name} -> Tring to log info.\n')

                i += 1
                toc = time.perf_counter()
                hours, minutes = (toc-tic)/60/60, (toc-tic)/60
                log_string = f"Trained and visualized model: {model_name}. Took {hours} hours / {minutes} minutes. "
                log_string = log_string + f"Done with {i}/{tot_it} models."
                with open('log.txt', 'a') as f:
                    f.write(log_string + '\n')
    
                with open('debug.txt', 'a') as handle:
                    handle.write(f'Successfully logged info -> Training new model - debug file for this model will now be cleared.\n')

if __name__ == '__main__':
    train_and_save()
