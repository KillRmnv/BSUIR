import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

plt.style.use('seaborn-v0_8')
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
    
def linear_plot(df, column_x, column_y):
    plt.figure(figsize=(10, 6))
    sns.regplot(x=column_x, y=column_y, data=df, scatter_kws={'s': 50}, line_kws={'color': 'red'})
    plt.xlabel(column_x)
    plt.ylabel(column_y)
    plt.title(f'Корреляционная прямая: {column_x} vs {column_y}')
    plt.grid(True)
    plt.show()
def find_correlation(df, column_x, column_y):

    linear_plot(df, column_x, column_y)

    corr_coef, p_value = pearsonr(df[column_x], df[column_y])
    print(f"Коэффициент корреляции для {column_x} к {column_y}: {corr_coef}\np-value: {p_value}")
            
if __name__=="__main__":
    df = pd.read_csv('student_habits_performance.csv')
    print((df[df['gender']=='Other']))
        
    
    print("Table:")
    print(df.info() )
    print("\nMain info:")
    print(df.describe() )
    print("\nHeader:")
    print(df.head() )
    print(f"\nРазмер датасета: {df.shape}\n")
    print(df.dtypes )   
    print("\nПоиск пропусков:")
    print(df.isnull().sum())
    print(df.isnull().sum() / len(df) * 100)
    df['parental_education_level'] = df['parental_education_level'].fillna('absence')
    print(f"Количество дубликатов: {df.duplicated().sum()}")
    df_unique = df.drop_duplicates()
    print("\nАнализ выбросов:")
    
    outliers('age')
    outliers('study_hours_per_day')
    outliers('social_media_hours')
    outliers('netflix_hours')
    outliers('attendance_percentage')
    outliers('sleep_hours')
    outliers('exercise_frequency') 
    outliers('mental_health_rating') 
    outliers('exam_score') 
    
    df=IQR_method(df,'age')
    df=IQR_method(df,'study_hours_per_day')
    df=IQR_method(df,'social_media_hours')
    df=IQR_method(df,'netflix_hours')
    df=IQR_method(df,'attendance_percentage')
    df=IQR_method(df,'sleep_hours')
    df=IQR_method(df,'exercise_frequency') 
    df=IQR_method(df,'mental_health_rating') 
    df=IQR_method(df,'exam_score') 
    print(f"\nРазмер датасета: {df.shape}\n")
    # 1.Зависимость между количеством сна и посещаемостью
    find_correlation(df,'sleep_hours','attendance_percentage')
    # 2.Зависимость между количеством часов учебы и ментальным здоровьем
    find_correlation(df,'study_hours_per_day','mental_health_rating')
    # 4.Зависимость между посещаемостью и успеваемостью
    find_correlation(df,'attendance_percentage','exam_score')
    # 5.Зависимость между временем затраченным на учебу и успеваемостью
    find_correlation(df,'study_hours_per_day','exam_score')
    # 8.Cвязь между exercise_frequency и mental_health_rating
    find_correlation(df,'exercise_frequency','mental_health_rating')
    # 10.Социальные сети и сон
    find_correlation(df,'social_media_hours','sleep_hours')
    # 3.Зависимость между успеваемостью студента и степенью образования родителей
    group_stats = df.groupby('parental_education_level').agg({
    'exam_score': 'mean',
    'attendance_percentage': 'mean'
})
    print(group_stats)
    
    sns.barplot(x='parental_education_level', y='exam_score', data=group_stats)
    plt.xlabel('Уровень образования родителей')
    plt.ylabel('Средний балл экзамена')
    plt.title('Средний балл экзамена по уровню образования родителей')
    plt.xticks(rotation=45)##поворот подписей по оси х на 45 градцсов
    plt.show()
    
    
    # 6.Успеваемость и гендер
    group_stats = df.groupby('gender').agg({
    'exam_score': 'mean',
    'attendance_percentage': 'mean'
})
    print(group_stats)
    group_stats['exam_score'].plot(kind='bar', color='skyblue')
    plt.xlabel('Гендер')
    plt.ylabel('Средний балл экзамена')
    plt.title('Средний балл экзамена по гендеру')
    plt.xticks(rotation=45)
    plt.show()
    
    
# 7. Распределение активностей по гендеру
filtered_df = df.copy()  
filtered_df['part_time_job'] = filtered_df['part_time_job'].map({'Yes': 1, 'No': 0})
filtered_df['extracurricular_participation'] = filtered_df['extracurricular_participation'].map({'Yes': 1, 'No': 0})

group_stats = filtered_df.groupby('gender').agg({
    'social_media_hours': 'mean',
    'netflix_hours': 'mean',
    'part_time_job': 'mean',
    'exercise_frequency': 'mean',
    'extracurricular_participation': 'mean'
}).reset_index()## reset_index() добавляет новый столбец с индексами, а столбец с генднром делает обычным столбцом 

print("Распределение активностей по гендеру:")
print(group_stats)

group_stats_melted = pd.melt(group_stats, 
                             id_vars=['gender'], 
                             value_vars=['social_media_hours', 'netflix_hours', 'part_time_job', 
                                         'exercise_frequency', 'extracurricular_participation'],
                             var_name='activity', 
                             value_name='mean_value')##преобразует исходный DataFrame в DataFrame с тремя столбцами(gender,activity,mean_value).В столбец activity записывает value_vars,


plt.figure(figsize=(10, 6))
sns.barplot(x='activity', y='mean_value', hue='gender', data=group_stats_melted, palette='husl')
plt.xlabel('Активности')
plt.ylabel('Среднее значение')
plt.title('Средние значения активностей по гендеру')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Гендер')
plt.tight_layout()
plt.show()

# 9. Связь диеты и ментального здоровья
group_stats = filtered_df.groupby('diet_quality').agg({
    'mental_health_rating': 'mean'
}).reset_index()

print("\nСредний рейтинг ментального здоровья по качеству диеты:")
print(group_stats)

plt.figure(figsize=(10, 6))
sns.barplot(x='diet_quality', y='mental_health_rating', data=group_stats, palette='husl')
plt.xlabel('Качество диеты')
plt.ylabel('Средний рейтинг ментального здоровья')
plt.title('Связь качества диеты и ментального здоровья')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='age', kde=True, bins=30)
plt.title('Распределение по возрасту')


plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='study_hours_per_day', kde=True, bins=30)
plt.title('Распределение по времени затрачиваемому на обучение')





corr_matrix = df.select_dtypes(include=[np.number]).corr()
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
square=True, fmt='.2f', cbar_kws={'label': 'Коэффициент корреляции'})
plt.title('Матрица корреляций')
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='coolwarm', center=0)
plt.title('Матрица корреляций (нижний треугольник)')
plt.show()




plt.figure(figsize=(10, 6))
sns.regplot(data=df, x='age', y='study_hours_per_day', scatter_kws={'alpha':0.6})
plt.title('Зависимость времени затрачиваемого на обочение от возраста')
plt.show()


plt.figure(figsize=(10, 6))
sns.regplot(data=df, x='netflix_hours', y='social_media_hours', scatter_kws={'alpha':0.6})
plt.title('Зависимость времени затрачиваемого на социальные сети и нетфликс')
plt.show()

contingency_table = pd.crosstab(df['gender'], df['part_time_job'])
print("Таблица сопряженности:")
print(contingency_table)
plt.figure(figsize=(10, 6))
sns.heatmap(contingency_table, annot=True, fmt='d', cmap='Blues', cbar_kws={'label': 'Частота'})
plt.xlabel('Частичная занятость')
plt.ylabel('Гендер')
plt.title('Таблица сопряженности: Гендер vs Частичная занятость')
plt.tight_layout()
plt.show()