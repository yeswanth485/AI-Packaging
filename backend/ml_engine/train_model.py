from __future__ import annotations

import argparse
from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

from ml_engine.dataset_loader import load_dataset


DEFAULT_DATASET = "packaging_dataset.csv"
DEFAULT_MODEL_PATH = "packaging_model.pkl"


def train(
    dataset_path: str = DEFAULT_DATASET,
    model_path: str = DEFAULT_MODEL_PATH,
    n_estimators: int = 200,
    max_depth: int | None = None,
    random_state: int = 42,
) -> None:
    """
    Training pipeline:
    1. Load dataset
    2. Clean invalid rows (handled in loader)
    3. Split train/test
    4. Train RandomForestClassifier
    5. Evaluate
    6. Save trained model to packaging_model.pkl
    """
    X_train, X_test, y_train, y_test = load_dataset(dataset_path, random_state=random_state)

    clf = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=random_state,
        n_jobs=-1,
    )
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Test accuracy: {acc:.4f}")
    print(classification_report(y_test, y_pred))

    out_path = Path(model_path)
    joblib.dump(clf, out_path)
    print(f"Saved trained model to: {out_path.resolve()}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Train packaging RandomForest model.")
    parser.add_argument(
        "--dataset",
        type=str,
        default=DEFAULT_DATASET,
        help="Path to CSV dataset (default: packaging_dataset.csv)",
    )
    parser.add_argument(
        "--model-out",
        type=str,
        default=DEFAULT_MODEL_PATH,
        help="Output path for trained model (default: packaging_model.pkl)",
    )
    args = parser.parse_args()

    train(dataset_path=args.dataset, model_path=args.model_out)


if __name__ == "__main__":
    main()

