import json
import os
import shutil

with open('archive/WLASL_v0.3.json', 'r') as f:
    data = json.load(f)

asl_dir = 'static/gestures/asl'
os.makedirs(asl_dir, exist_ok=True)

copied = 0
for entry in data:
    word = entry['gloss'].lower()
    # Find the first available video file for this word
    for instance in entry['instances']:
        video_id = instance['video_id']
        src_path = os.path.join('archive', 'videos', f'{video_id}.mp4')
        if os.path.exists(src_path):
            dst_path = os.path.join(asl_dir, f'{word}.mp4')
            shutil.copy(src_path, dst_path)
            copied += 1
            break # only need one video per word

print(f'Successfully copied {copied} word videos to the asl folder.')
