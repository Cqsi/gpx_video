import gpxpy

with open('data\\activity_1.gpx', 'r') as gpx_file:
    gpx = gpxpy.parse(gpx_file)

# Extract data points with timestamp, latitude, longitude, and elevation
# for track in gpx.tracks:
#     for segment in track.segments:
#         for point in segment.points:
#             print(f"Time: {point.time}, Latitude: {point.latitude}, Longitude: {point.longitude}")

