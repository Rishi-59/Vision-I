# AI-Based Intelligent Visual Guidance System for Visually Impaired Users

## Phase 2 Technical Specification Document

---

## 1. Target User Profile

The system is designed to assist visually impaired individuals in navigating indoor and outdoor environments safely by providing real-time voice guidance based on visual understanding of surroundings.

---

## 2. Phase 2 Objectives

The objective of Phase 2 is to upgrade the existing object detection system into an intelligent assistive system with the following capabilities:

- **Contextual Understanding**: Interpret the environment beyond simple object recognition
- **Hazard Identification**: Detect and evaluate potential dangers in real-time
- **Actionable Guidance**: Provide meaningful navigation instructions rather than raw object labels

---

## 3. Critical Navigation Scenarios

Based on common navigation challenges faced by visually impaired users, the following situations have been identified as critical and achievable within the scope of this capstone project.

### 3.1 Intelligence Specification Matrix

| Situation Detected | Condition Evaluated | System Decision | Voice Guidance Output |
|-------------------|---------------------|-----------------|----------------------|
| Obstacle ahead | Object distance < 2 meters in center | Stop movement | "Obstacle ahead. Please stop." |
| Clear path | No object in center region | Move forward | "Path is clear. Go straight." |
| Obstacle on left | Object detected only on left | Avoid left side | "Obstacle on left. Move right." |
| Obstacle on right | Object detected only on right | Avoid right side | "Obstacle on right. Move left." |
| Moving vehicle | Object approaching with increasing speed | Danger alert | "Vehicle approaching. Stay back." |
| Crowd detected | Multiple persons within close range | Slow movement | "Crowded area ahead. Move slowly." |
| Narrow passage | Objects detected on both sides | Careful navigation | "Narrow path ahead. Proceed carefully." |

---

## 4. Visual Information Requirements

To enable intelligent decision-making, the system extracts the following information from detected objects:

| Information | Purpose |
|------------|---------|
| Object type | Identify obstacle or vehicle |
| Bounding box size | Estimate distance |
| Object position | Determine left, center, right |
| Frame-to-frame change | Detect motion |

**Note**: No additional sensors are required. All information is derived from monocular camera input.

---

## 5. System Intelligence Architecture

The system employs a hybrid approach combining deep learning perception with rule-based reasoning:

- **Perception Layer**: Pretrained object detection model
- **Reasoning Layer**: Rule-based decision engine for guidance generation

### 5.1 Design Rationale

This approach ensures:

- **Explainability**: Clear logic paths for decision-making
- **Faster Development**: Leverages existing pretrained models
- **Academic Suitability**: Appropriate complexity for evaluation and demonstration

---

## 6. AI Integration Framework

| Component | AI Role |
|-----------|---------|
| Object detection | Deep Learning (Pretrained CNN) |
| Distance estimation | Mathematical approximation |
| Motion detection | Temporal analysis |
| Decision making | Rule-based AI |
| Voice guidance | Natural language generation |

---

## 7. Expected Phase 2 Deliverables

Upon successful implementation of Phase 2, the system will demonstrate the following capabilities:

- Understand spatial context of the environment
- Predict potential dangers based on object behavior
- Guide users using meaningful, context-aware voice instructions
- Function in real-time using a single camera input

---

## 8. Capstone Project Justification

This project is suitable for a final-year capstone because it:

- **Technical Depth**: Applies AI and computer vision concepts in a practical implementation
- **System Integration**: Combines multiple components into a cohesive solution
- **Social Impact**: Addresses a real-world assistive technology challenge
- **Academic Rigor**: Demonstrates both engineering implementation and analytical thinking

---

**Document Version**: 1.0  
**Last Updated**: January 2026