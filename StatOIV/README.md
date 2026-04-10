# Statistical Analysis and Data Processing (СОИВ) Repository

This repository contains Python scripts for statistical analysis and data processing tasks, including weather classification, weather regression analysis, clustering analysis, and student habits analysis.

## Contents

- `3.py` - Weather classification script
- `4.py` - Weather clustering analysis script  
- `1/lab1.py` - Student habits and performance analysis script
- `2/статка/2.py` - Weather regression analysis script
- Supporting PDF documents (laboratory works, methodological guides, textbook)

## Script Descriptions

### 3.py - Weather Classification

**Purpose:** Classifies weather conditions based on meteorological data.

**Dataset:** Weather prediction dataset from Kaggle (ananthr1/weather-prediction)

**Methods Used:**
- Decision Tree Classifier (default parameters)
- K-Nearest Neighbors Classifier (n_neighbors=5)
- Logistic Regression (max_iter=1000, solver='lbfgs', multi_class='auto')
- Gaussian Naive Bayes (default parameters)

**Preprocessing Steps:**
- Handling missing values and outliers using IQR method
- Creating seasonal features from date column
- Filling missing categorical values with mode
- Feature engineering: temperature differences, lag features, change indicators
- Standard scaling and KNN imputation for missing values
- Label encoding for categorical variables and target variable

**Evaluation:**
- Stratified K-Fold cross-validation (n_splits=5)
- Metrics: Accuracy, Precision, Recall, F1-score, ROC-AUC
- Confusion matrices and classification reports
- Model comparison visualization

### 4.py - Weather Clustering Analysis

**Purpose:** Performs clustering analysis on weather data to identify natural groupings.

**Dataset:** Same weather prediction dataset as in 3.py

**Methods Used:**
- PCA for dimensionality reduction (retaining 90% variance)
- KMeans Clustering (n_clusters=5, random_state=42, n_init=10)
- Agglomerative Clustering (n_clusters=5, linkage='ward')
- DBSCAN (eps=1.48, min_samples=10)

**Preprocessing Steps:**
- Similar to 3.py: outlier removal, seasonal features, missing value handling
- Feature engineering: temperature differences, lag features, change indicators
- Standard scaling

**Evaluation:**
- Internal metrics: Silhouette score, Davies-Bouldin index, Calinski-Harabasz index
- External metrics (using weather labels): Adjusted Rand Index, Normalized Mutual Information
- Visualizations: Elbow method, dendrogram, k-distance graph, cluster scatter plots

### 2/статка/2.py - Weather Regression Analysis

**Purpose:** Predicts numerical weather variables (temperature, precipitation, wind) using regression models.

**Dataset:** Weather prediction dataset from Kaggle (ananthr1/weather-prediction)

**Methods Used:**
- Linear Regression (with StandardScaler pipeline)
- Polynomial Regression (degree=2 and degree=3, with StandardScaler pipeline)
- Ridge Regression (alpha=1.0, with StandardScaler pipeline)
- Lasso Regression (alpha=0.01, with StandardScaler pipeline)
- Random Forest Regressor (n_estimators=100, random_state=42)
- Gradient Boosting Regressor (n_estimators=100, random_state=42)

**Preprocessing Steps:**
- Handling missing values and outliers using IQR method
- Creating seasonal features from date column
- One-hot encoding of categorical variables (weather, season)
- Feature engineering: temperature differences, lag features, change indicators, interaction terms
- Standard scaling of numerical features

**Evaluation:**
- K-Fold cross-validation (n_splits=5, shuffle=True)
- Metrics: Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), R²
- Feature importance analysis using Gradient Boosting model
- Comparative visualization of model performance across different target variables

### 1/lab1.py - Student Habits Analysis

**Purpose:** Analyzes relationships between student habits, lifestyle factors, and academic performance.

**Dataset:** Student habits performance dataset (student_habits_performance.csv)

**Methods Used:**
- Pearson correlation analysis
- Linear regression visualization
- Group-based aggregation and comparison
- Distribution analysis

**Analysis Performed:**
- Correlation between sleep hours and attendance percentage
- Correlation between study hours and mental health rating
- Correlation between attendance and exam scores
- Correlation between study hours and exam scores
- Correlation between exercise frequency and mental health rating
- Correlation between social media usage and sleep hours
- Exam score analysis by parental education level
- Exam score analysis by gender
- Activity distribution by gender (part-time job, extracurricular participation)
- Diet quality vs mental health rating analysis

**Visualizations:**
- Boxplots for outlier detection
- Regression plots with correlation coefficients
- Bar plots for group comparisons
- Histograms for distribution analysis
- Heatmaps for correlation matrices and contingency tables

## Requirements

The scripts require the following Python libraries:
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- kagglehub
- scipy

## Usage

Each script can be run independently:
```bash
python 3.py
python 4.py
python 2/статка/2.py
python 1/lab1.py
```

Scripts will automatically download required datasets from Kaggle (where applicable) and generate visualizations.

## Notes

- All scripts include data preprocessing pipelines
- Visualizations are displayed during execution
- Results are printed to console including metrics and analysis summaries
- The weather datasets (3.py, 4.py, and 2/статка/2.py) use the same source for comparable analysis