# ✋ Gesture-Based Brightness & Volume Control

A real-time **computer vision-based hand gesture controller** that lets you control your computer's **screen brightness and system volume using finger movements**.

The project uses **OpenCV** for webcam processing, **MediaPipe Hands** for hand landmark detection, `screen_brightness_control` for display brightness, and `pycaw` for Windows system-volume control.

---

## 🚀 Features

* 🎥 Real-time webcam-based hand tracking
* ✋ Detects hand landmarks using MediaPipe
* ☝️ **One finger up → Brightness control**
* ✌️ **Two fingers up → Volume control**
* ⬆️ Move your fingers upward to increase brightness/volume
* ⬇️ Move your fingers downward to decrease brightness/volume
* 🪟 Directly controls Windows system volume
* 🖥️ Directly controls display brightness
* ⚡ Real-time processing
* 🔴 Press `ESC` to exit

---

## 🧠 How It Works

The system follows a simple pipeline:

```text
Webcam
   ↓
OpenCV Frame Capture
   ↓
MediaPipe Hand Detection
   ↓
21 Hand Landmarks
   ↓
Finger Detection
   ↓
Gesture Classification
   ↓
Vertical Finger Movement
   ↓
Brightness / Volume Adjustment
```

### 1. Capture Webcam Input

OpenCV continuously captures frames from the webcam:

```python
cap = cv2.VideoCapture(0)
```

Each frame is flipped horizontally so that the movement feels natural, similar to looking into a mirror.

---

### 2. Detect the Hand

MediaPipe Hands detects the hand and provides **21 landmarks**.

Important landmarks used by this project include:

```text
4  → Thumb tip
8  → Index finger tip
12 → Middle finger tip
16 → Ring finger tip
20 → Pinky tip
```

The project primarily uses the **index and middle fingers** to determine the active control mode.

---

### 3. Detect Fingers

The `count_fingers()` function compares the vertical position of a fingertip with its corresponding lower joint.

For example:

```python
if hand_landmarks.landmark[tip_ids[i]].y < \
   hand_landmarks.landmark[tip_ids[i]-2].y:
    fingers.append(1)
```

Because MediaPipe coordinates are normalized:

```text
y = 0  → top of image
y = 1  → bottom of image
```

A smaller `y` value means the finger is higher.

---

## 🎛️ Gesture Controls

| Gesture          | Action             |
| ---------------- | ------------------ |
| ☝️ One finger    | Control brightness |
| ✌️ Two fingers   | Control volume     |
| ⬆️ Move upward   | Increase           |
| ⬇️ Move downward | Decrease           |
| `ESC`            | Exit application   |

### Brightness

When one finger is detected:

```python
if fingers_up == 1:
```

The program measures the change in the index finger's vertical position.

Moving upward produces a positive adjustment:

```text
Finger moves ↑
      ↓
Brightness increases
```

Moving downward:

```text
Finger moves ↓
      ↓
Brightness decreases
```

---

### 🔊 Volume

When two fingers are detected:

```python
elif fingers_up == 2:
```

The same vertical movement principle is applied to the Windows master-volume level.

The volume is represented as a value between:

```text
0.0 → 0%
1.0 → 100%
```

The value is then constrained to this range:

```python
max(0.0, min(1.0, current_vol + change))
```

---

## 🛠️ Technologies Used

| Technology                | Purpose                             |
| ------------------------- | ----------------------------------- |
| Python                    | Core programming language           |
| OpenCV                    | Webcam capture and image processing |
| MediaPipe                 | Hand and finger landmark detection  |
| NumPy                     | Numerical operations                |
| screen-brightness-control | Display brightness control          |
| Pycaw                     | Windows audio control               |
| COM                       | Windows audio interface             |

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/gesture-control.git
cd gesture-control
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install opencv-python mediapipe numpy screen-brightness-control pycaw comtypes
```

---

## ▶️ Running the Project

Run:

```bash
python gesture_control.py
```

Your webcam should open with a window titled:

```text
Finger Control
```

Show your hand to the camera and use the gestures described above.

Press:

```text
ESC
```

to terminate the program.

---

## 🖥️ System Requirements

### Operating System

This project is primarily designed for:

```text
Windows
```

because `pycaw` uses the Windows Core Audio API.

### Hardware

* Webcam
* Windows computer
* Display with software-controllable brightness

### Python

Python 3.x is recommended.

---

## 📁 Project Structure

```text
gesture-control/
│
├── gesture_control.py
├── README.md
├── requirements.txt
└── .gitignore
```

Example `requirements.txt`:

```text
opencv-python
mediapipe
numpy
screen-brightness-control
pycaw
comtypes
```

---

## ⚙️ Important Parameters

### Detection Confidence

```python
min_detection_confidence=0.7
```

This controls how confident MediaPipe needs to be before considering a hand detection valid.

Higher values can reduce false detections but may make detection less responsive.

---

### Sensitivity

```python
sensitivity = 0.4
```

This determines how strongly finger movement affects brightness or volume.

Increasing it:

```text
Higher sensitivity
      ↓
Small movement → larger adjustment
```

Decreasing it:

```text
Lower sensitivity
      ↓
Larger movement → smaller adjustment
```

---

## 🧩 Core Logic

The important variable is:

```python
prev_y
```

It stores the previous vertical position of the index finger.

The current position is:

```python
index_finger_y
```

The movement is calculated as:

```python
dy = prev_y - index_finger_y
```

Therefore:

```text
dy > 0 → finger moved upward
dy < 0 → finger moved downward
```

The program then maps this movement to either:

```text
Brightness
```

or:

```text
System Volume
```

depending on the detected gesture.

---

## 🔍 Example

Suppose the index finger was previously at:

```text
y = 400
```

and moves to:

```text
y = 350
```

Then:

```python
dy = 400 - 350
```

giving:

```text
dy = +50
```

The positive value means the finger moved upward.

For brightness:

```python
change = int(dy * sensitivity)
```

With:

```text
dy = 50
sensitivity = 0.4
```

the brightness adjustment becomes:

```text
20
```

So the brightness increases.

---

## ⚠️ Limitations

* Designed primarily for Windows.
* Requires a functioning webcam.
* Poor lighting can reduce hand-detection accuracy.
* Rapid hand movements may cause unstable adjustments.
* The current implementation supports only one detected hand.
* The thumb is not currently used for gesture classification.
* Continuous movement can cause repeated brightness/volume changes.

---

## 🔮 Future Improvements

Possible extensions include:

* 🤚 Support for multiple hand gestures
* 👌 Add more gesture commands
* 🤏 Pinch gesture for precise control
* 🖱️ Gesture-based mouse control
* ⏯️ Media play/pause gestures
* 🎵 Previous/next track controls
* 🔒 Gesture-based screen locking
* 📊 On-screen brightness and volume indicators
* 🎚️ Smoothing/filtering to prevent sudden changes
* 🧠 Custom gesture classification using machine learning
* 📱 Gesture-controlled presentation navigation
* 🖥️ Multi-monitor brightness control

---

## 🎯 Project Objective

The goal of this project is to demonstrate how **computer vision can be used as a human-computer interaction (HCI) interface**.

Instead of interacting with traditional physical controls:

```text
Hand Movement
      ↓
Computer Vision
      ↓
Gesture Recognition
      ↓
System Command
      ↓
Brightness / Volume
```

This creates a **touchless interface** for controlling common computer functions.

---

## 📚 Concepts Demonstrated

This project provides practical experience with:

* Computer Vision
* Real-time video processing
* Hand pose estimation
* Landmark detection
* Gesture recognition
* Human-Computer Interaction
* Windows system APIs
* Audio device control
* Hardware/software interaction
* Coordinate-based motion tracking

---

## 👩‍💻 Author

**Srutilaya Rajaraman**

Built as a computer-vision and human-computer-interaction project using Python, OpenCV and MediaPipe.
