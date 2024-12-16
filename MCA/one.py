import json
import plotly.graph_objects as go
from matplotlib.sankey import Sankey
import matplotlib.pyplot as plt
import pandas as pd
import sankey as sk

DATA = "Contemporary Art Artists.json"

def decade_sankey(source,target):

def main():

    df = pd.read_json(DATA)
    artist_data = pd.DataFrame(df, columns=["Nationality","Gender","BeginDate"])
    artist_data = artist_data.dropna()

    artist_data["Decade"] = ((artist_data["BeginDate"].astype(int) // 10) % 10) * 10
    artist_data.dropna()

    # Task 5: Nationality and Decade

    artist_data['Decade'] = artist_data['Decade'].astype(str)

    nat_dec = artist_data.groupby(['Nationality', 'Decade']).size().reset_index(name='Count')

    nat_dec_filtered = nat_dec[nat_dec['Count'] >= 20]

    nat_dec = pd.concat([nat_dec, nat_dec_filtered])

    # sk.make_sankey(nat_dec, 'Nationality', 'Decade')

    # Task 6: Nationality and Gender

    nat_gen = artist_data.groupby(['Nationality', 'Gender']).size().reset_index(name='Count')

    nat_gen = nat_gen[nat_gen['Count'] >= 20]

    # # sk.make_sankey(nat_gen, 'Nationality', 'Gender')
    #
    # # Task 8: Gender and Decade
    #
    # artist_data['Decade'] = artist_data['Decade'].astype(str)
    # gen_dec = artist_data.groupby(['Gender', 'Decade']).size().reset_index(name='Count')
    #
    # gen_dec_filtered = gen_dec[gen_dec['Count'] >= 20]
    #
    # gen_dec = pd.concat([gen_dec, gen_dec_filtered], ignore_index=True)
    #
    # sk.make_sankey(gen_dec_filtered, 'Gender', 'Decade')
    #
    # ng = nat_gen[['Nationality', 'Gender','Count']]
    # ng.columns = ['src', 'targ','val']
    #
    # gd = gen_dec_filtered[['Gender', 'Decade','Count']]
    # gd.columns = ['src', 'targ','val']
    #
    # stacked = pd.concat([ng, gd], axis=0)
    # print(stacked)
    #
    # # sk.make_sankey(stacked,'src','targ','val',label_color = ['blue'])

if __name__ == "__main__":
    main()
