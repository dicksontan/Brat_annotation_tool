import pandas as pd
from pathlib import Path

def generate_annotation_csv(annotated_index,folder_path):

    '''This function extracts labelling data from the annotated brat files, 
    stores them into a df and outputs a csv'''

    extract_index = [str(x).zfill(4) for x in annotated_index]

    concat_list = []

    files = Path(folder_path).glob('*')

    # looping through files to match file name and check if it is an annotation file

    for file in files:

        file_num = file.name[:4]
        
        if file_num in extract_index:

            if file.name[-3:] == 'ann':
                with open(file) as f:
                    lines = f.readlines()

                    print(file.name)

                # transforming annotation file to store into df

                transf_1 = [x.replace("\t"," ") for x in lines]
                transf_2 = [x.replace("\n"," ") for x in transf_1]
                transf_3 = [x.split(' ',4) for x in [x.strip() for x in transf_2]]

                df_1 = pd.DataFrame(transf_3)

                df_1.columns = ['tag_index','class','start','end','entity']

                df_1['index'] = file_num

                concat_list.append(df_1)
                
    labelled_df = pd.concat(concat_list)

    return labelled_df


if __name__ == '__main__':

    # input1: amend this index according to the files which have been annotated
    # e.g. 40 43 110 149 173 226 257 319

    annotated_index = input('Please enter index of files which have been man labelled: ').split()

    # input2: folder_path_man is the path where the extracted brat files that have been man labelled are from
    # e.g. ./Desktop/brat_extracted/brat_annotations

    folder_path_man = input('Please enter path where the extracted man labelled brat files are in: ')

    # input3: folder_path_2 is the path where the extracted brat files that have been labelled by spacy are from
    # e.g. ./Desktop/brat_annotations

    folder_path_spacy = input('Please enter path where the spacy labelled brat files are in: ')

    # input4: enter folder path where we want to store file
    # e.g. ./Desktop/brat_extracted/extract_labels_csv

    csv_folder_path = input('Please enter folder path where we want to store file: ')

    # generating df for labels data for manual annotation files

    man_labelled_df = generate_annotation_csv(annotated_index,folder_path_man)

    man_labelled_df.to_csv(csv_folder_path+'/man_labelled_df.csv', header = True, index=False)

    # generating df for labels data for spacy annotation files

    spacy_labelled_df = generate_annotation_csv(annotated_index,folder_path_spacy)

    spacy_labelled_df.to_csv(csv_folder_path+'/spacy_labelled_df.csv', header = True, index=False)

