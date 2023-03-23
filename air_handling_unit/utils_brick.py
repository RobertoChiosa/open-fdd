import pandas as pd
from IPython import get_ipython
from rdflib import URIRef, Variable

try:
    from IPython.display import display, Markdown
except:
    pass


# Helper functions
def is_notebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True  # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False  # Probably standard Python interpreter


def print_graph(g):
    g_str = g.serialize(format='turtle')
    new_g_str = ''
    for line in g_str.split('\n'):
        if 'prefix' not in line:
            new_g_str += line + '\n'
    if is_notebook():
        display(Markdown('```turtle\n' + new_g_str + '\n```'))
    else:
        print(g_str)


def operational_mode(df):
    df['Occupied'] = False
    # define mode depending on index
    df.loc[(df.index.dayofweek < 5) & (df.index.hour >= 6) & (df.index.hour < 22), 'Occupied'] = True
    df.loc[(df.index.dayofweek == 5) & (df.index.hour >= 6) & (df.index.hour < 18), 'Occupied'] = True
    return df


def parse_results(results, explicit=True, fullURI=False, df=True, noPrefix=False):
    m = {
        'https://brickschema.org/schema/Brick': 'brick',
        'http://www.w3.org/1999/02/22-rdf-syntax-ns': 'rdf',
        'http://www.w3.org/2000/01/rdf-schema': 'rdfs',
        'https://brickschema.org/schema/1.0.1/BrickFrame': 'bf',
        'http://www.w3.org/2002/07/owl': 'owl',
        'http://www.w3.org/2004/02/skos/core': 'skos',
        'http://bldg-59': 'bldg',
    }

    # alternative for
    # for row in res:
    # print(row)
    # if explicit:
    #     y = [[str(term.split('//')[1]) for term in row] for row in res]
    # else:
    #     y = [[str(term.split('#')[1]) for term in row] for row in res]
    # y = list([str(row[0]).split('#')[1] for row in results])
    # return y

    if not fullURI:
        rows = [
            [m[r.split('#')[0]] + ':' + r.split('#')[1] if isinstance(r, URIRef) and '#' in r else r for r in
             row] for row in results]

        if noPrefix is True:
            # split prefix from name in list comprehension
            out = [[item.split(':')[1] if isinstance(item, str) and ':' in item else item for item in row] for row in
                   rows]

        else:
            out = rows

    else:
        out = list(results)

    if df:
        out = pd.DataFrame.from_records(
            data=out, columns=[str(item) for item in results.vars if isinstance(item, Variable)])

    return out
