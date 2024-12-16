# Importing libraries
import pandas as pd
import sankey as sk

DATA = "Contemporary Art Artists.json"


def decade_sankey(df, source, target):
    """"
    This function filters and aggregates a DataFrame based on the
    specified source and target columns, considering only rows with
    counts greater than or equal to 20. It then creates a Sankey diagram
    using the sk.make_sankey function and returns the filtered DataFrame."""

    df[target] = df[target].astype(str)
    dec = df.groupby([source, target]).size().reset_index(name='Count')
    dec_filtered = dec[dec['Count'] >= 20]
    dec = pd.concat([dec, dec_filtered])

    sk.make_sankey(dec_filtered, source, target)
    return dec_filtered


def main():
    df = pd.read_json(DATA)
    artist_data = pd.DataFrame(df, columns=["Nationality", "Gender", "BeginDate"])
    artist_data = artist_data.dropna()

    artist_data["Decade"] = (artist_data["BeginDate"] // 10) * 10
    artist_data = artist_data.dropna()

    # Task 5: Nationality and Decade

    nat_dec = decade_sankey(artist_data, 'Nationality', 'Decade')

    # Task 6: Nationality and Gender

    nat_gen = artist_data.groupby(['Nationality', 'Gender']).size().reset_index(name='Count')
    nat_gen = nat_gen[nat_gen['Count'] >= 20]
    sk.make_sankey(nat_gen, 'Nationality', 'Gender')

    # Task 7: Gender and Decade

    gen_dec = decade_sankey(artist_data, 'Gender', 'Decade')

    # Task 8: Multi-layered Sankey

    ng = nat_gen[['Nationality', 'Gender', 'Count']]
    ng.columns = ['src', 'targ', 'val']

    gd = gen_dec[['Gender', 'Decade', 'Count']]
    gd.columns = ['src', 'targ', 'val']

    stacked = pd.concat([ng, gd], axis=0)
    sk.make_sankey(stacked, 'src', 'targ', 'val')


if __name__ == "__main__":
    main()
