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

def map_keys(ontario):
    d = {}
    for key, value in ontario.items():
        if 'Number of cases' in key:
            d['total'] = int(value.replace(",","").replace("*",""))
        elif 'Change from previous report' in key :
            pass
        elif 'Resolved' in key : 
            d['resolved'] = int(value.replace(",","").replace("*",""))
        elif 'Deceased' in key:
            d['deceased'] = int(value.replace(",","").replace("*",""))
        elif 'Total Tested' in key : 
            d["total tested"] = int(value.replace(",","").replace("*",""))
        elif 'Currently Under Investigation' in key : 
            d['pending'] = int(value.replace(",","").replace("*",""))
            
        elif ' ' == key : 
            pass
        elif 'hospitalized' in key :
            d['hospitalizations'] = int(value.replace(",","").replace("*",""))
        elif 'ventilator' in key : 
            d["ventilator"] = int(value.replace(",","").replace("*",""))
        elif "ICU" in key : 
            d["ICU"] = int(value.replace(",","").replace("*",""))
        else :
            d[key] = int(value.replace(",","").replace("*",""))

            
    return d

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

    new_total = map_keys(total)
    new_total["date"] = date
    new_total["positive"] = new_total["total"] - new_total["resolved"] - new_total["deceased"]        
    with open("data/ontario/updates.jsonl", 'a') as outfile:
        json.dump(new_total, outfile)
        outfile.write('\n')

if __name__ == "__main__":
    main()