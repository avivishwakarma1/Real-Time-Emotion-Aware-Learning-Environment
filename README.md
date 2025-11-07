# Real-Time Emotion Aware Learning Environment

> An AI-powered system that detects and analyzes students' facial emotions in real-time to enhance engagement and personalize learning experiences.

## 🎓 Project Overview

This project focuses on creating a **Real-Time Emotion Aware Learning Environment** that uses computer vision and deep learning to detect students’ facial expressions and interpret their emotional states during learning sessions. By identifying emotions such as happiness, surprise, sadness, or confusion, the system provides insights to educators or adaptive learning systems for improving student engagement and learning outcomes.

## 📌 Features

- 🎥 Real-time facial emotion detection using webcam
- 🧠 Deep Learning model trained for emotion classification
- 📊 Visualization of emotion trends and engagement levels
- 🔁 Continuous feedback loop for adaptive learning systems
- 💻 User-friendly interface for monitoring and reporting

## 🗂 Project Structure

```
├── emotion_detection.ipynb         # Jupyter Notebook (model training & evaluation)
├── emotion_dashboard.py            # Streamlit-based dashboard application
├── haarcascade_frontalface.xml     # Face detection classifier
├── emotion_model.h5                # Trained emotion recognition model
├── sample_images/                  # Example images for testing
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```

## ⚙️ Installation & Setup

1. Clone the repository

```bash
git clone https://github.com/your-username/Real-Time-Emotion-Aware-Learning-Environment.git
cd Real-Time-Emotion-Aware-Learning-Environment
```

2. (Optional) Create and activate a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

## 🚀 Run the Application

### Jupyter Notebook (Model Development)

```bash
jupyter notebook emotion_detection.ipynb
```

Use this notebook to train, test, and evaluate the deep learning model for emotion detection.

### Streamlit Dashboard

```bash
streamlit run emotion_dashboard.py
```

This will launch the real-time monitoring dashboard where the webcam input is processed for facial emotion recognition and visualized dynamically.

## 📊 Technologies Used

- Python 🐍
- OpenCV — face detection & image processing
- TensorFlow / Keras — deep learning for emotion recognition
- NumPy & Pandas — data handling
- Matplotlib & Seaborn — visualization and analytics
- Streamlit — real-time interactive dashboard

## 🧠 Model Details

- Model Type: Convolutional Neural Network (CNN)
- Input: Grayscale facial images (48x48)
- Output: Emotion classes (e.g., Happy, Sad, Angry, Neutral, Surprise)
- Dataset: FER2013 / custom dataset for facial expressions

## 🔮 Future Improvements

- Integrate emotion analytics with e-learning platforms (e.g., Moodle, Google Classroom)
- Use multi-modal inputs (voice tone, text sentiment)
- Improve accuracy using transfer learning (VGG16, ResNet50)
- Real-time emotion tracking of multiple users simultaneously
- Deploy system on web or cloud-based environments

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to your branch: `git push origin feature/your-feature`
5. Submit a Pull Request

## 📝 License

This project is licensed under the MIT License — see the `LICENSE` file for details.

## 👨‍💻 Author

**Abhitesh, Ayushi, Himanshi**  
B.Tech in Artificial Intelligence & Data Science
