import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import kagglehub
import os

from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import StratifiedKFold, cross_val_predict

from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)
from sklearn.preprocessing import label_binarize

pd.set_option("display.max_columns", None)
plt.style.use('seaborn') 
plt.rcParams['figure.figsize'] = (10, 6)

def get_season(month):
    if month in [12, 1, 2]:
        return 'winter'
    elif month in [3, 4, 5]:
        return 'spring'
    elif month in [6, 7, 8]:
        return 'summer'
    else:
        return 'autumn'
def outliers(column_name):    
    plt.figure(figsize=(8, 6))
    plt.boxplot(df[column_name])
    plt.title(f'Коробчатая диаграмма с выбросами {column_name}')
    plt.ylabel(column_name)
    plt.show()
def IQR_method(df,column_name):
    Q1 = df[ column_name].quantile(0.25)
    Q3 = df[ column_name].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[ column_name] >= lower_bound) & (df[column_name] <= upper_bound)]
def plot_distribution(names):
    i=0
    fig, axes = plt.subplots(1, 4, figsize=(12, 6))

    for name  in names:
        sns.histplot(df[name].to_numpy(), bins=50, ax=axes[i], color='teal', kde=False)
        axes[i].set_title(f"{name} до обработки выбросов")
        i+=1
    plt.tight_layout()
    plt.show()
def plot_confusion_matrix(y_true, y_pred, class_labels, title):
    """
    y_true, y_pred - массивы меток (числа после LabelEncoder)
    class_labels - список реальных названий классов в порядке кодирования
    """
    cm = confusion_matrix(y_true, y_pred)
    cm_df = pd.DataFrame(cm, index=class_labels, columns=class_labels)
    print(f"\nConfusion Matrix ({title}):")
    print(cm_df)
    plt.figure(figsize=(6,5))
    sns.heatmap(cm_df, annot=True, fmt='d', cmap='Blues')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.title(title)
    plt.show()


if __name__ == "__main__":

    DATASET = "ananthr1/weather-prediction"

    path = kagglehub.dataset_download(DATASET)
    print("Dataset path:", path)

    csv_path = None
    for file in os.listdir(path):
        if file.endswith(".csv"):
            csv_path = os.path.join(path, file)
            break
    if csv_path is None:
        raise FileNotFoundError("CSV not found in downloaded dataset path.")

    df = pd.read_csv(csv_path, on_bad_lines='skip')
    print("Table:")
    print(df.info() )
    print("\nMain info:")
    print(df.describe() )
    print(f"\nРазмер датасета: {df.shape}\n")
    print(df.dtypes )   
    print("\nПоиск пропусков:")
    print(df.isnull().sum())
    print(df.isnull().sum() / len(df) * 100)
    print(f"Количество дубликатов: {df.duplicated().sum()}")
    df_unique = df.drop_duplicates()
    columns=["precipitation","temp_max","temp_min","wind"]
    plot_distribution(columns)
    print("\nАнализ выбросов:")


    for key in columns:
        outliers(key)
    for key in ["temp_max","temp_min","wind"]:
        df=IQR_method(df,key)        
    print(f"\nРазмер датасета: {df.shape}\n")
    
    plot_distribution(columns)

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date']).reset_index(drop=True)
    df['month'] = df['date'].dt.month
    df['season'] = df['month'].apply(get_season)

    num_cols = ["precipitation", "temp_max", "temp_min", "wind"]
    num_cols = [c for c in num_cols if c in df.columns]



    num_present = [c for c in num_cols if c in df.columns]
    if num_present:
        scaler_tmp = StandardScaler()
        num_values = df[num_present].copy()
        num_values_scaled = scaler_tmp.fit_transform(num_values)
        imputer = KNNImputer(n_neighbors=5)
        num_imputed = imputer.fit_transform(num_values_scaled)
        num_imputed_orig = scaler_tmp.inverse_transform(num_imputed)
        df[num_present] = num_imputed_orig

    cat_cols = ['weather', 'season']
    for c in cat_cols:
        if c in df.columns:
            df[c] = df[c].fillna(df[c].mode().iloc[0])

    if 'temp_max' in df.columns and 'temp_min' in df.columns:
        df['temp_diff'] = df['temp_max'] - df['temp_min']
        df['temp_max_prev'] = df['temp_max'].shift(1)
        df['precipitation_prev'] = df['precipitation'].shift(1) if 'precipitation' in df.columns else 0
        df['temp_max_change'] = df['temp_max'] - df['temp_max_prev']
        df['temp_min_change'] = df['temp_min'] - df['temp_min'].shift(1)
        df['temp_diff_precipitation_prev'] = df['precipitation_prev'] * df['temp_diff']

    if 'weather' in df.columns:
        df['is_cloudy'] = df['weather'].str.contains('fog|drizzle|rain|cloud', case=False, na=False).astype(int)
        df['is_clear'] = df['weather'].str.contains('sun|clear', case=False, na=False).astype(int)

    df = df.dropna().reset_index(drop=True)
    print("Table:")
    print(df.info() )
    print("\nMain info:")
    print(df.describe() )
    if 'weather' not in df.columns:
        raise ValueError("В датасете нет колонки 'weather' — невозможно классифицировать по погоде.")
    le_weather = LabelEncoder()
    y = le_weather.fit_transform(df['weather'])
    class_labels = list(le_weather.classes_)
    print("Weather classes:", class_labels)

    drop_cols = ['date', 'weather']

    X = df.drop(columns=drop_cols, errors='ignore')
    for col in X.select_dtypes(include=['object', 'category']).columns:
        X[col] = LabelEncoder().fit_transform(X[col].astype(str))

    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns, index=X.index)

    models = {
        "DecisionTree": DecisionTreeClassifier(random_state=42),
        "KNeighbors": KNeighborsClassifier(n_neighbors=5),
        "LogisticRegression": LogisticRegression(max_iter=1000, solver='lbfgs', multi_class='auto'),
        "GaussianNB": GaussianNB()
    }

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    results = []
    y_binarized = label_binarize(y, classes=np.arange(len(class_labels)))
    n_classes = y_binarized.shape[1]

    for name, model in models.items():
        print(f"\nTraining & evaluating {name} ...")

        y_pred = cross_val_predict(model, X_scaled, y, cv=skf, method='predict', n_jobs=-1)

        try:
            y_proba = cross_val_predict(model, X_scaled, y, cv=skf, method='predict_proba', n_jobs=-1)
            if n_classes == 2:
                roc_auc = roc_auc_score(y, y_proba[:, 1])
            else:
                roc_auc = roc_auc_score(y_binarized, y_proba, average='macro', multi_class='ovr')
        except Exception as e:
            print(f"Warning: модель {name} не поддерживает predict_proba через cross_val_predict: {e}")
            try:
                model.fit(X_scaled, y)
                if hasattr(model, "predict_proba"):
                    proba_full = model.predict_proba(X_scaled)
                    if n_classes == 2:
                        roc_auc = roc_auc_score(y, proba_full[:, 1])
                    else:
                        roc_auc = roc_auc_score(y_binarized, proba_full, average='macro', multi_class='ovr')
                else:
                    roc_auc = np.nan
            except Exception:
                roc_auc = np.nan

        acc = accuracy_score(y, y_pred)
        prec = precision_score(y, y_pred, average='macro', zero_division=0)
        rec = recall_score(y, y_pred, average='macro', zero_division=0)
        f1 = f1_score(y, y_pred, average='macro', zero_division=0)

        results.append({
            "Model": name,
            "Accuracy": acc,
            "Precision_macro": prec,
            "Recall_macro": rec,
            "F1_macro": f1,
            "ROC_AUC_macro": roc_auc
        })

        # Confusion matrix и classification report
        print(f"Classification report for {name}:\n")
        print(classification_report(y, y_pred, target_names=class_labels, zero_division=0))
        plot_confusion_matrix(y, y_pred, class_labels=class_labels, title=f"Confusion Matrix: {name}")
 
        print("Label mapping (index -> label):")
        for idx, lab in enumerate(class_labels):
            print(f"{idx} -> {lab}")

    results_df = pd.DataFrame(results).sort_values(by='F1_macro', ascending=False)
    print("\nСводная таблица результатов (по убыванию F1_macro):")
    print(results_df)

  
    plt.figure(figsize=(10,6))
    metrics_plot = results_df.set_index('Model')[['Accuracy','Precision_macro','Recall_macro','F1_macro','ROC_AUC_macro']]
    sns.heatmap(metrics_plot, annot=True, fmt=".3f", cmap='YlGnBu', cbar_kws={'label': 'score'})
    plt.title("Сравнение моделей по метрикам (кросс-валидация)")
    plt.show()