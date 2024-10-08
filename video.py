from moviepy.editor import TextClip, VideoClip

def get_speed(t):
    return t % 10 + 10

def make_speed_counter(duration):
    def make_frame(t):
        speed = get_speed(t)
        txt = f"{speed:.1f} m/s"
        txt_clip = TextClip(txt, fontsize=50, color='white', bg_color=None)
        return txt_clip.get_frame(t)

    speed_clip = VideoClip(make_frame, duration=duration)
    speed_clip = speed_clip.set_fps(60)
    
    return speed_clip

duration = 60
speed_counter_video = make_speed_counter(duration)

speed_counter_video.write_videofile("speed_counter.mov", codec='png', fps=60, transparent=True)
