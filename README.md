# 🎯 Attendance Marker by Face Recognition | Raspberry Pi

An **automated attendance system** built using a **Raspberry Pi** and an integrated **camera module** that captures real-time classroom photos and marks attendance through **face recognition**.  
The system achieves a **93% accuracy rate**, enhancing classroom management efficiency and reducing manual effort.

---

## 📅 Project Duration
**January 2025 – April 2025**

---

## 👥 Team
- **Team Lead:** [Your Name]  
- **Team Size:** 4 Members  
- Responsibilities:
  - Led project planning and weekly progress meetings  
  - Managed dataset creation and verification  
  - Coordinated Raspberry Pi integration and server communication

---

## 🚀 Features
- 📸 Real-time image capture every 1–2 seconds using Raspberry Pi Camera Module  
- 🧠 Face recognition and matching against pre-registered student dataset  
- ☁️ Automatic image upload to a remote server for processing  
- ✅ Attendance marking with **93% recognition success rate**  
- 🧾 Easy dataset management with registered names and photographs  
- ⚙️ Scalable system design adaptable for classrooms or offices  

---

## 🧩 System Architecture

**Hardware Components:**
- Raspberry Pi (Model 3B/4)
- Raspberry Pi Camera Module
- Wi-Fi or Ethernet Connectivity
- Power Supply

**Software Stack:**
- Python (OpenCV, face_recognition, NumPy, Flask)
- SQLite / MySQL (for attendance database)
- Server (Local/Cloud-based for processing)
- Raspbian OS

---

## 🔄 Workflow
1. **Image Capture:**  
   Raspberry Pi camera continuously captures classroom images every 1–2 seconds.

2. **Image Upload:**  
   Captured images are sent to the server via Wi-Fi for analysis.

3. **Face Recognition:**  
   Server compares detected faces with the registered student dataset using the `face_recognition` library.

4. **Attendance Marking:**  
   When a match is found, the student’s attendance is marked automatically in the database.

5. **Dashboard (Optional):**  
   Real-time attendance visualization via a simple web dashboard built using Flask.

---

## 🛠️ Installation & Setup

### 📍 Prerequisites
- Raspberry Pi with Camera Module enabled
- Python 3.x installed
- Internet connection
- Server (local or cloud) with sufficient compute capability

### 💻 Steps
```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/attendance-marker-raspberrypi.git
cd attendance-marker-raspberrypi

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the capture script on Raspberry Pi
python capture.py

# 4. Start the server for face recognition
python server.py
