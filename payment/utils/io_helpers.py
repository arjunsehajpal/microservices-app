import json


def get_secret(path: str, key: str, sub_key: str = None):
    """_summary_

    Args:
        path (str): path of JSON file
        key (str): key of JSON
        sub_key (str, optional): key of the nested JSON (which is defined against `key`). Defaults to None.

    Returns:
        Union[str, dict]: returns the value against key (or key and sub-key combination)
    """
    try:
        with open(path) as F:
            dict_ = json.load(F)
            if sub_key:
                return dict_[key][sub_key]
            else:
                return dict_[key]
    except ValueError as E:
        raise (f"Unable to fetch secret due to following error:\n{E}")
