import folium
import pandas
import json


def create_map():
    location = [0, 0]
    map = folium.Map(location=location, zoom_start=2)
    return map


def create_volcano_fg(map):
    # Get and store data from csv
    volcano_data = pandas.read_csv('usa-volcanoes.csv')
    names = volcano_data['NAME']
    locations = volcano_data['LOCATION']
    lats = volcano_data['LAT']
    longs = volcano_data['LON']
    statuses = volcano_data['STATUS']
    elevations = volcano_data['ELEV']

    # Add volcanoes features
    volcano_fg = folium.FeatureGroup(name='Volcanoes in the US')
    for name, location, lat, long, status, elevation in zip(names, locations, lats, longs, statuses, elevations):
        popup_string = str(name) + ', ' + str(location) + ' [' + str(elevation) + 'm]'
        volcano_fg.add_child(
            folium.Marker(location=(lat, long), popup=popup_string, icon=folium.Icon(color='red')))
    map.add_child(volcano_fg)


def create_geo_population_fg(map):
    # Get and store data from geo-json
    with open('world.json') as file:
        data = json.load(file)

    # Add geoJson features
    geo_fg = folium.FeatureGroup(name='Geo Population Data')
    geo_fg.add_child(folium.GeoJson(data=data, style_function=lambda x: {
        'fillColor':
            'green' if x['properties']['POP2005'] < 1000000
            else 'yellow' if x['properties']['POP2005'] < 50000000
            else 'red'}))
    map.add_child(geo_fg)


if __name__ == '__main__':
    # Create a map
    map = create_map()
    # Display volcanoes in USA
    create_volcano_fg(map)
    # Shade countries with population categories
    create_geo_population_fg(map)
    # Adding layer control
    map.add_child(folium.LayerControl())
    map.save('map.html')
