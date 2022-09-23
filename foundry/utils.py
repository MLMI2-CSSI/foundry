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
