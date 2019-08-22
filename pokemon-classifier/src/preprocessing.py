# reads unprocessed, moves to train, creates csv of labels
import os
import shutil
import sys
import pandas as pd
import numpy as np

sys.path.append('/Users/tanya/PycharmProjects/Webscraping/pokemon-classifier')

# from data.test.scrape import poke_df

Unprocessed_path = '/Users/tanya/PycharmProjects/Webscraping/pokemon-classifier/data/unprocessed/'
train_path = '/Users/tanya/PycharmProjects/Webscraping/pokemon-classifier/data/train/'
test_path = '/Users/tanya/PycharmProjects/Webscraping/pokemon-classifier/data/test/'


def read_unprocessed(path):
    """
    Gives a list of the jpg files in the path directory.
    :param path: path of the directory to look into.
    :return: List of all the files.
    """
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if '.jpg' in file:
                files.append(os.path.join(r, file))
    return files


def move_files(files, move_path):
    """
    Moves all the files to the destination path.
    :param files: List of files to be moved.
    :param move_path: Destination path.
    :return: None, move files
    """
    for file in files:
        shutil.copy(file, move_path)


def import_df(fname):
    """

    :param fname:
    :return:
    """

    df = pd.read_csv(test_path + fname, index_col=0)
    return df


def get_poke_name(file_path):
    split_path = file_path.split('/')
    split_nametype = split_path[-1].split('_')
    split_subname = split_nametype[0]
    if '(' in split_subname:
        split_name = split_subname.split('(')
        poke_name = split_name[-2]
    else:
        poke_name = split_subname
    return poke_name


def labeled_csv(path, poke_df):
    """
    Creates a csv with file name and label as the pokemon id.
    :param path:
    :param poke_df:
    :return:
    """
    # selects all the files in train
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if '.jpg' in file:
                files.append(os.path.join(r, file))
    labels = []
    print("@@@@@")

    for file in files:
        poke_name = get_poke_name(file)

        rows_ = np.where(poke_df['Name'] == poke_name)
        print(rows_)
        for r in rows_:
            """
            if r == (array([], dtype=int64),):
                labels.append(None)
            else:"""
            labels.append(poke_df.iloc[r, 1].values[0])

    print(labels)

    poke_label_dict = {'File': files, 'Label': labels}
    labeled_df = pd.DataFrame(poke_label_dict)
    labeled_df.to_csv(train_path + 'poke_file_labels.csv')


if __name__ == "__main__":
    files_to_move = read_unprocessed(Unprocessed_path)
    move_files(files_to_move, train_path)
    poke_df = import_df('pokemondb.csv')
    """
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(poke_df)"""
    labeled_csv(train_path, poke_df)
