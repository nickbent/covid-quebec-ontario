import json
import os

def get_date(file):
    date = file.split("_")[-1].split(".")[0]
    return date

def get_city_from_public_health_unit(public_health_unit):
    # http://www.health.gov.on.ca/en/common/system/services/phu/locations.aspx
    if 'Ajax' in public_health_unit:
        return 'Ajax'
    if 'Algoma' in public_health_unit:
        return 'Sault Ste. Marie'
    if 'Brant' in public_health_unit:
        return 'Brantford'
    if 'Chatham' in public_health_unit:
        return 'Chatham'
    if 'Durham' in public_health_unit:
        return 'Whitby'
    if 'Eastern Ontario' in public_health_unit:
        return 'Cornwall'
    if 'Grand River Hospital' in public_health_unit:
        return 'Kitchener'
    if 'Grey Bruce' in public_health_unit:
        return 'Owen Sound'
    if 'Haliburton' in public_health_unit:
        return 'Port Hope'
    if 'Halton' in public_health_unit:
        return 'Oakville'
    if 'Hamilton' in public_health_unit:
        return 'Hamilton'
    if 'Hastings' in public_health_unit:
        return 'Belleville'
    if 'Huron Perth' in public_health_unit:
        return 'Stratford'
    if 'Kingston' in public_health_unit:
        return 'Kingston'
    if 'London' in public_health_unit:
        return 'London'
    if 'Mackezie' in public_health_unit:
        return 'Richmond Hill'
    if 'Mississauga' in public_health_unit:
        return 'Mississauga'
    if 'Mount Sinai' in public_health_unit:
        return 'Toronto'
    if 'Niagara' in public_health_unit:
        return 'Niagara'
    if 'Northwestern' in public_health_unit:
        return 'Kenora'
    if 'North York' in public_health_unit:
        return 'Toronto'
    if 'Ottawa' in public_health_unit:
        return 'Ottawa'
    if 'Peel' in public_health_unit:
        return 'Peel'
    if 'Peterborough' in public_health_unit:
        return 'Peterborough'
    if 'Porcupine' in public_health_unit:
        return 'Timmins'
    if 'Simcoe' in public_health_unit:
        return 'Simcoe'
    if 'Scarborough' in public_health_unit:
        return 'Scarborough'
    if 'Southlake' in public_health_unit:
        return 'Newmarket'
    if 'Sudbury' in public_health_unit:
        return 'Sudbury'
    if 'Sunnybrook' in public_health_unit:
        return 'Toronto'
    if 'Toronto' in public_health_unit:
        return 'Toronto'
    if 'Waterloo' in public_health_unit:
        return 'Waterloo'
    if 'Wellington Dufferin Guelph' in public_health_unit:
        return 'Guelph'
    if 'Windsor' in public_health_unit:
        return 'Windsor'
    if 'York' in public_health_unit:
        return 'York'
    return public_health_unit


def main():
    data_directory = "data/ontario/"
    files = os.listdir(data_directory)
    table_path = [ f for f in files if "table" in f][0]

    date = get_date(table_path)

    with open(data_directory+table_path, 'r') as outfile:
        table = [json.loads(l) for l in outfile]

    #update the table to required specifications
    updated_table = []
    for x in table:
        person = x['patient']
        if len(person.split(" ")) ==2 :
            try : 
                age = int(person.split(" ")[0][:-1])
            except ValueError:
                age = age
            gender = person.split(" ")[1]
        elif len(person.split(" ")) ==3: 
            age = 10
            gender = person.split(" ")[-1]
        else:
            age = 'pending'
            gender = 'pending'
        place = x['public health unit']
        transmission = x['transmission']
        status = x['status']
        city = get_city_from_public_health_unit(place)
        new = { "number" : x["case number"],
                "date" : date,
                "age" : age, 
                'gender' : gender, 
                'public_health_unit' : place,
                'transmission' : transmission,
                'city' : city,
                'status' : status
                                    }
        updated_table.append(new)

#merge with existing table

    path = "data/ontario/cases.jsonl"
    all_cases = {}
    with open(path, 'r') as outfile:
        for c in outfile:
            case = json.loads(c)
            all_cases[case["number"]] = case
        
    for case in updated_table : 
        if case["number"] not in all_cases:
            all_cases[case["number"]]  = case
        else :
            current = all_cases[case["number"]]
            for key, item in case.items():
                if key == 'number':
                    continue
                if key in current : 
                    if current[key] == 'pending' and item != 'pending':
                        current[key] = item
                else : 
                    current[key] = item
                    
    # saving

    with open(path, 'w') as outfile:
        for key, case in all_cases.items():
            json.dump(case, outfile)
            outfile.write('\n')


if __name__ == "__main__":
    main()