# **Bachelor Thesis Project: Design and Implementation of Medical Image Segmentation System**
<img src="assets/demo.png" alt="Screenshot" width="600"/>

## **Table of Contents**
- [Introduction](#introduction)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Methodology](#methodology)
- [Results](#results)
- [Future Work](#future-work)
- [References](#references)
- [Contact](#contact)

## **Introduction**

 A system for fetal ultrasound image segmentation using YOLOv5 for object detection and a U-Net
variant for accurate head circumference measurement. Designed a user-friendly GUI with PyQt, following the
MVC pattern. It includes image browsing, one-click image annotation operation,
label correction, saving and other functions. The system can greatly reduce the cost of
medical image annotation and relieve the pressure of operator.

## **Project Structure**

```plaintext
project-root/
├── client/                 # GUI source code
├── HC18Challege/           # Source code for model training and inference
├── test/                   # Example Data
├── log/                    # Results and figures
├── README.md               # This README file
└── requirements.txt        # Project dependencies
```

## **Installation**

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Lumiere401/graduate-design.git
   cd graduate-design
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## **Usage**

Instructions on how to run the project.

```bash
python .\client\main.py 
```

## **Methodology**

### Annoation 
![Alt text](./assets/demo2.png "a title")
## **Results**

Summary of the key results with references to figures or tables.

## **Future Work**

Suggestions for future research or improvements.

## **References**

List of references used in the project.

## **Contact**

**Your Name**  
[Email Address](mailto:youremail@example.com)  
[GitHub Profile](https://github.com/yourusername)

---

### **Notes:**
- Replace placeholders (e.g., `[Your Project Title]`) with actual information.
- Adjust the content to match your project's specifics.
- Keep it concise and focused on essential information.

This simplified README should be easy to follow and maintain, providing just enough information for someone to understand and use your bachelor thesis project.