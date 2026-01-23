# Vision I  
### AI-Based Intelligent Visual Guidance System

Vision I is an AI-powered intelligent visual assistance system designed to help visually impaired users perceive and navigate their surroundings through real-time voice guidance. The system transforms live camera input into meaningful, context-aware, safety-critical, and personalized audio instructions using computer vision and rule-based artificial intelligence.

This project is developed as a **final-year capstone**, following a structured, modular, and professional AI system engineering approach with strong emphasis on safety, explainability, and human-centric design.

---

## Problem Statement

Visually impaired individuals face significant challenges in understanding their surroundings and navigating safely, especially in unfamiliar or dynamic environments. Traditional assistive tools provide limited contextual awareness and often fail to adapt to changing environmental conditions or individual user needs.

Vision I addresses this challenge by combining real-time computer vision with intelligent decision-making to provide adaptive and reliable voice-based navigation assistance.

---

## Project Objectives

- Capture live video input using a camera  
- Detect objects in real time using deep learning  
- Extract spatial and temporal features (distance, direction, motion)  
- Infer environmental context (e.g., crowded, outdoor)  
- Apply rule-based intelligent decision-making  
- Escalate alerts based on safety severity  
- Reduce alert fatigue using short-term memory  
- Personalize guidance based on user profiles  
- Deliver clear, timely, and human-centric voice guidance  
- Build a modular and extensible AI system  

---

## System Overview

Vision I follows a layered, intelligence-driven architecture:

```text
Camera
↓
Object Detection (YOLO)
↓
Feature Extraction
(Distance, Direction, Motion)
↓
Scene Context Inference
↓
Adaptive Decision Engine
↓
Safety Escalation & Short-Term Memory
↓
User Profile Personalization
↓
Voice Guidance
↓
User
```

Each layer is independently designed to ensure clarity, scalability, and maintainability.

---

## Project Phases

### Phase 1 – Visual Perception
- Live camera feed acquisition
- Object detection using a pretrained YOLO model
- Basic voice alerts for detected objects

### Phase 2 – Intelligent Navigation
- Distance estimation using bounding box geometry
- Direction estimation (left, center, right)
- Motion analysis (approaching, static)
- Rule-based navigation guidance

### Phase 3 – Adaptive Intelligence
- Adaptive distance thresholds based on system behavior
- Decision logging and metrics collection
- Performance monitoring (alerts per minute, response time)

### Phase 4 – System Robustness
- Configuration-driven system behavior
- Runtime controls and safe shutdown
- Final metrics reporting

### Phase 5 – Advanced Intelligence & Human-Centric Design

#### Phase 5.1 – Context Awareness
- Infers scene context (crowded, outdoor, indoor)
- Dynamically adjusts distance thresholds
- Reduces unnecessary alerts in dense environments

#### Phase 5.2 – Safety & Alert Escalation
- Classifies alerts into severity levels (LOW, HIGH, CRITICAL)
- Bypasses cooldown for safety-critical situations
- Escalates alert urgency when required

#### Phase 5.3 – Short-Term Memory
- Remembers recently alerted objects across frames
- Suppresses repeated alerts for the same obstacle
- Ensures critical alerts are never suppressed

#### Phase 5.4 – User Profiles & Personalization
- Supports configurable user profiles (cautious, normal, fast)
- Personalizes alert sensitivity, cooldown duration, and verbosity
- Enables human-centric adaptation without retraining models

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Programming Language | Python 3.10 |
| Computer Vision | OpenCV |
| Object Detection | YOLO (Ultralytics) |
| Decision Logic | Rule-based AI |
| Audio Output | Text-to-Speech (TTS) |
| Configuration | YAML-based profiles |
| Numerical Processing | NumPy |

---

## Repository Structure

```
vision-i/
│
├── README.md
├── requirements.txt
├── .gitignore
├── activate_venv.ps1
│
├── .venv/                     # Python virtual environment (ignored)
│
├── config/
│   └── user_profile.yaml      # User personalization profiles
│
├── docs/
│   ├── problem_definition.md
│   ├── block_diagram.png
│   ├── algorithm.md
│   └── system_capabilities.md
│
├── src/
│   ├── main.py                # Application entry point
│
│   ├── vision/                # Visual perception layer
│   │   ├── camera.py
│   │   └── detector.py
│
│   ├── features/              # Feature extraction
│   │   ├── distance.py
│   │   ├── direction.py
│   │   └── motion.py
│
│   ├── context/               # Scene context inference
│   │   └── scene_context.py
│
│   ├── decision/              # Decision engine
│   │   └── rules.py
│
│   ├── safety/                # Alert escalation
│   │   └── alert_manager.py
│
│   ├── memory/                # Short-term memory
│   │   └── short_term_memory.py
│
│   ├── profiles/              # User personalization
│   │   └── user_profile.py
│
│   ├── utils/                 # Logging and metrics
│   │   ├── logger.py
│   │   └── metrics.py
│
│   └── audio/                 # Voice output
│       └── tts.py
│
└── tests/                     # Unit and integration tests
```

---

## Design Philosophy

- Modular and explainable architecture
- Safety-first decision making
- Separation of perception, intelligence, and interaction
- Minimal dependency on model retraining
- Human-centric personalization
- Real-time performance focus
- Academic clarity with practical applicability

---

## Future Scope

- Custom object training (stairs, potholes, curbs)
- Sensor fusion and depth-based distance estimation
- Mobile and wearable device deployment
- GPS-based outdoor navigation
- Emergency detection and SOS alerts
- Multi-language and emotion-aware voice output

---

## Project Status

🟢 **Core system completed (Phase 5)**  
Current focus: documentation, evaluation, and final presentation

---

## License

This project is developed for academic and research purposes only.