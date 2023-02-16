import pandas as pd


def is_pandas_pytable(group):
    if 'axis0' in group.keys() and 'axis1' in group.keys():
        return True
    else:
        return False


def is_doi(string: str):
    if string.startswith('10.') or string.startswith('https://doi.org/'):
        return True
    else:
        return False


def _read_json(path_to_file, lines=False):
    """Read JSON file

    Arguments:
        path_to_file (string): Path to JSON file

    Returns: (dict) JSON file contents
    """
    df = pd.read_json(path_to_file, lines=lines)
    return df


def _read_csv(path_to_file):
    """Read CSV file

    Arguments:
        path_to_file (string): Path to CSV file

    Returns: (dict) CSV file contents
    """
    return pd.read_csv(path_to_file)


def _read_excel(path_to_file):
    return pd.read_excel(path_to_file)
