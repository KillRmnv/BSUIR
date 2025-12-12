Отчет по анализу данных о погоде
1. Импорт необходимых библиотек
Для выполнения анализа данных, визуализации и построения моделей машинного обучения импортируем следующие библиотеки:

pandas и numpy — для работы с данными.
matplotlib и seaborn — для визуализации.
sklearn — для обработки данных и обучения моделей.
kagglehub — для загрузки датасета.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import kagglehub
import os
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, MultiLabelBinarizer, PolynomialFeatures
from sklearn.model_selection import KFold, cross_validate
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

2. Настройка отображения и стилей
Настраиваем параметры отображения таблиц и графиков для улучшения читаемости и визуального восприятия:
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12

Комментарий: Эти настройки обеспечивают удобный вывод таблиц и единообразный стиль графиков.
3. Вспомогательные функции для анализа данных
Определяем функции для выполнения следующих задач:

Визуализация выбросов с помощью коробчатых диаграмм.
Удаление выбросов методом межквартильного размаха (IQR).
Построение распределений признаков.
Заполнение пропусков в данных.
Кодирование категориальных переменных.
Оценка качества моделей.

def plot_outliers(column_name, df):
    plt.figure(figsize=(8, 6))
    plt.boxplot(df[column_name])
    plt.title(f'Коробчатая диаграмма для {column_name}')
    plt.ylabel(column_name)
    plt.show()

def iqr_method(df, column_name):
    Q1 = df[column_name].quantile(0.25)
    Q3 = df[column_name].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column_name] >= lower_bound) & (df[column_name] <= upper_bound)]

Комментарий: Эти функции позволяют автоматизировать анализ данных и подготовку к моделированию.
4. Загрузка и предварительный анализ данных
Скачиваем датасет о погоде с Kaggle и проводим его предварительный анализ:
DATASET = "ananthr1/weather-prediction"
path = kagglehub.dataset_download(DATASET)
print("Путь к датасету:", path)

for file in os.listdir(path):
    if file.endswith(".csv"):
        csv_path = os.path.join(path, file)
        print("Найден CSV файл:", csv_path)
        break

df = pd.read_csv(csv_path, on_bad_lines='skip')
print("Информация о датасете:")
print(df.info())
print("\nОписательная статистика:")
print(df.describe())
print(f"\nРазмер датасета: {df.shape}\n")
print("Типы данных:\n", df.dtypes)
print("\nПропуски в данных:")
print(df.isnull().sum())
print("\nДоля пропусков (%):")
print(df.isnull().sum() / len(df) * 100)
print(f"\nКоличество дубликатов: {df.duplicated().sum()}")

Вывод:

Путь к датасету: /home/kirillromanoff/.cache/kagglehub/datasets/ananthr1/weather-prediction/versions/1
Найден CSV файл: /home/kirillromanoff/.cache/kagglehub/datasets/ananthr1/weather-prediction/versions/1/seattle-weather.csv
Информация о датасете:<class 'pandas.core.frame.DataFrame'>
RangeIndex: 1461 entries, 0 to 1460
Data columns (total 6 columns):
 #   Column         Non-Null Count  Dtype
---  ------         --------------  -----
 0   date           1461 non-null   object
 1   precipitation  1461 non-null   float64
 2   temp_max       1461 non-null   float64
 3   temp_min       1461 non-null   float64
 4   wind           1461 non-null   float64
 5   weather        1461 non-null   object
dtypes: float64(4), object(2)
memory usage: 68.6+ KB


Описательная статистика:       precipitation     temp_max     temp_min         wind
count    1461.000000  1461.000000  1461.000000  1461.000000
mean        3.029432    16.439083     8.234771     3.241136
std         6.680194     7.349758     5.023004     1.437825
min         0.000000    -1.600000    -7.100000     0.400000
25%         0.000000    10.600000     4.400000     2.200000
50%         0.000000    15.600000     8.300000     3.000000
75%         2.800000    22.200000    12.200000     4.000000
max        55.900000    35.600000    18.300000     9.500000


Размер датасета: (1461, 6)
Типы данных:date             object
precipitation    float64
temp_max         float64
temp_min         float64
wind             float64
weather          object
dtype: object


Пропуски в данных: Отсутствуют.
Доля пропусков (%): 0% для всех столбцов.
Количество дубликатов: 0.

5. Анализ выбросов
Проводим анализ выбросов для числовых признаков (precipitation, temp_max, temp_min, wind):
columns = ["precipitation", "temp_max", "temp_min", "wind"]
def plot_distribution(columns, df):
    for col in columns:
        plt.figure(figsize=(8, 6))
        sns.histplot(df[col], kde=True)
        plt.title(f'Распределение {col}')
        plt.show()

plot_distribution(columns, df)
print("\nАнализ выбросов:")
for key in columns:
    plot_outliers(key, df)
for key in ["temp_max", "temp_min", "wind"]:
    df = iqr_method(df, key)
print(f"\nРазмер датасета после удаления выбросов: {df.shape}\n")

Комментарий: Удаление выбросов методом IQR позволяет очистить данные для повышения качества моделей.
6. Обработка дат и создание новых признаков
Преобразуем столбец date в формат datetime и добавляем новые признаки: месяц и сезон.
def get_season(month):
    if month in [12, 1, 2]:
        return 'winter'
    elif month in [3, 4, 5]:
        return 'spring'
    elif month in [6, 7, 8]:
        return 'summer'
    else:
        return 'autumn'

df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month
df['season'] = df['month'].apply(get_season)
print("Информация о датасете:")
print(df.info())
print("\nПервые строки датасета:")
print(df.head())

Вывод:

Информация о датасете:<class 'pandas.core.frame.DataFrame'>
Index: 1427 entries, 0 to 1460
Data columns (total 8 columns):
 #   Column         Non-Null Count  Dtype
---  ------         --------------  -----
 0   date           1427 non-null   datetime64[ns]
 1   precipitation  1427 non-null   float64
 2   temp_max       1427 non-null   float64
 3   temp_min       1427 non-null   float64
 4   wind           1427 non-null   float64
 5   weather        1427 non-null   object
 6   month          1427 non-null   int32
 7   season         1427 non-null   object
dtypes: datetime64[ns](1), float64(4), int32(1), object(2)
memory usage: 94.8+ KB


Первые строки датасета:        date  precipitation  temp_max  temp_min  wind  weather  month  season
0 2012-01-01            0.0      12.8       5.0   4.7  drizzle      1  winter
1 2012-01-02           10.9      10.6       2.8   4.5     rain      1  winter
2 2012-01-03            0.8      11.7       7.2   2.3     rain      1  winter
3 2012-01-04           20.3      12.2       5.6   4.7     rain      1  winter
4 2012-01-05            1.3       8.9       2.8   6.1     rain      1  winter



7. Масштабирование и кодирование признаков
Нормализуем числовые признаки и кодируем категориальные переменные с помощью One-Hot Encoding:
scaler = StandardScaler()
df[columns] = scaler.fit_transform(df[columns])

def one_hot(df, columns):
    encoder = OneHotEncoder(sparse_output=False, drop='first')
    encoded = encoder.fit_transform(df[columns])
    encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(columns))
    return pd.concat([df.drop(columns, axis=1).reset_index(drop=True), encoded_df], axis=1)

print("Распределение погодных условий:")
print(df['weather'].value_counts(normalize=True))
df = one_hot(df, ["weather", "season"])

Вывод:

Распределение погодных условий:weather
sun        0.444989
rain       0.429573
fog        0.070778
drizzle    0.037141
snow       0.017519
Name: proportion, dtype: float64



8. Генерация новых признаков
Создаем дополнительные признаки для улучшения качества моделей:
df['temp_diff'] = df['temp_max'] - df['temp_min']
df['temp_max_prev'] = df['temp_max'].shift(1)
df['precipitation_prev'] = df['precipitation'].shift(1)
df['avg_temperature'] = (df["temp_max"] + df["temp_min"]) / 2
df['temp_precipitation'] = df["precipitation"] * df['avg_temperature']
df['temp_diff_precipitation_prev'] = df['precipitation_prev'] * df['temp_diff']
df['temp_max_change'] = df['temp_max'] - df['temp_max_prev']
df['temp_min_change'] = df['temp_min'] - df['temp_min'].shift(1)
df['avg_temp_change'] = df['avg_temperature'] - df['avg_temperature'].shift(1)
df['precipitation_change'] = df['precipitation'] - df['precipitation_prev']
df['is_cloudy'] = (df['weather_fog'] + df['weather_drizzle'] + df['weather_rain']).clip(0, 1)
df['is_clear'] = df['weather_sun']
df['temp_precip_change'] = df['precipitation_change'] * df['avg_temperature']
df['tempdiff_precip_change'] = df['temp_diff'] * df['precipitation_change']

print("Информация о датасете:")
print(df.info())
print("\nПервые строки датасета:")
print(df.head())

Вывод:

Информация о датасете:<class 'pandas.core.frame.DataFrame'>
RangeIndex: 1427 entries, 0 to 1426
Data columns (total 29 columns):
 #   Column                        Non-Null Count  Dtype
---  ------                        --------------  -----
 0   date                          1427 non-null   datetime64[ns]
 1   precipitation                 1427 non-null   float64
 2   temp_max                      1427 non-null   float64
 3   temp_min                      1427 non-null   float64
 4   wind                          142


