# data from https://download.geofabrik.de/africa/niger.html
from osmread import parse_file, Node
highway_count = 0

%%time
a = []
for entity in parse_file('niger-latest.osm.pbf'):
    if isinstance(entity, Node) and 'place' in entity.tags:
        place = {'lon':entity.lon , 'lat':entity.lat , 'name':entity.tags['name']}
        a.append(entity)

import pandas as pd
u = pd.DataFrame.from_dict(a)

print("%d highways found" % highway_count)

u=a[0]
u.tags['name']
