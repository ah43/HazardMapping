import folium.vector_layers
from folium.vector_layers import Circle, PolyLine
import geopandas as gpd
from shapely.geometry import Polygon, Point
from shapely.ops import nearest_points
from math import radians, cos
from geopy.distance import great_circle

def create_germany_map(lat, lng, name):
    # (Put the entire create_germany_map function here, unchanged)
    def create_germany_map(lat, lng, name):
        germany_lat, germany_lng = 51.1657, 10.4515
        m = folium.Map(location=[germany_lat, germany_lng], zoom_start=6)

        # Add a marker to the map
        marker = folium.Marker([lat, lng], popup=name).add_to(m)

        # Load the GeoJSON data and filter by bounds
        search_radius = 100  # km
        lat_range = search_radius / 111.2  # Approximate 1 degree of latitude as 111.2 km
        lng_range = search_radius / abs(
            111.2 * cos(radians(lat)))  # Approximate 1 degree of longitude at the given latitude
        bounds = Polygon([(lng - lng_range, lat - lat_range), (lng + lng_range, lat - lat_range),
                          (lng + lng_range, lat + lat_range), (lng - lng_range, lat + lat_range)])
        geojson_file = "/home/ah/Desktop/map/simple.geojson"
        gdf = gpd.read_file(geojson_file)
        gdf = gdf[gdf.geometry.intersects(bounds)]
        circle = Circle(location=[lat, lng], radius=30000, color='blue', fill=True, fill_opacity=0.2)
        circle.add_to(m)

        # Find the closest point in the filtered layer
        origin = Point(lng, lat)
        gdf['geometry'] = gdf['geometry'].buffer(0)  # Clean the geometries
        nearest_geom = gdf.geometry.unary_union
        nearest_point = nearest_points(origin, nearest_geom)[1]

        # Add a marker for the closest point
        closest_marker = folium.Marker([nearest_point.y, nearest_point.x], popup="Closest Point",
                                       icon=folium.Icon(color='red')).add_to(m)

        # Draw a dotted line between the initial and the calculated marker
        line = PolyLine([(lat, lng), (nearest_point.y, nearest_point.x)],
                        color='black',
                        dash_array='5, 5',
                        weight=2).add_to(m)

        from geopy.distance import great_circle

        # Calculate the distance between the initial and the calculated marker
        distance = great_circle((lat, lng), (nearest_point.y, nearest_point.x)).km

        # Add the distance as a popup to the line
        line.add_child(folium.Popup(f'Distance: {distance:.2f} km'))

        # Add the filtered GeoJSON layer to the map as a vector layer
        folium.GeoJson(
            gdf,
            name="Flood Risk Zones",
            style_function=lambda feature: {
                'fillColor': 'red',
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.4,
            },
            overlay=True,
            control=False,
        ).add_to(m)

        m.save('germany_map_with_marker_and_filtered_geojson.html')