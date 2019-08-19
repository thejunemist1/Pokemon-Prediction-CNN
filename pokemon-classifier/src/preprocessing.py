# reads unprocessed, moves to train, creates csv of labels
import os
import shutil
import sys
import pandas as pd

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
    df = pd.read_csv(test_path + fname)
    df.drop(df.columns[0], axis=1)
    return df


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

    # check which pokemon
    labels = []
    poke_foldername = []
    for file in files:
        split_path = file.split('/')
        poke_foldername = split_path[-2]
        #for row in poke_df.iterrows():
        #for folder in poke_foldername:
        for index, row in poke_df.iterrows():
            if row['Name'] == poke_foldername:
                labels.append(row['id'])
            else:
                labels.append('Not Found')
            print("#")

        # labels.append(poke_df.loc[(poke_df['Name'] == poke_foldername), 'id'])
    print(labels)
    poke_label_dict = {'File': files, 'Label': labels}
    print(poke_label_dict)


if __name__ == "__main__":
    files_to_move = read_unprocessed(Unprocessed_path)
    move_files(files_to_move, train_path)
    poke_df = import_df('pokemondb.csv')
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(poke_df)
    labeled_csv(train_path, poke_df)
