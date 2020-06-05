import requests
import json
import csv
import io
from datetime import datetime as dt

def csv_to_json(csv_url, first_column, filename_prefix):
    r = requests.get(csv_url)
    string_content = r.content.decode('latin1')
    f = io.StringIO(string_content)
    reader = csv.DictReader(f, delimiter=";")
    _json = {}
    for row in reader:
        _json[row[first_column]] = [
            row["Nombre de cas confirmés"],
            row["Taux de cas pour 100 000 personnes"],
            row["Nombre de décès"]
        ]
    date = dt.now().strftime('%Y-%m-%dT%H:%M:%S')
    _path = f'data/quebec/{filename_prefix}{date}.json'
    with open(_path, 'w') as outfile:
        json.dump(_json, outfile)
    print(f"Wrote {_path:}")

montreal_ciuss_csv = "https://santemontreal.qc.ca/fileadmin/fichiers/Campagnes/coronavirus/situation-montreal/ciusss.csv"
csv_to_json(
    csv_url=montreal_ciuss_csv,
    first_column="CIUSSS",
    filename_prefix="montreal_ciuss"
)

montreal_nhood_csv = "https://santemontreal.qc.ca/fileadmin/fichiers/Campagnes/coronavirus/situation-montreal/municipal.csv"
csv_to_json(
    csv_url=montreal_nhood_csv,
    first_column="Arrondissement ou ville liée",
    filename_prefix="montreal_nhood"
)
