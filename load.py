"""Functions for loading data."""

from collections import defaultdict

import numpy as np
import pandas as pd


def load_subjects(subjs, sessions, path):
    """Load data."""
    
    ### Create empty dataframe for data
    dd_gp = defaultdict(list)

    ### Loop through subjects ###
    for subj in subjs:

        if 'J' in subj:
            exp_group = 'Young adults'
        elif 'Z' in subj:
            exp_group = 'Teenagers'
        else:
            exp_group = 'N/A'   
            
        ### Loop through sessions ###
        for sesh in sessions:
            ### Assign corresponding condition ###
            if sesh == 0:
                cond = 'FR'
                lst_len = range(12)
                if subj == 'R1510Z':
                    lst_len = range(1,12)
            elif sesh == 1:
                cond = 'FR_MP'
                lst_len = range(1,12)
                if subj == 'R1510Z':
                    lst_len = range(2,12)
                    
            ### Loop through lists (trials) ###
            for lst in lst_len:
                file_enc = path + '/%s/session_%s/%s.lst' % (subj, sesh, lst)
                file_rec = path + '/%s/session_%s/%s-resp.lst' % (subj, sesh, lst)
                
                #file_enc = '/home1/tamara.gedankien/data/FR1/%s/session_%s/%s.lst' % (subj, sesh, lst)
                #file_rec = '/home1/tamara.gedankien/data/FR1/%s/session_%s/%s-resp.lst' % (subj, sesh, lst)

                ### Open encoding and recall files ###
                with open(file_enc, 'r') as f_enc, open(file_rec, 'r') as f_rec:
                    line_enc = f_enc.read().splitlines()
                    line_rec = f_rec.read().splitlines()
                    
                    intrus = [j for j in [i for i in line_rec if i not in line_enc] if j]
                    intrus_count = len(intrus)
                    
                    ### Loop through words in encoding list ###
                    for serialpos, word in enumerate(line_enc):
                        if word in line_rec:
                            recalled = 1
                            recorder = np.where(word == np.array(line_rec))[0][0]                                
                        elif word not in line_rec:
                            recalled = 0
                            recorder = -1
                        
                        #########################   
                        #### CREATE DATAFRAME ###
                        #########################
                        info_for_df = {'subject': subj,
                                       'exp_group': exp_group,
                                       'condition': cond,
                                       'session': sesh,
                                       'type': 'WORD',
                                       'trial': lst+1,
                                       'intrus_per_trial': intrus_count,
                                       'serialpos': serialpos+1,
                                       'recorder': recorder+1,
                                       'item_name': word,
                                       'recalled': recalled}

                        for key, value in info_for_df.items():
                            dd_gp[key].append(value)
                        df = pd.DataFrame(data = dd_gp)

                    #df.to_pickle('/home1/tamara.gedankien/BRAINYAC_FR_data.pkl')
    return df
