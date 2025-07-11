import folium
from folium.plugins import MarkerCluster
from geopy.distance import geodesic

def create_route_map(route_coords, stops=None, start=None, end=None):
 
    m = folium.Map(location=route_coords[0], zoom_start=6)
    
    folium.PolyLine(
        locations=route_coords,
        color='blue',
        weight=5,
        opacity=0.7
    ).add_to(m)
   
    if start:
        folium.Marker(
            location=start,
            icon=folium.Icon(color='green', icon='play', prefix='fa'),
            tooltip="Start"
        ).add_to(m)
    
    if end:
        folium.Marker(
            location=end,
            icon=folium.Icon(color='red', icon='stop', prefix='fa'),
            tooltip="End"
        ).add_to(m)
    
    if stops:
        marker_cluster = MarkerCluster().add_to(m)
        
        for stop in stops:
            folium.Marker(
                location=[stop['lat'], stop['lon']],
                popup=f"⛽ {stop['name']}<br>${stop['price']}/gal",
                icon=folium.Icon(color='orange', icon='gas-pump', prefix='fa')
            ).add_to(marker_cluster)
    
    return m