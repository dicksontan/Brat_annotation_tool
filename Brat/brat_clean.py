import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer 

class cleaner:
    
    def __init__(self,path,new_stop_words):
        self.data_df = pd.read_csv(path).set_index(['index'])
        self.new_stop_words = new_stop_words
        self.cleaned_df = pd.DataFrame()

    def lemmatize_sent(self,sent):

        '''Function for lemmatizing sentences'''
        
        word_list = word_tokenize(sent)

        lemma = WordNetLemmatizer()

        lemma_list = ' '.join([lemma.lemmatize(w) for w in word_list if w not in self.new_stop_words])

        return lemma_list

    def clean(self):

        '''Clean and lemmatize sentences before tagging'''

        # combining all the strings together for cleaning

        str_series = self.data_df['description']+ self.data_df['medical_specialty']+ self.data_df['sample_name']+self.data_df['transcription']
        
        concat_df = pd.DataFrame({'med_str':str_series,'labels': self.data_df['keywords']})
        
        # dropping null values from combined list of medical strings

        concat_df2 = concat_df.dropna(subset=['med_str'])

        #setting all to lower case

        concat_df2['med_str'] = concat_df2['med_str'].apply(str.lower)

        #filter out punctuation

        concat_df3 = concat_df2.copy()

        # concat_df3['med_str'] = concat_df2['med_str'].str.replace(r'([^\w\s])',' ')

        # concat_df3['med_str'] = concat_df3['med_str'].str.replace(r'(_)', ' ')

        # # filter out single digit numbers

        # concat_df4 = concat_df3.copy()

        # concat_df4['med_str'] = concat_df3['med_str'].str.replace('(\d+)','')

        # #filter out lone letters

        # concat_df5 = concat_df4.copy()

        # concat_df5['med_str'] = concat_df4['med_str'].str.replace(r'(\b[a-zA-Z]\b)','')

        # #lemmatize sentences

        # concat_df6 = concat_df5.copy()

        # concat_df6['med_str'] = concat_df5['med_str'].map(self.lemmatize_sent)

        # self.cleaned_df = concat_df6

        self.cleaned_df = concat_df3

        # if you want want to do data cleaning, then set self.cleaned_df = concat_df6 and uncomment cleaning lines above

class stop_words:

    def __init__(self):
        self.stop_words_list = CountVectorizer(stop_words= 'english').get_stop_words()

    def gen_stop_words(self,add_stop_words):

        '''Function to generate stop words and add new stop words'''

        new_stop_words = []

        for word in self.stop_words_list:
            new_stop_words.append(word)

        new_stop_words.extend(add_stop_words)

        return new_stop_words

