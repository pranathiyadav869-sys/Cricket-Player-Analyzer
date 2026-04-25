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

(<img width="1437" height="819" alt="Screenshot 2025-10-29 at 9 46 21 PM" src="https://github.com/user-attachments/assets/513e6f76-d528-4bc7-95e5-925eae88f435" />

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
