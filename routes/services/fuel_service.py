#spotterapi/routes/services/fuel_service.py
import pandas as pd
from geopy.distance import geodesic
from django.conf import settings

class FuelService:
    @staticmethod
    def load_fuel_data():

        df = pd.read_csv(settings.CSV_FILE)
        df = df.dropna(subset=["Latitude", "Longitude", "Retail Price"])
        return df[["Truckstop Name", "Retail Price", "Latitude", "Longitude"]]

    @staticmethod
    def find_cheapest_stations(fuel_df, segment_points, radius):
        stops = []
        for i, seg in enumerate(segment_points):
            lat1, lon1 = seg
            nearby = fuel_df.copy()
            nearby["Distance"] = nearby.apply(
                lambda row: geodesic((row["Latitude"], row["Longitude"]), (lat1, lon1)).miles,
                axis=1
            )
            candidates = nearby[nearby["Distance"] <= radius]

            if not candidates.empty:
                cheapest = candidates.sort_values("Retail Price").iloc[0]
                stops.append({
                    "name": cheapest["Truckstop Name"],
                    "price": cheapest["Retail Price"],
                    "lat": cheapest["Latitude"],
                    "lon": cheapest["Longitude"]
                })
        return stops