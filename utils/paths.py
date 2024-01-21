from os import listdir
from os.path import exists

RELIGION_DATA_FOLDER_NAME: str = 'religion'

EDUCATIONAL_ATTAINMENT_FOLDER_NAME: str = 'educational_attainment'


def get_list_of_counties(assets_path: str) -> list[str]:

    """
    This function returns with hte list of the available counties.
    :param assets_path: The path to the assets' folder.
    :return: An array of strings, specifically the county names.
    """

    # creating a set for the file names
    unique_files: set[str] = set()

    # reading all the available files from educational_attainment folder
    files: list[str] = listdir(f'{assets_path}/educational_attainment')

    # add only those file names into the unique files set, which is not in the set
    [unique_files.add(file) if file not in unique_files else None for file in files]

    # reading all the available files from religion folder
    files: list[str] = listdir(f'{assets_path}/religion')

    # add only those file names into the unique files set, which is not in the set
    [unique_files.add(file) if file not in unique_files else None for file in files]

    # we return with the file names without the .csv extension
    return [file.replace('.csv', '') for file in files]


def get_religion_data_path(assets_path: str, county: str) -> (bool, str):

    """
    This function returns with the path to the given county's religion data.
    :param assets_path: The path to the assets' folder.
    :param county: The name of the country in the following format: 'gyor_moson_sopron'
    :return: Tuple[bool, str], which holds a boolean value as the first parameter,
     it tells you if the file exists for the given county's religion data, and the second
     parameter is the path to the asset.
    """

    path: str = f'{assets_path}/{RELIGION_DATA_FOLDER_NAME}/{county}.csv'

    return (True, path) if exists(path) else (False, '')


def get_educational_attainment_data_path(assets_path: str, county: str) -> (bool, str):

    """
    This function returns with the path to the given county's educational attainment data.
    :param assets_path: The path to the assets' folder.
    :param county: The name of the country in the following format: 'gyor_moson_sopron'
    :return: Tuple[bool, str], which holds a boolean value as the first parameter,
     it tells you if the file exists for the given county's educational attainment data,
     and the second parameter is the path to the asset.
    """

    path: str = f'{assets_path}/{EDUCATIONAL_ATTAINMENT_FOLDER_NAME}/{county}.csv'

    return (True, path) if exists(path) else (False, '')
