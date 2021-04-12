import pgeocode
import folium
from folium.plugins import MarkerCluster
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time

def make_map(df, filename):
    # folium.Map(location=[45.5236, -122.6750],
    #        tiles='Mapbox',
    #        API_key='your.API.key')


    map = folium.Map(
        location=[49.2767, -123.1300],
        tiles='cartodbpositron',
        zoom_start=12,
    )

    # folium.CircleMarker(
    #     location=[45.5215, -122.6261],
    #     radius=50,
    #     popup="Laurelhurst Park",
    #     color="#3186cc",
    #     fill=True,
    #     fill_color="#3186cc",
    # ).add_to(m)

    df.apply(lambda row:folium.CircleMarker(location=[row["latitude"], row["longitude"]]).add_to(map), axis=1)

    # mapper = lambda row : folium.CircleMarker(location=[row["latitude"], row["longitude"]], radius=50).add_to(map)
    # df.apply(mapper, axis=1)
    
    map.save(filename)

def make_mapbox(df, filename):
    map = folium.Map(
        location=[49.2767, -123.1300],
        zoom_start=12,
        tiles="https://api.mapbox.com/styles/v1/drjasonharrison/ckmz9fzye2jjs17o5xmm72yim/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZHJqYXNvbmhhcnJpc29uIiwiYSI6ImNrbXo5MG5vYzBiajIydm1sM283bWZjaHcifQ.tE6uoUPprLmH76y6cFHp9Q",
        attr="Copyright MapBox 2021")

    for row in df.iterrows():
        lat = row[1]["latitude"]
        long = row[1]["longitude"]
        folium.CircleMarker(location=[lat, long]).add_to(map)
        time.sleep(0.001)
    map.save(filename)

def make_mapbox_clustered(df, filename):
    map = folium.Map(
        location=[49.2767, -123.1300],
        zoom_start=12,
        tiles="https://api.mapbox.com/styles/v1/drjasonharrison/ckmz9fzye2jjs17o5xmm72yim/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZHJqYXNvbmhhcnJpc29uIiwiYSI6ImNrbXo5MG5vYzBiajIydm1sM283bWZjaHcifQ.tE6uoUPprLmH76y6cFHp9Q",
        attr="Copyright MapBox 2021")

    marker_cluster = MarkerCluster().add_to(map)

    for row in df.iterrows():
        lat = row[1]["latitude"]
        long = row[1]["longitude"]
        folium.CircleMarker(location=[lat, long]).add_to(marker_cluster)
        time.sleep(0.001)
    map.save(filename)


def make_map_clustered(df, filename):
    map = folium.Map(
        location=[49.2767, -123.1300],
        tiles='cartodbpositron',
        zoom_start=12,
    )

    marker_cluster = MarkerCluster().add_to(map)
    df.apply(lambda row:folium.Marker(location=[row["latitude"], row["longitude"]]).add_to(marker_cluster), axis=1)
    map.save(filename)



def main():
    codes = []  # ["V6Z 3C7", "T2P 2J5"]
    count = 0
    with open("postal_codes_clean.txt", "r") as fp:
        for line in fp:
            count += 1
            codes.append(line.strip())
    
    nomi = pgeocode.Nominatim('ca')
    df = nomi.query_postal_code(codes)

    make_mapbox_clustered(df, "cannabis-mapbox-clustered.html")
    make_mapbox(df, "cannabis-mapbox.html")
    make_map(df, "cannabis.html")

    make_map_clustered(df, "cannabis-clustered.html")


#if __name__ == main:
main()