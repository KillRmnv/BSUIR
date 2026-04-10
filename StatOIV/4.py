import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import kagglehub
import os

from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import make_pipeline

from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
from scipy.cluster.hierarchy import dendrogram, linkage
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
plt.style.use('seaborn-v0_8')
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
        sns.histplot(df[name], bins=50, ax=axes[i], color='teal', kde=True)
        axes[i].set_title(f"{name} до обработки выбросов")
        i+=1
    plt.tight_layout()
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
    for key in ["temp_max","temp_min","wind","precipitation"]:
        df=IQR_method(df,key)     
        df = df.reset_index(drop=True)
   
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
    

    print("\n--- 4. Применение PCA ---")
    
    pca = PCA(n_components=0.90) 
    X_pca_array = pca.fit_transform(X_scaled)
    
    n_components = X_pca_array.shape[1]
    X_to_cluster = pd.DataFrame(X_pca_array, 
                                columns=[f'PC_{i+1}' for i in range(n_components)], 
                                index=X_scaled.index)
    
    print(f"Количество компонент: {n_components}")
    print(f"Объясненная дисперсия: {pca.explained_variance_ratio_.sum():.3f}")

    results_table = []


    print("\n--- 1. KMeans ---")
    
    # А) Метод локтя (Elbow Method) для поиска оптимального количества кластеров
    inertia = []
    k_range = range(2, 11) 

    for k in k_range:
        kmeans_temp = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans_temp.fit(X_to_cluster) 
        inertia.append(kmeans_temp.inertia_)

    plt.figure(figsize=(8, 5))
    plt.plot(k_range, inertia, marker='o')
    plt.title('Метод локтя (KMeans)')
    plt.xlabel('Количество кластеров')
    plt.ylabel('Inertia (сумма квадратов расстояний)')
    plt.show()
    
    # Б) Обучаем финальную модель
    optimal_k = 5 
    print(f"Выбрано количество кластеров: {optimal_k}")
    
    model_kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    labels_kmeans = model_kmeans.fit_predict(X_to_cluster) 


    print("\n--- 2. Agglomerative Clustering ---")

    # А) Дендрограмма
    plt.figure(figsize=(10, 7))
    plt.title("Дендрограмма")
    linked = linkage(X_to_cluster, method='ward')
    dendrogram(linked, truncate_mode='lastp', p=30) 
    plt.show()

    # Б) Обучение модели
    optimal_k_agglo = 5
    model_agglo = AgglomerativeClustering(n_clusters=optimal_k_agglo, linkage='ward')
    labels_agglo = model_agglo.fit_predict(X_to_cluster) 


    print("\n--- 3. DBSCAN ---")

    # А) График k-расстояний (k-distance graph) для выбора eps
    k_neighbors_for_eps = 10 
    neigh = NearestNeighbors(n_neighbors=k_neighbors_for_eps)
    nbrs = neigh.fit(X_to_cluster) # ИСПОЛЬЗУЕМ X_to_cluster
    distances, indices = nbrs.kneighbors(X_to_cluster) # ИСПОЛЬЗУЕМ X_to_cluster
    
    distances = np.sort(distances[:, k_neighbors_for_eps - 1], axis=0) 
    
    plt.figure(figsize=(8, 5))
    plt.plot(distances)
    plt.title(f"K-distance Graph (k={k_neighbors_for_eps}) для выбора eps")
    plt.ylabel("Eps (расстояние)")
    plt.xlabel("Точки (отсортированные)")
    plt.show()

    # Б) Обучение DBSCAN
    eps_val = 1.48  
    min_samples_val = k_neighbors_for_eps 
    
    model_dbscan = DBSCAN(eps=eps_val, min_samples=min_samples_val)
    labels_dbscan = model_dbscan.fit_predict(X_to_cluster) # ИСПОЛЬЗУЕМ X_to_cluster

    print(f"Параметры DBSCAN: eps={eps_val}, min_samples={min_samples_val}")

    

    def evaluate_clustering(name, labels, data_x, true_labels):
        unique_labels = set(labels)
        n_clusters = len(unique_labels) - (1 if -1 in labels else 0)
        n_noise = list(labels).count(-1)
        
        print(f"\n>>> Оценка: {name}")
        print(f"Найдено кластеров: {n_clusters}")
        print(f"Выбросов (шум): {n_noise} ({n_noise/len(labels)*100:.2f}%)")

        if n_clusters < 2:
            print("Слишком мало кластеров для оценки метрик.")
            return {
                "Алгоритм": name, 
                "Кластеров": n_clusters,
                "Silhouette": np.nan, "Davies-Bouldin": np.nan, "Calinski-Harabasz": np.nan,
                "ARI": np.nan, "NMI": np.nan
            }

        if -1 in labels:
            mask = labels != -1
            data_for_metric = data_x.values[mask] 
            labels_for_metric = labels[mask]
        else:
            data_for_metric = data_x.values
            labels_for_metric = labels

        sil = silhouette_score(data_for_metric, labels_for_metric)
        db = davies_bouldin_score(data_for_metric, labels_for_metric)
        ch = calinski_harabasz_score(data_for_metric, labels_for_metric)
        

        ari = adjusted_rand_score(true_labels, labels)
        nmi = normalized_mutual_info_score(true_labels, labels)

        print(f"Silhouette: {sil:.3f}")
        print(f"Davies-Bouldin: {db:.3f}")
        print(f"ARI: {ari:.3f}")

        return {
            "Алгоритм": name,
            "Кластеров": n_clusters,
            "Silhouette": round(sil, 3),
            "Davies-Bouldin": round(db, 3),
            "Calinski-Harabasz": round(ch, 3),
            "ARI": round(ari, 3),
            "NMI": round(nmi, 3)
        }

    res_km = evaluate_clustering("KMeans", labels_kmeans, X_to_cluster, y) 
    results_table.append(res_km)

    res_agg = evaluate_clustering("Agglomerative", labels_agglo, X_to_cluster, y) 
    results_table.append(res_agg)

    res_db = evaluate_clustering("DBSCAN", labels_dbscan, X_to_cluster, y)
    results_table.append(res_db)


    print("\n" + "="*50)
    print("ЧАСТЬ 5. ВИЗУАЛИЗАЦИЯ")
    print("="*50)

    def plot_clusters(model_name, labels):

        X_2d = X_to_cluster[['PC_1', 'PC_2']].values 
        
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=X_2d[:, 0], y=X_2d[:, 1], hue=labels, palette='viridis', s=50)
        plt.title(f"{model_name}: PCA проекция (2D) PC1 vs PC2")
        plt.xlabel("PCA Component 1")
        plt.ylabel("PCA Component 2")
        plt.legend(title="Cluster")
        plt.show()

        plt.figure(figsize=(6, 4))
        sns.countplot(x=labels, palette='viridis')
        plt.title(f"{model_name}: Размер кластеров")
        plt.xlabel("Номер кластера")
        plt.ylabel("Количество точек")
        plt.show()

        temp_df = X_to_cluster.copy() 
        temp_df['Cluster'] = labels
        


    print("Визуализация для KMeans...")
    plot_clusters("KMeans", labels_kmeans)
    
    plot_clusters("Agglomerative", labels_agglo)
    plot_clusters("DBSCAN", labels_dbscan)

    print("\n" + "="*50)
    print("ИТОГОВАЯ ТАБЛИЦА РЕЗУЛЬТАТОВ")
    print("="*50)
    
    df_results = pd.DataFrame(results_table)
    print(df_results)
    
