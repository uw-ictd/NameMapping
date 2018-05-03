# data from https://download.geofabrik.de/africa/niger.html
from osmread import parse_file, Node
import pandas as pd

highway_count = 0

places = []
for entity in parse_file('niger-latest.osm.pbf'):
    if isinstance(entity, Node) and 'name' in entity.tags:
        place = {'lon':entity.lon , 'lat':entity.lat , 'name':entity.tags['name']}
        places.append(place)

out_data_frame = pd.DataFrame(places)

out_data_frame.to_csv('osm_data.csv')
