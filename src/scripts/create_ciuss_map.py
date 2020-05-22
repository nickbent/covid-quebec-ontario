from shapely.geometry import Polygon, mapping
from shapely.ops import cascaded_union
import json


CIUSS = {
    "CIUSSS du Centre-Ouest-de-l'Île-de-Montréal ": ['Westmount','Côte-Saint-Luc','Côte-des-Neiges-Notre-Dame-de-Grâce', 
                                                     'Montréal-Ouest', 'Hampstead', 'Outremont', ],
    "CIUSSS du Centre-Sud-de-l'Île-de-Montréal" : ['Verdun','Le Sud-Ouest', 'Ville-Marie', 'Le Plateau-Mont-Royal' ],
    "CIUSSS de l'Est-de-l'Île-de-Montréal" : ['Rosemont-La Petite-Patrie', 'Saint-Léonard','Mercier-Hochelaga-Maisonneuve',
                                             'Anjou', 'Montréal-Est', 'Rivière-des-Prairies-Pointe-aux-Trembles'],
    "CIUSSS du Nord-de-l'Île-de-Montréal" : ['Mont-Royal', 'Saint-Laurent', 'Ahuntsic-Cartierville', 
                                             'Villeray-Saint-Michel-Parc-Extension', 'Montréal-Nord'],
    "CIUSSS de l'Ouest-de-l'Île-de-Montréal" : ["L'Île-Bizard-Sainte-Geneviève", 'Pierrefonds-Roxboro', 'Senneville', 
                                                     'Sainte-Anne-de-Bellevue', "Baie-d'Urfé", 'Kirkland', 'Beaconsfield', 
                                                     'Pointe-Claire', 'Dorval','LaSalle','Lachine', 'Dollard-des-Ormeaux',
                                               "L'Île-Dorval"]
    
    
}

nhood_map = {
    'Côte-des-Neiges–Notre-Dame-de-Grâce' : 'Côte-des-Neiges-Notre-Dame-de-Grâce',
    'Plateau-Mont-Royal' : 'Le Plateau-Mont-Royal',
    "Baie-D'Urfé" : "Baie-d'Urfé",
    'Mercier–Hochelaga-Maisonneuve' : 'Mercier-Hochelaga-Maisonneuve',
    'Côte-Saint-Luc' : 'Côte-Saint-Luc',
    'Kirkland' : 'Kirkland',
    "L'Île-Bizard–Sainte-Geneviève" :"L'Île-Bizard-Sainte-Geneviève",
    'Pierrefonds–Roxboro' :'Pierrefonds-Roxboro',
    'Rivière-des-Prairies–Pointe-aux-Trembles' : 'Rivière-des-Prairies-Pointe-aux-Trembles',
    'Rosemont–La Petite Patrie' : 'Rosemont-La Petite-Patrie',
    'Saint-Léonard' : 'Saint-Léonard',
    'Senneville' : 'Senneville',
    'Ahuntsic–Cartierville' :'Ahuntsic-Cartierville',
    'Sud-Ouest' : 'Le Sud-Ouest',
    'Villeray–Saint-Michel–Parc-Extension' :'Villeray-Saint-Michel-Parc-Extension' 
    
}

def main():

    with open("../data/quebec/montreal.geojson","r") as infile:
        montreal_nhood = json.load(infile)
    nhood_list =  [f["properties"]["NOM"] for f in montreal_nhood["features"]]
    nhood_polygons = {f["properties"]["NOM"]:f["geometry"]["coordinates"] for f in montreal_nhood["features"]}

    ciuss_map = {'name': 'LIMADMIN',
    'type': 'FeatureCollection',
    'features': []
                }

    features = []
    for c, areas in CIUSS.items():
        temp = []
        for area in areas :
            temp.append(Polygon(nhood_polygons[area][0][0]))
        new_geometry = mapping(cascaded_union(temp))
        new_feature = dict(type='Feature', properties={"NOM" : c},geometry=dict(type=new_geometry['type'], coordinates=new_geometry['coordinates']))

        features.append(new_feature)
        
    ciuss_map['features'] = features

    with open("../data/quebec/montreal_ciuss.geojson","w") as outfile:
        json.dump(ciuss_map, outfile)

if __name__ == "__main__":
    main()

