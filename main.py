from geopy.distance import geodesic
from datetime import timedelta
import gpxpy

from PIL import Image, ImageDraw, ImageFont
import moviepy.editor as mpy
import os

speeds = []

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
                speeds.append(round(speed, 1))
                #print(f"Speed at time {previous_point.time}: {speed} km/h")

            previous_point = point


print("First part done!")
speeds = speeds[80:100]

def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height


# Folder to store frames
frames_dir = 'frames'
os.makedirs(frames_dir, exist_ok=True)

# Image size
width, height = 640, 480

# Generate images with speeds
for i, speed in enumerate(speeds):
    # Create an image with RGBA (A for transparency)
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))  # Transparent background
    
    # Draw text on the image
    draw = ImageDraw.Draw(img)
    
    # Define font (You can replace 'arial.ttf' with a different font path if needed)
    try:
        font = ImageFont.truetype('arial.ttf', 50)
    except IOError:
        font = ImageFont.load_default()
    
    # Define text and its position
    text = f"Speed: {speed} m/s"
    text_width, text_height = textsize(text, font=font)
    position = ((width - text_width) // 2, (height - text_height) // 2)  # Centered
    
    # Draw the text
    draw.text(position, text, fill="white", font=font)
    
    # Save the image to frames folder
    img.save(os.path.join(frames_dir, f"frame_{i}.png"))

# Create a list of image file paths
image_files = [os.path.join(frames_dir, f"frame_{i}.png") for i in range(len(speeds))]

# Create a video from the images using moviepy
clips = [mpy.ImageClip(img).set_duration(1) for img in image_files]  # 1 second per frame

# Concatenate the clips into a video
video = mpy.concatenate_videoclips(clips, method="compose")

# Write the video to a file (with transparency support)
video.write_videofile("video_test_1.mp4", fps=1, codec="libx264", 
                      preset="slow", ffmpeg_params=["-pix_fmt", "yuva420p"])