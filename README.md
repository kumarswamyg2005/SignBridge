# SignBridge 🤝 - Speech to Sign Language Animator

Translate spoken words and text into visually engaging sign language animations using ASL and ISL.

## 🌟 Features

- 🎤 Real-time Speech-to-Text translation
- 🤟 Plays ASL/ISL sign language videos
- ✋ Fallback to fingerspelling for unknown words
- 🌓 Dark / Light Mode support
- 🚀 Fun Easter Eggs included!
- 📜 History tracking for previously signed sentences

## 💻 Tech Stack

- **Frontend:** HTML5, CSS3, JavaScript, Web Speech API
- **Backend:** Python, Flask, SpeechRecognition, OpenCV
- **Libraries:** pyttsx3, numpy, canvas-confetti

## 🛠️ Setup Instructions

1. **Install Dependencies:**
   It is recommended to use a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Generate Placeholder Videos:**
   This project requires videos. Run the setup script to generate automatic placeholder videos for testing purposes.

   ```bash
   python setup_dataset.py
   ```

3. **Start the Flask Server:**

   ```bash
   python app.py
   ```

4. **Open in Browser:**
   Navigate to [http://localhost:5000](http://localhost:5000)

## 📁 Dataset Download Instructions

For the real authentic experience, you should replace the placeholder videos with actual ASL/ISL videos.

- **WLASL Dataset:** https://github.com/dxli94/WLASL
- **MS-ASL Dataset:** https://www.microsoft.com/en-us/research/project/ms-asl
- **ISL Dataset:** https://www.kaggle.com/datasets/ahmedkhanak1995/sign-language-gesture-images-dataset

Name the files according to the word (e.g., `hello.mp4`) and place them in the corresponding `static/gestures/asl/` or `static/gestures/isl/` directories.

## 📂 Project Structure

```text
│
├── app.py                  ← Flask backend server
├── templates/
│   └── index.html          ← Main frontend UI (HTML/CSS/JS)
├── static/
│   └── gestures/           ← Video datasets
│       ├── asl/            ← ASL gesture videos
│       └── isl/            ← ISL gesture videos
├── dataset/
│   └── README.txt          ← Instructions to download dataset
├── requirements.txt        ← Python dependencies list
├── setup_dataset.py        ← Script to generate placeholder files
└── README.md               ← Full setup instructions (you are here)
```

## 👥 Credits

Developed for Multimedia Systems Project.

## 📄 License

MIT License
