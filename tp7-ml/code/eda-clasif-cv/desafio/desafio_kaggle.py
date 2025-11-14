
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.metrics import confusion_matrix
import os

# Crear carpetas (si no existen)
os.makedirs("data", exist_ok=True)
os.makedirs("output", exist_ok=True)


# 1. Cargar datos

train = pd.read_csv("data/arbolado-mendoza-dataset-train.csv")
test = pd.read_csv("data/arbolado-mendoza-dataset-test.csv")

test_ids = test["id"].copy()


# Preprocesamiento


# Columnas que NO sirven
drop_cols = ["id", "nombre_seccion", "ultima_modificacion"]
train = train.drop(columns=drop_cols)
test = test.drop(columns=drop_cols)


altura_map = {
    "Muy bajo (1 - 2 mts)": 1.5,
    "Bajo (2 - 4 mts)": 3,
    "Medio (4 - 8 mts)": 6,
    "Alto (> 8 mts)": 9
}

diam_map = {
    "Muy bajo (< 20 cm)": 10,
    "Bajo (20 - 40 cm)": 30,
    "Medio (40 - 60 cm)": 50,
    "Alto (> 60 cm)": 70
}

for df in [train, test]:
    df["altura"] = df["altura"].map(altura_map)
    df["diametro_tronco"] = df["diametro_tronco"].map(diam_map)


cat_cols = ["especie", "seccion"]

for col in cat_cols:
    le = LabelEncoder()
    train[col] = le.fit_transform(train[col].astype(str))

    # preparar clases extendidas para test
    le_classes = np.append(le.classes_, "NA")
    le.classes_ = le_classes

    test[col] = test[col].map(lambda x: x if x in le.classes_ else "NA")
    test[col] = le.transform(test[col].astype(str))


train["circ_altura_ratio"] = train["circ_tronco_cm"] / (train["altura"] + 0.01)
test["circ_altura_ratio"] = test["circ_tronco_cm"] / (test["altura"] + 0.01)

train["diam_circ_ratio"] = train["diametro_tronco"] / (train["circ_tronco_cm"] + 0.01)
test["diam_circ_ratio"] = test["diametro_tronco"] / (test["circ_tronco_cm"] + 0.01)


# Separar X e y

y = train["inclinacion_peligrosa"]
X = train.drop(columns=["inclinacion_peligrosa"])


# Stratified K-Fold

kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

acc_scores = []
auc_scores = []

for fold, (train_idx, val_idx) in enumerate(kf.split(X, y), 1):
    X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
    y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

    model = DecisionTreeClassifier(
        max_depth=6,
        min_samples_split=20,
        class_weight="balanced",
        random_state=42
    )

    model.fit(X_train, y_train)
    preds = model.predict(X_val)
    preds_prob = model.predict_proba(X_val)[:, 1]

    acc = accuracy_score(y_val, preds)
    auc = roc_auc_score(y_val, preds_prob)

    acc_scores.append(acc)
    auc_scores.append(auc)

    print(f"Fold {fold}  |  ACC={acc:.4f}  |  AUC={auc:.4f}")

print("\n===============================================")
print(f"Mean ACC: {np.mean(acc_scores):.4f} ± {np.std(acc_scores):.4f}")
print(f"Mean AUC: {np.mean(auc_scores):.4f} ± {np.std(auc_scores):.4f}")
print("===============================================\n")


# Entrenar modelo 

final_model = DecisionTreeClassifier(
    max_depth=6,
    min_samples_split=20,
    class_weight="balanced",
    random_state=42
)

final_model.fit(X, y)

# Predicciones finales

test_pred_prob = final_model.predict_proba(test)[:, 1]
test_pred_class = (test_pred_prob >= 0.5).astype(int)

submission = pd.DataFrame({
    "ID": test_ids,
    "inclinacion_peligrosa": test_pred_class
})

submission.to_csv("output/submission.csv", index=False)
print("\nArchivo generado: output/submission.csv")
