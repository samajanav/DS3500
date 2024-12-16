# Importing libraries
import plotly.graph_objects as go


def _code_mapping(df, src, targ):
    """This function generates integer codes for distinct labels in
    the specified source and target columns of a
    DataFrame, creating a label-to-code mapping and
    substituting names with codes in the DataFrame."""

    # get distinct labels
    labels = sorted(set(list(df[src]) + list(df[targ])))

    # get integer codes
    codes = list(range(len(labels)))

    # create label to code mapping
    lc_map = dict(zip(labels, codes))

    # substitute names for codes in the dataframe
    df = df.replace({src: lc_map, targ: lc_map})

    return df, labels


def make_sankey(df, src, targ, vals=None, **kwargs):
    """
    A function to make a sankey diagram.
    """

    if vals:
        values = df[vals]
    else:
        values = [1] * len(df)  # all 1's

    df, labels = _code_mapping(df, src, targ)

    width = kwargs.get('width', 2)
    link = {'source': df[src], 'target': df[targ], 'value': values,
            'line': {'width': width}}

    node = {'label': labels, 'pad': 50, 'thickness': 25,
            'line': {'color': 'black', 'width': 2}}

    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)
    fig.show()
