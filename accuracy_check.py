import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score, StratifiedKFold, KFold
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score
import warnings

# --- Import Twelve Distinct Models ---
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier # <--- AB ADDED
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB # <--- GNB ADDED
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis # <--- LDA ADDED

# Import specialized boosting libraries (requires installation: pip install xgboost lightgbm)
try:
    import xgboost as xgb # <--- XGBoost ADDED
    import lightgbm as lgb # <--- LightGBM ADDED
except ImportError:
    print("Warning: XGBoost or LightGBM not installed. Skipping these models.")
    xgb = None
    lgb = None


# Suppress known warnings for clean output
warnings.filterwarnings('ignore')

# ===============================
# 1. Load and Preprocess Data 
# ===============================
try:
    # NOTE: Ensure the path to your CSV file is correct!
    df = pd.read_csv("dataset_crickett.csv")
except FileNotFoundError:
    print("CRITICAL ERROR: Dataset file not found at the specified path.")
    exit()

feature_cols = [
    "matches played", "bat innings", "bat runs", "bat avg", "bat sr", "50s", "100s",
    "bowl innings", "overs", "wickets", "bowl avg", "econ", "bowl sr"
]

X = df[feature_cols]
y = df["role"]

# Preprocessing
le = LabelEncoder()
y_encoded = le.fit_transform(y)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


# ===============================
# 2. Define Models for Comparison (UPDATED: Total 11 Models)
# ===============================
models = {
    "Logistic Regression (LR)": LogisticRegression(solver='lbfgs', multi_class='multinomial', random_state=42, max_iter=1000),
    "Random Forest (RF)": RandomForestClassifier(n_estimators=100, random_state=42),
    "Support Vector Machine (SVC)": SVC(kernel='rbf', random_state=42),
    "K-Nearest Neighbors (KNN)": KNeighborsClassifier(n_neighbors=5),
    "Gradient Boosting (GBM)": GradientBoostingClassifier(n_estimators=100, random_state=42),
    "Decision Tree (DT)": DecisionTreeClassifier(random_state=42),
    # --- ADDED FIVE NEW MODELS ---
    "XGBoost Classifier (XGB)": xgb.XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42, n_estimators=100) if xgb else None,
    "LightGBM (LGBM)": lgb.LGBMClassifier(random_state=42, n_estimators=100) if lgb else None,
    "AdaBoost Classifier (AB)": AdaBoostClassifier(random_state=42, n_estimators=100),
    "Gaussian Naive Bayes (GNB)": GaussianNB(),
    "Linear Discriminant Analysis (LDA)": LinearDiscriminantAnalysis(),
}

# Remove models that couldn't be imported (if xgboost or lightgbm weren't installed)
models = {k: v for k, v in models.items() if v is not None}


# ===============================
# 3. Stratified 5-Fold Cross-Validation Evaluation
# ===============================

# Use StratifiedKFold for more reliable results in multi-class classification
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

print("=" * 75)
print("  🏆 Model Accuracy Comparison using STRATIFIED 5-Fold CV (11 Models)")
print("=" * 75)
print(f"{'Model Name':<35} | {'Mean CV Accuracy':<20} | {'Std. Dev':<10}")
print("-" * 75)

results_stratified_cv = {}
for name, model in models.items():
    # Perform cross-validation
    cv_scores = cross_val_score(model, X_scaled, y_encoded, cv=skf, scoring="accuracy", n_jobs=-1)
    
    mean_accuracy = np.mean(cv_scores)
    std_dev = np.std(cv_scores)
    
    results_stratified_cv[name] = mean_accuracy
    
    print(f"{name:<35} | {mean_accuracy:<20.4f} | {std_dev:<.4f}")

print("-" * 75)
print(f"Highest Mean Accuracy (Stratified): {max(results_stratified_cv.values()):.4f}")
print("=" * 75)


# ===============================
# 4. Standard 5-Fold Cross-Validation Evaluation
# ===============================

# Use KFold for standard cross-validation
kf = KFold(n_splits=5, shuffle=True, random_state=42)

print("\n" + "=" * 75)
print("  📉 Model Accuracy Comparison using STANDARD 5-Fold CV (11 Models)")
print("=" * 75)
print(f"{'Model Name':<35} | {'Mean CV Accuracy':<20} | {'Std. Dev':<10}")
print("-" * 75)

results_standard_cv = {}
for name, model in models.items():
    # Perform standard K-Fold cross-validation
    cv_scores = cross_val_score(model, X_scaled, y_encoded, cv=kf, scoring="accuracy", n_jobs=-1)
    
    mean_accuracy = np.mean(cv_scores)
    std_dev = np.std(cv_scores)
    
    results_standard_cv[name] = mean_accuracy
    
    print(f"{name:<35} | {mean_accuracy:<20.4f} | {std_dev:<.4f}")

print("-" * 75)
print(f"Highest Mean Accuracy (Standard): {max(results_standard_cv.values()):.4f}")
print("=" * 75)