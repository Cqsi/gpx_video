from geopy.distance import geodesic
from datetime import timedelta
import gpxpy


with open('data\\activity_1.gpx', 'r') as gpx_file:
    gpx = gpxpy.parse(gpx_file)

def calculate_speed(point1, point2):
    coord1 = (point1.latitude, point1.longitude)
    coord2 = (point2.latitude, point2.longitude)
    distance = geodesic(coord1, coord2).meters  # Distance in meters
    time_diff = (point2.time - point1.time).total_seconds()  # Time difference in seconds
    
    if time_diff > 0:
        return distance / time_diff  # Speed in m/s
    
    return 0

# Example usage
previous_point = None
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            if previous_point:
                speed = calculate_speed(previous_point, point)

                print(f"Speed at time {previous_point.time}: {speed} km/h")
            previous_point = point


