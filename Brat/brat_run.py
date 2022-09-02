from brat_clean import cleaner, stop_words
import pandas as pd
import en_ner_bionlp13cg_md
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

class get_ents:
    
    def __init__(self,cleaner):
        self.cleaned_df = cleaner.cleaned_df
        self.data_df = cleaner.data_df
        self.med_nlp = en_ner_bionlp13cg_md.load()
        self.start_index = 0
        self.end_index = 0
        self.brat_table_2 = pd.DataFrame()
        self.doc = pd.DataFrame()
        self.no_labels = []
    
    def get_ents_now(self, folder_path, brat_index, start_index = None, end_index = None):

        ent_labels = []

        ''' Here, we are creating a dataframe whose values we will use for brat. '''

        if brat_index is not None:

            brat_index = [int(i) for i in brat_index]

        if brat_index is None:
            brat_index = list(self.cleaned_df[start_index: end_index].index)

        for i in brat_index:

            doc = self.med_nlp(self.cleaned_df.loc[i,'med_str'])

            # Creating dataframe format to put into brat

            brat_table = pd.DataFrame(doc.to_json()['ents'])

            if brat_table.empty:
                self.no_labels.append(i)
                continue

            brat_table['ents'] = ['\t'+ str(ent) for ent in doc.ents]
            brat_table['label'] = '\t'+ brat_table['label']

            brat_table['brat_tag'] = ['T' + str(i) for i in brat_table.index]
            brat_table['start'] = [' ' + str(i) for i in brat_table.start]
            brat_table['end'] = [' ' + str(i) for i in brat_table.end]

            brat_table_2 = brat_table[['brat_tag','label','start','end','ents']]

            self.brat_table_2 = brat_table_2

            labels_1 = brat_table_2['label'].values.tolist()

            #ent_labels is to get labels to store into config file

            ent_labels = ent_labels + labels_1

            # standardize file naming convention to index, specialty and sample

            index_name = str(i).zfill(4)
            specialty_name = self.data_df.loc[i,'medical_specialty']
            sample_name = self.data_df.loc[i,'sample_name']

            file_name = index_name + '_' + specialty_name +  '_' + sample_name
            file_name = file_name.replace(' ','_')
            file_name = file_name.replace("/",'_')

            self.save_annot_files(folder_path,doc,file_name)

        self.save_config_files(folder_path,ent_labels)

        print(f'no labels for: {self.no_labels}')

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

        text = '[entities]\n\n' + '\n'.join(unique_labels) +'\n\n[relations]\n\n[events]\n\n[attributes]'

        f.write(text)

        f.close()

if __name__ == "__main__":

    # Input 1: enter path of dataset file to create object with dataframe
    # e.g. /Users/user_1/Desktop/Vs_Code_Projects/brat/datasets/mtsamples.csv

    dataset_path = input('Please enter path to your dataset:')

    # Input 2: Enter specific indexes of the dataset in which you want to run spacy tagging on.
    # e.g. 40, 70, 173
    # If you want a range, enter range
    # If you want to loop though every index in the dataset, then just enter all

    index_input = input('Please enter specific indexes: ')

    if index_input != 'range':
        brat_index = index_input.split()
        start_index = None
        end_index = None

    # optional input if we want range

    if index_input == 'range':

        brat_index = None

        # Input 3a: index range which you want to start filter
        # e.g. start = 6

        input_start_index = input('Please enter start range index which you want to start loop in dataset: ')
        start_index = int(input_start_index)

        # Input 3b: index range which you want to filter up to. This is inclusive. So if you want till 8 then enter 8
        # e.g. end = 8

        input_end_index = input('Please enter end range index which you want to end loop in dataset: ')
        end_index = int(input_end_index)+1

    if index_input == 'all':

        brat_index = None
        start_index = None
        end_index = None

    # Input 4: enter output path to save files to
    # e.g. /Users/user_1/Desktop/brat_annotations
    # e.g. /Users/user_1/Desktop/a

    folder_path = input('Please enter output path for output files:')

    # Input 5: Input a list of stop words you wish to add to general count vec stop words
    # e.g. en wa ha

    add_stop_words = input('Please enter additional stop words: ').split()

    # creating stop words list

    stop_words_1 = stop_words().gen_stop_words(add_stop_words)

    # path of dataset file to create object with dataframe

    dataset_path = dataset_path

    #create cleaner object to clean df
    cleaner = cleaner(dataset_path,stop_words_1)

    # helps to generate a cleaned_df in cleaner object
    cleaner.clean()

    # create object to process and save taggings

    ent_obj = get_ents(cleaner)

    # index which you want to filter up to

    start_index = start_index
    end_index = end_index
    brat_index = brat_index
    folder_path = folder_path

    ent_obj.get_ents_now(folder_path, brat_index, start_index, end_index)