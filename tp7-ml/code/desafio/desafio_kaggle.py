import os
import pandas as pd
import numpy as np
import xgboost as xgb


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

train_path = os.path.join(DATA_DIR, "arbolado-mza-dataset.csv")
test_path = os.path.join(DATA_DIR, "arbolado-mza-dataset-test.csv")

train = pd.read_csv(train_path)
test = pd.read_csv(test_path)

# PREPROCESAMIENTO

# Eliminar columnas irrelevantes
drop_cols = ["id", "nombre_seccion", "ultima_modificacion"]
train = train.drop(columns=drop_cols)
test = test.drop(columns=drop_cols)

# ---- Mapeos ----
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

for df in (train, test):
    df["altura"] = df["altura"].map(altura_map)
    df["diametro_tronco"] = df["diametro_tronco"].map(diam_map)

# ---- Encoding manual ----
def encode(train_col, test_col):
    uniq = sorted(train_col.fillna("").unique())
    mapping = {v: i for i, v in enumerate(uniq)}

    train_enc = train_col.map(lambda x: mapping.get(x, -1))
    test_enc  = test_col.map(lambda x: mapping.get(x, -1))

    return train_enc, test_enc

for col in ["especie", "seccion"]:
    train[col], test[col] = encode(train[col], test[col])


train["circ_altura_ratio"] = train["circ_tronco_cm"] / (train["altura"] + 0.01)
test["circ_altura_ratio"]  = test["circ_tronco_cm"] / (test["altura"] + 0.01)

train["diam_circ_ratio"] = train["diametro_tronco"] / (train["circ_tronco_cm"] + 0.01)
test["diam_circ_ratio"]  = test["diametro_tronco"] / (test["circ_tronco_cm"] + 0.01)

# SEPARAR X E Y
y = train["inclinacion_peligrosa"].values
X = train.drop(columns=["inclinacion_peligrosa"])

# K-FOLD
def stratified_folds(y, k=5):
    idx0 = np.where(y == 0)[0]
    idx1 = np.where(y == 1)[0]

    np.random.shuffle(idx0)
    np.random.shuffle(idx1)

    folds0 = np.array_split(idx0, k)
    folds1 = np.array_split(idx1, k)

    return [np.concatenate([folds0[i], folds1[i]]) for i in range(k)]

folds = stratified_folds(y, 5)


# ENTRENAMIENTO CON BALANCE CORRECTO

pos = (y == 1).sum()
neg = (y == 0).sum()
scale = neg / pos  # <---- CLAVE

params = {
    "objective": "binary:logistic",
    "eta": 0.03,
    "max_depth": 5,
    "subsample": 0.9,
    "colsample_bytree": 0.9,
    "scale_pos_weight": scale,
    "eval_metric": "logloss"
}

auc_list = []

for i in range(5):
    val_idx = folds[i]
    train_idx = np.concatenate([folds[j] for j in range(5) if j != i])

    dtrain = xgb.DMatrix(X.iloc[train_idx], label=y[train_idx])
    dval   = xgb.DMatrix(X.iloc[val_idx],   label=y[val_idx])

    model = xgb.train(
        params,
        dtrain,
        num_boost_round=800,
        evals=[(dval, "val")],
        verbose_eval=False
    )

    pred = model.predict(dval)
    # AUC manual
    order = np.argsort(pred)
    y_sorted = y[val_idx][order]
    auc = (np.cumsum(y_sorted) / y_sorted.sum()).mean()
    auc_list.append(auc)

print("AUC promedio K-Fold:", np.mean(auc_list))

# ENTRENAMIENTO FINAL

dtrain_full = xgb.DMatrix(X, label=y)
dtest = xgb.DMatrix(test)

final_model = xgb.train(
    params,
    dtrain_full,
    num_boost_round=800
)

# PREDICCIÓN 

pred_prob = final_model.predict(dtest)
pred = (pred_prob >= 0.45).astype(int)   # threshold más sensible

submission = pd.DataFrame({
    "ID": pd.read_csv(test_path)["id"],
    "inclinacion_peligrosa": pred
})

OUT = os.path.join(BASE_DIR, "..", "output", "submission.csv")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

submission.to_csv(OUT, index=False)

print("\n✔ Submission generado en:", OUT)
