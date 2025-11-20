<div align="center">

# Leaf Disease Identification using Fuzzy Logic

![last-commit](https://img.shields.io/github/last-commit/Gushtasp47/Leaf-Disease-Identification-using-Fuzzy?style=flat&logo=git&logoColor=white&color=0080ff)
![repo-top-language](https://img.shields.io/github/languages/top/Gushtasp47/Leaf-Disease-Identification-using-Fuzzy?style=flat&color=0080ff)
![repo-language-count](https://img.shields.io/github/languages/count/Gushtasp47/Leaf-Disease-Identification-using-Fuzzy?style=flat&color=0080ff)

**Built with:**

![Python](https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000.svg?style=flat&logo=flask&logoColor=white)
![FuzzyLogic](https://img.shields.io/badge/FuzzyLogic-0080ff.svg?style=flat)

A fuzzy-logic–based expert system for identifying common leaf diseases using rule-based inference and membership functions.  
The system runs as a simple and interactive **Flask web application**.

</div>

---

## Table of Contents

- [Project Description](#project-description)
- [Disease Set](#disease-set)
- [Tech Stack](#tech-stack)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [How It Works](#how-it-works)
- [How to Run](#how-to-run)
- [Credits](#author)

---

## Project Description

This project implements a **Fuzzy Inference System (FIS)** to classify leaf diseases based on visual and environmental attributes such as:

- Color  
- Texture  
- Shape  
- Curling severity  
- Necrosis  
- Defoliation  
- Temperature  
- Humidity  
- Sunlight exposure  

Using **skfuzzy**, the system defines membership functions and expert-designed rules to infer the most likely disease and calculate **confidence levels**.

A simple Flask UI allows users to enter symptoms via dropdowns and get instant analysis.

---

## Disease Set

The fuzzy system currently supports classification of:

- **Powdery Mildew**  
- **Downy Mildew**  
- **Leaf Rust**  
- **Early Blight**  
- **Late Blight**  
- **Anthracnose**  
- **Botrytis Blight**  
- **Septoria Leaf Spot**
- **Tip Burn**
- **Black Spot**
- 

Each disease has its own expert-defined rule set and matching conditions.

---

## Tech Stack

| Component | Technology |
|----------|------------|
| **Backend** | Python, scikit-fuzzy, Flask |
| **Frontend** | HTML (render_template_string), Bootstrap (optional) |
| **Inference Engine** | Mamdani Fuzzy Inference System |
| **Deployment** | Localhost |

---

## Key Features

- Fully functional fuzzy inference model  
- Multi-disease classification  
- Custom membership functions for all inputs  
- Flask web UI for interactive diagnosis  
- Computes **confidence scores** for each disease  
- Handles missing attributes with neutral fuzzy values  
- Extensive rule coverage (30+ expert rules)

---

## Architecture
User Input-> Membership Functions -> Rule Evaluation -> Aggregation -> Defuzzification -> Disease + Confidence Output


## How It Works

### Membership Functions  
Each variable maps to a numerical range (0–10).  
Neutral values are used when input is missing.

### Fuzzy Rules  
Expert rules such as:
IF color is yellowish AND texture is powdery AND humidity is high
THEN disease is Powdery Mildew

Rules are combined using fuzzy AND/OR operations.

### Disease Scoring  
Every rule adds +1 to the matching disease.  
The final disease is chosen as the one with the highest score.  
Confidence = score / total_rules_matching

### Flask Web App  
Users select symptoms → backend fuzzy system runs → disease returned.

---

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/Gushtasp47/Leaf-Disease-Identification-using-Fuzzy.git
   cd Leaf-Disease-Identification-using-Fuzzy

2. Create a virtual environment(optional):
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
3. Install dependencies:
   ```bash
   pip install skfuzzy, flask, numpy
4. Run the Flask app(user-interface.py):
   ```bash
   python ui.py
5. Open your browser:
   http://127.0.0.1:5000/


## Author

**Author:** Shehzada Gushtasp Khan, Kashan Maqsood, Mahad Ajmal, Khubaib Muhammad   
**Course:** Knowledge Representation & Reasoning   
**Institution:** Bahria University
