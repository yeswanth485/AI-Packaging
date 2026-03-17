"""
Generates a lightweight packaging recommendation model and saves it as packaging_model.pkl.
Run this once before starting the server or during Docker build.
"""
from __future__ import annotations

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Training data: [length, width, height, weight, quantity] → box label
X = np.array([
    [10, 8, 5, 0.5, 1],
    [12, 10, 6, 0.8, 1],
    [15, 10, 8, 1.0, 2],
    [20, 15, 10, 2.0, 3],
    [25, 18, 12, 3.0, 4],
    [30, 20, 10, 4.0, 5],
    [35, 25, 15, 5.0, 6],
    [40, 30, 20, 8.0, 8],
    [45, 35, 25, 10.0, 10],
    [50, 40, 30, 15.0, 12],
])

y = [
    "Box_A",
    "Box_A",
    "Box_A",
    "Box_B",
    "Box_B",
    "Box_B",
    "Box_C",
    "Box_C",
    "Box_C",
    "Box_C",
]

model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X, y)

joblib.dump(model, "packaging_model.pkl")
print("Model saved to packaging_model.pkl")
