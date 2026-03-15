import os
import cv2
import numpy as np

def create_placeholder_video(path, text, duration=3, fps=30, size=(450, 450)):
    """Creates a simple black video with white text in the center."""
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(path, fourcc, fps, size)
    
    for _ in range(duration * fps):
        frame = np.zeros((size[1], size[0], 3), dtype=np.uint8)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 3
        thickness = 5
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        
        text_x = (size[0] - text_size[0]) // 2
        text_y = (size[1] + text_size[1]) // 2
        
        cv2.putText(frame, text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)
        out.write(frame)
        
    out.release()

def main():
    print("===================================================================")
    print("VIDEO DATASET SETUP")
    print("===================================================================")
    print("\n[WLASL Dataset (World Level American Sign Language)]")
    print("URL: https://github.com/dxli94/WLASL")
    print("Instructions: Download WLASL_v0.3.zip, extract videos into /static/gestures/asl/ folder, rename each video file to the word it represents (e.g., hello.mp4, thanks.mp4)")
    print("\n[MS-ASL Dataset (Microsoft)]")
    print("URL: https://www.microsoft.com/en-us/research/project/ms-asl")
    print("Instructions: Request access and download. Organize into /static/gestures/asl/ folder.")
    print("\n[ISL (Indian Sign Language)]")
    print("URL: https://www.kaggle.com/datasets/ahmedkhanak1995/sign-language-gesture-images-dataset")
    print("Instructions: Download and place in /static/gestures/isl/ folder")
    print("\n[Fingerspelling (A-Z letters)]")
    print("URL: https://www.kaggle.com/datasets/grassknoted/asl-alphabet")
    print("Instructions: Download video clips for each letter, rename to a.mp4, b.mp4 ... z.mp4 and place in /static/gestures/asl/ folder")
    print("\n===================================================================")
    print("Creating Placeholder Videos...")
    
    base_dir = "static/gestures"
    asl_dir = os.path.join(base_dir, "asl")
    isl_dir = os.path.join(base_dir, "isl")
    
    os.makedirs(asl_dir, exist_ok=True)
    os.makedirs(isl_dir, exist_ok=True)
    
    words = ["hello", "my", "name", "is", "thank", "you", "good", "morning", "please", "sorry", "help", "yes", "no", "stop", "wait", "love", "friend", "family", "school", "home", "food", "water", "bathroom"]
    letters = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    
    all_items = words + letters
    
    print("Generating files (this may take a moment)...")
    for item in all_items:
        asl_path = os.path.join(asl_dir, f"{item}.mp4")
        if not os.path.exists(asl_path):
            create_placeholder_video(asl_path, item.upper())
            
        isl_path = os.path.join(isl_dir, f"{item}.mp4")
        if not os.path.exists(isl_path):
            create_placeholder_video(isl_path, item.upper())
            
    print("\nREQUIREMENTS CHECKLIST:")
    print(f"{'✅' if os.path.exists(asl_dir) else '❌'} static/gestures/asl folder exists")
    print(f"{'✅' if os.path.exists(isl_dir) else '❌'} static/gestures/isl folder exists")
    print("✅ Placeholder videos created for: a-z, and common words.")
    print("Setup Complete! You can now start the app.")

if __name__ == '__main__':
    main()