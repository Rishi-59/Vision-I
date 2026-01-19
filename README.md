# Vision I  
### AI-Based Intelligent Visual Guidance System

Vision I is an AI-powered visual assistance system designed to help visually impaired users perceive and navigate their surroundings through real-time voice guidance. The project focuses on converting live camera input into meaningful audio instructions using computer vision and intelligent decision-making.

This project is developed as a **final-year capstone**, following a structured, modular, and professional AI system design approach.

---

## Problem Statement

Visually impaired individuals face significant challenges in understanding their surroundings and navigating safely in unfamiliar environments. Traditional assistive tools provide limited contextual awareness and often fail to deliver real-time guidance.

Vision I aims to address this problem by using artificial intelligence to interpret visual scenes and provide actionable voice-based navigation assistance.

---

## Project Objectives

- Capture live video input using a camera
- Detect objects in real time using AI-based computer vision
- Extract meaningful features such as distance, direction, and motion
- Analyze the environment using an intelligent decision engine
- Provide clear and timely voice guidance to the user
- Build a modular system that can be extended in future phases

---

## System Overview

Vision I follows a layered architecture:
```text
Camera
↓
Video Frame Capture
↓
Object Detection (Pretrained Model)
↓
Feature Extraction
(Distance, Direction, Motion)
↓
Decision Engine (Rule-Based AI)
↓
Voice Guidance
↓
User
```

Each module is designed independently to ensure clarity, scalability, and ease of maintenance.

---

## Project Phases

### Phase 1 – Visual Perception
- Real-time camera input
- Object detection using a pretrained deep learning model
- Voice alerts for detected objects

### Phase 2 – Intelligent Navigation (Planned)
- Distance estimation using visual cues
- Direction and motion analysis
- Rule-based decision-making for safe navigation
- Context-aware voice guidance

---

## Technology Stack

- **Programming Language:** Python 3.10  
- **Computer Vision:** OpenCV  
- **Object Detection:** Pretrained deep learning model (YOLO-based)  
- **Decision Logic:** Rule-based AI  
- **Audio Output:** Text-to-Speech (TTS)  
- **Numerical Processing:** NumPy  

---

## Repository Structure
```
vision-i/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── docs/
│ ├── problem_definition.md
│ ├── block_diagram.png
│ ├── algorithm.md
│
├── src/
│ ├── main.py
│ ├── config.py
│
│ ├── vision/
│ │ ├── camera.py
│ │ ├── detector.py
│
│ ├── features/
│ │ ├── distance.py
│ │ ├── direction.py
│ │ ├── motion.py
│
│ ├── decision/
│ │ └── rules.py
│
│ └── audio/
│   └── tts.py
│
└── tests/
```
---

## Design Philosophy

- Modular and explainable architecture  
- Separation of perception and intelligence  
- Minimal dependency on model retraining  
- Real-time performance focus  
- Academic clarity and practical applicability  

---

## Future Scope

- Custom object training (stairs, potholes, curbs)
- Mobile application integration
- GPS and outdoor navigation support
- Emergency alert and SOS features
- Multi-language voice support

---

## Project Status

🟡 In active development  
(Current focus: system design, algorithm definition, and module implementation)

---

## License

This project is developed for academic and research purposes.
