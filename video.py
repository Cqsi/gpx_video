from PIL import Image, ImageDraw, ImageFont
import moviepy.editor as mpy
import os

def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height

# List of speeds (one for each second)
speeds = [10, 20, 15, 18, 25, 30, 35, 40]  # Example speeds

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
video.write_videofile("speed_video_with_transparency.mp4", fps=1, codec="libx264", 
                      preset="slow", ffmpeg_params=["-pix_fmt", "yuva420p"])

# Cleanup: Optionally remove the frames if you don't need them anymore
# import shutil
# shutil.rmtree(frames_dir)
