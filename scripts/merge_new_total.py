import json
import os

SUMMARY_LABEL_MAP = {
    'Negative1': 'negative',
    'Currently under investigation2': 'pending',
    'Currently under investigation3': 'pending',
    'Confirmed positive3': 'positive',
    'Confirmed positive4': 'positive',
    'Confirmed positive5': 'positive',
    'Resolved4': 'resolved',
    'Resolved5': 'resolved',
    'Deceased': 'deceased',
}

def get_date(file):
    date = file.split("_")[-1].split(".")[0]
    return date


def main():
    data_directory = "data/ontario/"
    files = os.listdir(data_directory)
    total_path = [ f for f in files if "total_ontario" in f][0]
    with open(data_directory+total_path, 'r') as outfile:
        total = json.load(outfile)

    date = get_date(total_path)

    new_total = {"date": date}
    for key, item in total.items():
        if key in SUMMARY_LABEL_MAP:
            new_total[SUMMARY_LABEL_MAP[key]] = int(item)
        else :
            new_total[key] = int(item)

            
    with open("data/ontario/all_updates.json", 'a') as outfile:
        json.dump(new_total, outfile)
        outfile.write('\n')

if __name__ == "__main__":
    main()