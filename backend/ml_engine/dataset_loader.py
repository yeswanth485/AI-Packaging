from __future__ import annotations

from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


def load_dataset(
    csv_path: str | Path,
    test_size: float = 0.2,
    random_state: int = 42,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Load packaging dataset from CSV and return train/test splits.

    Expected columns:
      - length, width, height, weight, box_type
    """
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at: {path}")

    df = pd.read_csv(path)

    # Basic cleaning: drop rows with missing values
    df = df.dropna(subset=["length", "width", "height", "weight", "box_type"])

    # Filter invalid dimensions / weight
    df = df[
        (df["length"] > 0)
        & (df["width"] > 0)
        & (df["height"] > 0)
        & (df["weight"] > 0)
    ]

    if df.empty:
        raise ValueError("No valid rows after cleaning dataset.")

    X = df[["length", "width", "height", "weight"]].to_numpy(dtype=float)
    y = df["box_type"].astype(str).to_numpy()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    return X_train, X_test, y_train, y_test

