# 🏏 Cricket Player Analyzer

## 👩‍💻 Authors

* **Bandi Pranathi**
* **K. V. Lakshman**

---

## 🌟 Overview

Cricket Player Analyzer is a web-based analytics system that evaluates cricket players based on performance metrics and intelligently classifies their roles (Batsman, Bowler, All-rounder, Wicketkeeper).

It provides advanced features such as player comparison, team balance analysis, leaderboard generation, and best team selection using data-driven techniques.

---

![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?logo=flask)
![JavaScript](https://img.shields.io/badge/JavaScript-Frontend-yellow?logo=javascript)
![Chart.js](https://img.shields.io/badge/Chart.js-Data%20Visualization-orange?logo=chartdotjs)
![Data Analytics](https://img.shields.io/badge/Data%20Analytics-Player%20Analysis-blue)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
## 🚀 Features

* 🧠 Player Role Classification
* 📊 Radar Chart Visualization (Chart.js)
* ⚔️ Player Comparison System
* 🏏 Best Playing XI Generator
* ⚖️ Team Balance Analyzer
* 🥇 Leaderboard by Role
* 🌐 Interactive Web Interface

---

## 🛠️ Tech Stack

* Python (Flask)
* JavaScript
* Chart.js
* HTML / CSS

---

## 📂 Project Structure

```bash
Cricket-Player-Analyzer/
├── app.py                  # Flask backend
├── static/
│   ├── script.js           # Frontend logic (charts, API calls)
│   └── style.css
├── templates/
│   └── index.html
├── data/                   # Player data (synthetic dataset)
├── utils/                  # Helper functions
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 📊 Dataset (Synthetic Data)

This project uses a **synthetic dataset** created to simulate real-world cricket player statistics.

### 🧩 Features included:

* Matches played
* Batting innings
* Runs scored
* Highest score
* Batting average
* Strike rate
* Number of 50s and 100s
* Wickets taken
* Economy rate
* Bowling strike rate

### 🎯 Purpose:

* Mimics realistic cricket performance data
* Enables testing and development without relying on external datasets
* Helps in validating player classification and team selection logic

> ⚠️ Note: This dataset is artificially generated and may not reflect real-world player statistics.

---

## ⚙️ How It Works

1. User inputs player statistics
2. System analyzes performance
3. Assigns role (Batsman/Bowler/All-rounder)
4. Generates radar chart visualization
5. Enables:

   * Player comparison
   * Team balance evaluation
   * Best XI generation

---

## 📊 Key Functionalities

### 📈 Radar Chart Visualization

Displays player strengths across:

* Batting performance
* Bowling performance
* Consistency

---

### ⚔️ Player Comparison

Compare two players based on:

* Performance score
* Consistency
* Overall metrics

---

### ⚖️ Team Balance Analyzer

* Select exactly 11 players
* System evaluates:

  * Batsmen
  * Bowlers
  * All-rounders
  * Wicketkeepers

---

### 🏏 Best Team Generator

* Automatically generates optimal playing XI
* Considers:

  * Player performance
  * Team balance

---

## ▶️ How to Run

```bash
git clone https://github.com/your-username/Cricket-Player-Analyzer.git
cd Cricket-Player-Analyzer
pip install -r requirements.txt
python app.py
```

Open in browser:

```
http://127.0.0.1:5000
```

---

## 📸 Screenshots

(
<img width="624" height="447" alt="Screenshot 2026-04-19 at 1 19 19 PM" src="https://github.com/user-attachments/assets/649aa91a-3607-46ce-91eb-db97a5219492" />
<img width="820" height="487" alt="Screenshot 2026-04-19 at 1 20 14 PM" src="https://github.com/user-attachments/assets/adf157e3-84e2-493d-942e-92ec84eefb5b" />
<img width="1672" height="1634" alt="Image 25-04-2026 at 2 03 PM" src="https://github.com/user-attachments/assets/35e6af51-6e8f-4952-9ddc-ef656bcb8aea" />
<img width="1588" height="1346" alt="Image 25-04-2026 at 2 04 PM" src="https://github.com/user-attachments/assets/29a643ba-9b15-456a-bff7-a3f66b7befe0" />
<img width="1503" height="1222" alt="Image 25-04-2026 at 2 05 PM (1)" src="https://github.com/user-attachments/assets/eed6ff57-0df1-4e9f-958e-a4eaeb881b7a" />
<img width="1313" height="714" alt="Image 25-04-2026 at 2 06 PM" src="https://github.com/user-attachments/assets/e31c777a-9cf2-4715-971d-066ac2fd404a" />


<img width="1365" height="1319" alt="Image 25-04-2026 at 2 08 PM" src="https://github.com/user-attachments/assets/62d9bf10-f886-41d5-8d09-c48d90c6c58f" />

)

---

## 🔮 Future Improvements

* Integration with real cricket datasets (IPL, ICC)
* Machine learning-based performance prediction
* Live match data integration
* Advanced analytics dashboard
* Mobile responsive UI

---

## 🏁 Conclusion

This project demonstrates how data analytics and visualization techniques can be applied to cricket performance analysis, enabling smarter team selection and player evaluation.

---

## ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub!
