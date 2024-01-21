import json
import os
import pandas as pd


COUNTY_NAMES: dict[str, str] = {
    'bacs_kiskun': 'Bács-Kiskun megye',
    'baranya': 'Baranya megye',
    'bekes': 'Békés megye',
    'borsod_abauj_zemplen': 'Borsod-Abaúj-Zemplén megye',
    'budapest': 'Budapest megye',
    'csongrad_csanad': 'Csongrád-Csanád megye',
    'fejer': 'Fejér megye',
    'gyor_moson_sopron': 'Győr-Moson-Sopron megye',
    'hajdu_bihar': 'Hajdú-Bihar megye',
    'heves': 'Heves megye',
    'jasz_nagykun_szolnok': 'Jász-Nagykun-Szolnok megye',
    'komarom_esztergom': 'Komárom-Esztergom megye',
    'nograd': 'Nógrád megye',
    'pest': 'Pest megye',
    'somogy': 'Somogy megye',
    'szabolcs_szatmar_bereg': 'Szabolcs-Szatmár-Bereg megye',
    'tolna': 'Tolna megye',
    'vas': 'Vas megye',
    'veszprem': 'Veszprém megye',
    'zala': 'Zala megye',
}


def collect_counties() -> None:

    base_url: str = os.path.join(os.getcwd(), '../assets/religion')

    counties: list[dict[str, any]] = []

    list_of_filenames: list[str] = os.listdir(base_url)

    for index, filename in enumerate(list_of_filenames):
        county_name: str = filename.replace('.csv', '')

        county = {
            'id': index + 1,
            'name': COUNTY_NAMES[county_name],
            'ids': [],
        }

        df = pd.read_csv(
            os.path.join(base_url, filename),
            delimiter=';',
            usecols=['TERUL_GEO5'],
            dtype={
                'TERUL_GEO5': 'string',
            },
        )

        county['ids'].extend(pd.unique(df['TERUL_GEO5']))

        counties.append(county)

    with open(os.path.join(os.getcwd(), '../out/counties.json'), 'w', encoding='utf-8') as file:
        json.dump(counties, file, indent=4, ensure_ascii=False)


def get_counties() -> list[dict[str, any]]:
    with open(os.path.join(os.getcwd(), '../out/counties.json'), 'r', encoding='utf-8') as file:
        return json.load(file)
