import sys
import pandas as pd

sys.path.append('/Users/tanya/PycharmProjects/Webscraping/pokemon-classifier')

from scrape import poke_dict

poke_df = pd.DataFrame.from_dict(poke_dict)
poke_df.insert(1, 'id', range(1, len(poke_df) + 1))
print(poke_df)

