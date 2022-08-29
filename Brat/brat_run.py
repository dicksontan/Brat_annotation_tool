from brat_clean import cleaner, stop_words
import pandas as pd
import en_ner_bionlp13cg_md
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

class get_ents:
    
    def __init__(self,cleaned_df):
        self.cleaned_df = cleaned_df
        self.med_nlp = en_ner_bionlp13cg_md.load()
        self.start_index = 0
        self.end_index = 0
        self.brat_table_2 = pd.DataFrame()
        self.doc = pd.DataFrame()
    
    def get_ents_now(self, folder_path, start_index = None, end_index = None):

        '''Here, we are creating a dataframe whose values we will use for brat. '''

        ent_labels = []

        i = 1

        for doc in self.med_nlp.pipe(self.cleaned_df['med_str'][start_index:end_index].to_list()):

            brat_table = pd.DataFrame(doc.to_json()['ents'])

            brat_table['ents'] = ['\t'+ str(ent) for ent in doc.ents]
            brat_table['label'] = '\t'+ brat_table['label']

            brat_table['brat_tag'] = ['T' + str(i) for i in brat_table.index]
            brat_table['start'] = [' ' + str(i) for i in brat_table.start]
            brat_table['end'] = [' ' + str(i) for i in brat_table.end]

            brat_table_2 = brat_table[['brat_tag','label','start','end','ents']]

            labels_1 = brat_table_2['label'].values.tolist()

            ent_labels = ent_labels + labels_1

            self.brat_table_2 = brat_table_2

            self.start_index = start_index
            self.end_index = end_index

            file_name = 'brat'+ f'_{i}'

            self.save_annot_files(folder_path,doc,file_name)

            i+=1

        self.save_config_files(folder_path,ent_labels)

    def save_annot_files(self,folder_path,doc,file_name):

        # saving annotations to local folder

        np.savetxt(folder_path+f'/{file_name}.ann', self.brat_table_2.values, fmt='%s', delimiter = '')

        # saving text file to local folder

        np.savetxt(folder_path+f'/{file_name}.txt',pd.Series(str(doc)), fmt='%s')

    def save_config_files(self, folder_path, ent_labels):

        #creating unique labels

        unique_labels = list(set(ent_labels))

        unique_labels = [label.replace('\t','') for label in unique_labels]

        # saving entity labels to config file

        f = open(folder_path + '/annotation.conf','w')

        text = '[entities]\n' + '\n'.join(unique_labels)

        f.write(text)

        f.close()

if __name__ == "__main__":

    # Input 1: enter path of dataset file to create object with dataframe
    dataset_path = '/Users/user_1/Desktop/Vs_Code_Projects/brat/datasets/mtsamples.csv'
    # Input 2: index range which you want to filter up to
    start_index = 6
    end_index = 8
    # Input 3: save files to output path
    folder_path = '/Users/user_1/Desktop/brat_annotations'
    # Input 4: creating a list of stop words you wish to add to general count vec stop words
    add_stop_words = ['en','wa','ha']

    # creating stop words list

    stop_words_1 = stop_words().gen_stop_words(add_stop_words)

    # path of dataset file to create object with dataframe

    dataset_path = dataset_path

    #create cleaner object to clean df
    cleaner = cleaner(dataset_path,stop_words_1)

    # helps to generate a cleaned_df in cleaner object
    cleaner.clean()

    # create object to process and save taggings

    ent_obj = get_ents(cleaner.cleaned_df)

    # index which you want to filter up to

    start_index = start_index
    end_index = end_index
    folder_path = folder_path

    ent_obj.get_ents_now(folder_path,start_index,end_index)