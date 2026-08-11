import os
import logging
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
import sys
from pathlib import Path

# Add project root to sys.path so we can import ai.utils
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from ai.utils import constants

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

def train():
    logger.info("Starting model training...")
    
    # 1. Load data
    dataset_path = constants.DATASET_PATH
    if not dataset_path.exists():
        logger.error(f"Dataset not found at {dataset_path}")
        return
        
    df = pd.read_csv(dataset_path)
    logger.info(f"Loaded dataset with {len(df)} rows and {len(df.columns)} columns.")
    
    # 2. Prepare features and target
    X = df[constants.FEATURE_COLUMNS]
    y = df[constants.LABEL_COLUMN]
    
    # 3. Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 4. Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 5. Train KNN model
    knn = KNeighborsClassifier(n_neighbors=constants.KNN_N_NEIGHBORS, weights=constants.KNN_WEIGHTS)
    knn.fit(X_train_scaled, y_train)
    
    # 6. Evaluate
    y_pred = knn.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    logger.info(f"Model Accuracy on Test Set: {acc:.4f}")
    
    # Cross validation
    cv_scores = cross_val_score(knn, X_train_scaled, y_train, cv=5)
    logger.info(f"Cross Validation Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    logger.info("\nClassification Report:\n" + classification_report(y_test, y_pred))
    
    # 7. Save model and scaler
    os.makedirs(constants.MODEL_DIR, exist_ok=True)
    joblib.dump(knn, constants.MODEL_PATH)
    joblib.dump(scaler, constants.SCALER_PATH)
    logger.info(f"Model saved to {constants.MODEL_PATH}")
    logger.info(f"Scaler saved to {constants.SCALER_PATH}")

if __name__ == "__main__":
    train()
