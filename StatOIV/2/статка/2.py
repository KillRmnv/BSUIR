import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import kagglehub
import os
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder, MultiLabelBinarizer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import KFold, cross_validate
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold, cross_validate
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

plt.style.use('seaborn')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12
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
def KNN(df, columns):
    features = df[columns]

    scaler = StandardScaler()
    standardized = scaler.fit_transform(features)

    imputer = KNNImputer(n_neighbors=5)
    imputed = imputer.fit_transform(standardized)

    imputed_original_scale = scaler.inverse_transform(imputed)

    df[columns] = imputed_original_scale

    return df
def fill_gaps_with_most_frequent(names):
    # Заполнение наиболее частым значением
    imputer_freq = SimpleImputer(strategy="most_frequent")
    for name in names:
        df[f"{name}_filled_freq"] = imputer_freq.fit_transform(df[[name]])  
def fill_gaps_with_missing(names):
    imputer_const = SimpleImputer(strategy="constant", fill_value="missing")
    for name in names:
        df[f"{name}_filled_freq"] = imputer_const.fit_transform(df[[name]])
def one_hot(df, columns):
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    encoded = encoder.fit_transform(df[columns])

    encoded_df = pd.DataFrame(
        encoded,
        columns=encoder.get_feature_names_out(columns),
        index=df.index
    )

    # Убираем оригинальные категориальные колонки
    df = pd.concat([df.drop(columns=columns), encoded_df], axis=1)
    return df
def get_season(month):
    if month in [12, 1, 2]:
        return 'winter'
    elif month in [3, 4, 5]:
        return 'spring'
    elif month in [6, 7, 8]:
        return 'summer'
    else:
        return 'autumn'      
def evaluate_models(X, y):
    models = {
        "LinearRegression": make_pipeline(StandardScaler(), LinearRegression()),
        "PolynomialRegression (deg=2)": make_pipeline(StandardScaler(), PolynomialFeatures(degree=2), LinearRegression()),
        "PolynomialRegression (deg=3)": make_pipeline(StandardScaler(), PolynomialFeatures(degree=3), LinearRegression()),
        "Ridge": make_pipeline(StandardScaler(), Ridge(alpha=1.0)),
        "Lasso": make_pipeline(StandardScaler(), Lasso(alpha=0.01)),
        "RandomForest": RandomForestRegressor(n_estimators=100, random_state=42),
        "GradientBoosting": GradientBoostingRegressor(n_estimators=100, random_state=42)
    }

    cv = KFold(n_splits=5, shuffle=True, random_state=42)

    results = []

    for name, model in models.items():
        cv_results = cross_validate(
            model, X, y, cv=cv,
            scoring=['neg_mean_absolute_error', 'neg_root_mean_squared_error', 'r2'],
            n_jobs=-1
        )

        results.append({
            "Модель": name,
            "MAE": -cv_results['test_neg_mean_absolute_error'].mean(),
            "RMSE": -cv_results['test_neg_root_mean_squared_error'].mean(),
            "R²": cv_results['test_r2'].mean()
        })

    results_df = pd.DataFrame(results).sort_values(by="R²", ascending=False)
    return results_df    
def influention(names):
    for name in names:
            # === ВАЖНОСТЬ ПРИЗНАКОВ ===
        best_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        best_model.fit(X, df[name])  # пример для temp_max, можно выбрать другую целевую переменную

        importances = pd.Series(best_model.feature_importances_, index=X.columns).sort_values(ascending=False)

        plt.figure(figsize=(10, 6))
        sns.barplot(x=importances.values, y=importances.index, palette="viridis")
        plt.title(f"Важность признаков для предсказания {name} (GradientBoosting)")
        plt.xlabel("Важность признака")
        plt.ylabel("Признак")
        plt.tight_layout()
        plt.show()
if __name__=="__main__":

    DATASET = "ananthr1/weather-prediction"

    path = kagglehub.dataset_download(DATASET)
    print("Dataset path:", path)

    for file in os.listdir(path):
        if file.endswith(".csv"):
            csv_path = os.path.join(path, file)
            print("CSV file found:", csv_path)
            break

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
    
    df['date'] = pd.to_datetime(df['date'])

    # Добавим колонку с месяцем
    df['month'] = df['date'].dt.month
    df['season'] = df['month'].apply(get_season)
    print("Table:")
    print(df.info() )
    print(df.head())
    
    scaler = StandardScaler()
    
    df[columns] = scaler.fit_transform(df[columns])
    print(df['weather'].value_counts(normalize=True))
    df=one_hot(df,["weather","season"])
    df['temp_diff'] = df['temp_max'] - df['temp_min']
    df['temp_max_prev'] = df['temp_max'].shift(1)
    df['precipitation_prev'] = df['precipitation'].shift(1)
    df['temp_diff_precipitation_prev']=df['precipitation_prev']*df['temp_diff']
    df['temp_max_change'] = df['temp_max'] - df['temp_max_prev']
    df['temp_min_change'] = df['temp_min'] - df['temp_min'].shift(1)

    df['is_cloudy'] = (df['weather_fog'] + df['weather_drizzle'] + df['weather_rain']).clip(0, 1)
    df['is_clear'] = df['weather_sun']

    print("Table:")
    print(df.info() )
    print(df.head())
    df = df.dropna().reset_index(drop=True)
    X = df.drop(columns=['date', 'temp_max', 'temp_min', 'precipitation', 'wind'])
    
    all_results = [] 

    for weather in ["temp_max", "temp_min", "precipitation", "wind"]:
        y = df[weather]

        results_df = evaluate_models(X, y)
        results_df["Целевая переменная"] = weather  
        all_results.append(results_df)

    final_results = pd.concat(all_results, ignore_index=True)

    final_results = final_results.sort_values(by=["Целевая переменная", "R²"], ascending=[True, False])

    
    influention(["temp_max", "temp_min", "precipitation", "wind"])
    

    print("\n Итоговое сравнение всех моделей по всем целевым переменным:\n")
    print(final_results)

    metrics_to_plot = ["MAE", "RMSE", "R²"]
    cmap = "YlGnBu"

    fig, axes = plt.subplots(1, len(metrics_to_plot), figsize=(18, 6))

    for i, metric in enumerate(metrics_to_plot):
        pivot = final_results.pivot_table(
            index="Модель",
            columns="Целевая переменная",
            values=metric
        )

        if metric in ["MAE", "RMSE"]:
            sns.heatmap(pivot, annot=True, cmap=cmap, fmt=".3f", ax=axes[i], cbar_kws={'label': metric})
        else:
            sns.heatmap(pivot, annot=True, cmap=cmap, fmt=".3f", ax=axes[i], cbar_kws={'label': metric})

        axes[i].set_title(f"Метрика: {metric}")
        axes[i].set_xlabel("Целевая переменная")
        axes[i].set_ylabel("Модель")

    plt.suptitle("Сравнение моделей по метрикам (MAE, RMSE, R²)", fontsize=14, y=1.05)
    plt.tight_layout()
    plt.show()