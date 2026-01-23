# AI-Based Intelligent Visual Guidance System for Visually Impaired Users  
## Phase 2 – Technical Specification Document

---

## 1. Target User Profile

The system is designed to assist visually impaired individuals in navigating both indoor and outdoor environments by providing real-time, voice-based navigation guidance derived from visual understanding of the surroundings.

The target users may rely primarily on auditory feedback for situational awareness and require clear, timely, and actionable instructions rather than raw visual or object-level information.

---

## 2. Phase 2 Objectives

Phase 2 focuses on transforming a basic object detection pipeline into an **intelligent navigation assistance system** capable of interpreting visual information and generating meaningful guidance.

The key objectives of Phase 2 are:

- **Contextual Interpretation**  
  Move beyond object labels to understand spatial relationships and navigation relevance.

- **Hazard Identification**  
  Identify potential risks based on object position, distance, and motion.

- **Actionable Guidance**  
  Generate clear navigation instructions that assist safe movement rather than descriptive outputs.

---

## 3. Critical Navigation Scenarios

Based on common challenges faced by visually impaired users, the following navigation scenarios were identified as critical, realistic, and achievable within the scope of a final-year capstone project.

### 3.1 Intelligence Specification Matrix

| Situation Detected | Condition Evaluated | System Decision | Voice Guidance Output |
|-------------------|---------------------|-----------------|----------------------|
| Obstacle ahead | Object detected in center region within safety distance | Stop movement | “Obstacle ahead. Please stop.” |
| Clear path | No object detected in center region | Continue movement | “Path is clear. Go straight.” |
| Obstacle on left | Object detected only in left region | Avoid left side | “Obstacle on left. Move right.” |
| Obstacle on right | Object detected only in right region | Avoid right side | “Obstacle on right. Move left.” |
| Approaching object | Object shows decreasing distance across frames | High-risk warning | “Warning. Object approaching ahead.” |
| Crowd detected | Multiple persons detected within close proximity | Reduce speed | “Crowded area ahead. Move slowly.” |
| Narrow passage | Obstacles detected on both sides | Careful navigation | “Narrow path ahead. Proceed carefully.” |

These scenarios form the foundation for the system’s rule-based decision logic.

---

## 4. Visual Information Requirements

To enable intelligent navigation decisions, the system extracts the following information from detected objects using monocular camera input:

| Visual Information | Purpose |
|-------------------|---------|
| Object class label | Identify obstacle or entity type |
| Bounding box size | Approximate object distance |
| Bounding box position | Determine left, center, or right placement |
| Frame-to-frame variation | Detect object motion or approach |

**Note:**  
The system does not rely on additional sensors such as LiDAR or depth cameras. All spatial reasoning is derived from 2D visual input for simplicity and deployability.

---

## 5. System Intelligence Architecture

The system adopts a **hybrid intelligence architecture**, combining deep learning-based perception with rule-based reasoning.

- **Perception Layer**  
  A pretrained deep learning model performs object detection and localization.

- **Reasoning Layer**  
  A deterministic, rule-based decision engine evaluates extracted features to generate navigation guidance.

### 5.1 Design Rationale

This architectural choice ensures:

- **Explainability**  
  Decision logic can be clearly explained and validated.

- **Development Efficiency**  
  Reduces the need for large custom datasets and extensive retraining.

- **Academic Suitability**  
  Balances practical implementation with theoretical understanding.

---

## 6. AI Integration Framework

| System Component | AI / Computational Role |
|------------------|-------------------------|
| Object detection | Deep learning (pretrained convolutional neural network) |
| Distance estimation | Mathematical approximation using bounding box geometry |
| Direction estimation | Spatial analysis relative to frame center |
| Motion detection | Temporal comparison across frames |
| Decision making | Rule-based artificial intelligence |
| Voice guidance | Natural language instruction generation |

---

## 7. Expected Phase 2 Deliverables

Upon completion of Phase 2, the system is expected to:

- Interpret spatial context of detected objects
- Identify navigation-relevant hazards
- Generate meaningful and actionable voice instructions
- Operate in real time using a single camera
- Demonstrate explainable decision-making behavior

These deliverables establish a strong foundation for subsequent phases involving adaptation, safety escalation, and personalization.

---

## 8. Capstone Project Justification

Phase 2 significantly strengthens the project’s suitability as a final-year capstone by demonstrating:

- **Technical Depth**  
  Practical application of computer vision and AI concepts.

- **System Integration**  
  Coordination between perception, reasoning, and interaction layers.

- **Social Impact**  
  Direct relevance to assistive technology for visually impaired users.

- **Academic Rigor**  
  Clear problem formulation, structured logic, and evaluable outcomes.

---

**Document Version**: 2.0  
**Last Updated**: January 2026  
**Project**: Vision I – AI-Based Intelligent Visual Guidance System
