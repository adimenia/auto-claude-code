# Data Exploration

Perform comprehensive exploratory data analysis (EDA) with automated profiling, visualization, and data quality assessment.

## Usage:
`/project:data-exploration [--dataset] [--output-format] [--depth]` or `/user:data-exploration [--dataset]`

## Process:
1. **Data Loading & Validation**: Load data and perform initial validation checks
2. **Statistical Profiling**: Generate comprehensive statistical summaries
3. **Data Quality Assessment**: Identify missing values, outliers, and inconsistencies
4. **Distribution Analysis**: Analyze feature distributions and relationships
5. **Correlation Analysis**: Identify feature correlations and multicollinearity
6. **Visualization Generation**: Create comprehensive data visualizations
7. **Bias Detection**: Check for potential data bias and sampling issues
8. **Report Generation**: Create automated EDA reports with insights and recommendations

## Analysis Types:
- **Univariate Analysis**: Individual feature analysis, distributions, outliers
- **Bivariate Analysis**: Feature relationships, correlations, scatter plots
- **Multivariate Analysis**: Feature interactions, dimensionality reduction
- **Time Series Analysis**: Temporal patterns, seasonality, trends
- **Categorical Analysis**: Category distributions, chi-square tests
- **Geographic Analysis**: Spatial data patterns and distributions

## Framework-Specific Implementation:
- **Data Science**: Jupyter notebooks, pandas profiling, automated reports
- **FastAPI**: Data validation endpoints, real-time data quality APIs
- **Django**: Data dashboard views, admin interface for data exploration
- **Flask**: Interactive data exploration web apps

## Arguments:
- `--dataset`: Target dataset (csv, parquet, database, api)
- `--output-format`: Output format (notebook, html, pdf, json)
- `--depth`: Analysis depth (basic, standard, comprehensive, research-grade)
- `--target`: Target variable for supervised learning analysis

## Examples:
- `/project:data-exploration --dataset data/customers.csv` - Basic customer data exploration
- `/project:data-exploration --depth comprehensive --target churn` - Deep analysis with target variable
- `/project:data-exploration --output-format html` - HTML report generation
- `/user:data-exploration --dataset database` - Database table exploration

## Automated EDA Implementation:

### Pandas Profiling Integration:
```python
import pandas as pd
import numpy as np
from pandas_profiling import ProfileReport
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class DataExplorer:
    """Comprehensive data exploration and analysis."""
    
    def __init__(self, data_path: str, target_column: str = None):
        self.data = pd.read_csv(data_path) if data_path.endswith('.csv') else pd.read_parquet(data_path)
        self.target = target_column
        self.profile = None
        self.insights = {}
    
    def generate_profile_report(self, output_path: str = "data_profile.html"):
        """Generate comprehensive pandas profiling report."""
        profile = ProfileReport(
            self.data,
            title="Data Exploration Report",
            explorative=True,
            minimal=False,
            samples={"head": 10, "tail": 10},
            correlations={
                "pearson": {"calculate": True},
                "spearman": {"calculate": True},
                "kendall": {"calculate": False},
                "phi_k": {"calculate": True},
                "cramers": {"calculate": True},
            },
            missing_diagrams={
                "matrix": True,
                "bar": True,
                "heatmap": True,
                "dendrogram": True,
            }
        )
        
        profile.to_file(output_path)
        self.profile = profile
        return profile
    
    def analyze_data_quality(self):
        """Perform comprehensive data quality analysis."""
        quality_report = {
            "shape": self.data.shape,
            "memory_usage": self.data.memory_usage(deep=True).sum(),
            "missing_values": self.data.isnull().sum().to_dict(),
            "duplicate_rows": self.data.duplicated().sum(),
            "data_types": self.data.dtypes.to_dict(),
        }
        
        # Detect outliers using IQR method
        numeric_columns = self.data.select_dtypes(include=[np.number]).columns
        outliers = {}
        
        for col in numeric_columns:
            Q1 = self.data[col].quantile(0.25)
            Q3 = self.data[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outlier_count = ((self.data[col] < lower_bound) | 
                           (self.data[col] > upper_bound)).sum()
            outliers[col] = {
                "count": outlier_count,
                "percentage": (outlier_count / len(self.data)) * 100
            }
        
        quality_report["outliers"] = outliers
        
        # Check for high cardinality categorical features
        categorical_columns = self.data.select_dtypes(include=['object']).columns
        high_cardinality = {}
        
        for col in categorical_columns:
            unique_count = self.data[col].nunique()
            if unique_count > 50:  # Threshold for high cardinality
                high_cardinality[col] = unique_count
        
        quality_report["high_cardinality_features"] = high_cardinality
        
        self.insights["data_quality"] = quality_report
        return quality_report
    
    def analyze_feature_relationships(self):
        """Analyze relationships between features."""
        numeric_data = self.data.select_dtypes(include=[np.number])
        
        # Correlation analysis
        correlation_matrix = numeric_data.corr()
        
        # Find highly correlated feature pairs
        high_correlations = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                corr_value = correlation_matrix.iloc[i, j]
                if abs(corr_value) > 0.8:  # High correlation threshold
                    high_correlations.append({
                        "feature1": correlation_matrix.columns[i],
                        "feature2": correlation_matrix.columns[j],
                        "correlation": corr_value
                    })
        
        # Target variable analysis (if provided)
        target_correlations = {}
        if self.target and self.target in self.data.columns:
            target_correlations = correlation_matrix[self.target].abs().sort_values(ascending=False).to_dict()
        
        relationship_analysis = {
            "correlation_matrix": correlation_matrix.to_dict(),
            "high_correlations": high_correlations,
            "target_correlations": target_correlations
        }
        
        self.insights["feature_relationships"] = relationship_analysis
        return relationship_analysis
    
    def detect_data_bias(self):
        """Detect potential bias in the dataset."""
        bias_analysis = {}
        
        # Check for class imbalance (if target is provided)
        if self.target and self.target in self.data.columns:
            target_distribution = self.data[self.target].value_counts(normalize=True)
            min_class_ratio = target_distribution.min()
            
            bias_analysis["class_imbalance"] = {
                "distribution": target_distribution.to_dict(),
                "imbalance_ratio": min_class_ratio,
                "is_imbalanced": min_class_ratio < 0.1  # Less than 10% is considered imbalanced
            }
        
        # Check for sampling bias indicators
        categorical_columns = self.data.select_dtypes(include=['object']).columns
        sampling_indicators = {}
        
        for col in categorical_columns:
            value_counts = self.data[col].value_counts(normalize=True)
            # Check if one category dominates (>80%)
            max_category_ratio = value_counts.max()
            if max_category_ratio > 0.8:
                sampling_indicators[col] = {
                    "dominant_category": value_counts.idxmax(),
                    "ratio": max_category_ratio
                }
        
        bias_analysis["sampling_bias_indicators"] = sampling_indicators
        
        self.insights["bias_analysis"] = bias_analysis
        return bias_analysis
    
    def generate_visualizations(self, output_dir: str = "visualizations"):
        """Generate comprehensive data visualizations."""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Distribution plots for numeric features
        numeric_columns = self.data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_columns[:10]:  # Limit to first 10 features
            plt.figure(figsize=(12, 4))
            
            plt.subplot(1, 2, 1)
            plt.hist(self.data[col].dropna(), bins=30, alpha=0.7)
            plt.title(f'Distribution of {col}')
            plt.xlabel(col)
            plt.ylabel('Frequency')
            
            plt.subplot(1, 2, 2)
            stats.probplot(self.data[col].dropna(), dist="norm", plot=plt)
            plt.title(f'Q-Q Plot of {col}')
            
            plt.tight_layout()
            plt.savefig(f'{output_dir}/{col}_distribution.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        # Correlation heatmap
        if len(numeric_columns) > 1:
            plt.figure(figsize=(12, 10))
            correlation_matrix = self.data[numeric_columns].corr()
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
            plt.title('Feature Correlation Matrix')
            plt.tight_layout()
            plt.savefig(f'{output_dir}/correlation_heatmap.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        # Missing value heatmap
        plt.figure(figsize=(12, 8))
        sns.heatmap(self.data.isnull(), yticklabels=False, cbar=True, cmap='viridis')
        plt.title('Missing Values Heatmap')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/missing_values_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        return f"Visualizations saved to {output_dir}/"
```

### Advanced Statistical Analysis:
```python
from scipy.stats import chi2_contingency, normaltest, shapiro
from sklearn.feature_selection import mutual_info_regression, mutual_info_classif
import warnings

class StatisticalAnalyzer:
    """Advanced statistical analysis for data exploration."""
    
    def __init__(self, data: pd.DataFrame, target: str = None):
        self.data = data
        self.target = target
        self.results = {}
    
    def test_normality(self):
        """Test normality of numeric features."""
        numeric_columns = self.data.select_dtypes(include=[np.number]).columns
        normality_tests = {}
        
        for col in numeric_columns:
            data_clean = self.data[col].dropna()
            
            if len(data_clean) > 5000:
                # Use D'Agostino's test for large samples
                stat, p_value = normaltest(data_clean)
                test_name = "D'Agostino"
            else:
                # Use Shapiro-Wilk for smaller samples
                stat, p_value = shapiro(data_clean)
                test_name = "Shapiro-Wilk"
            
            normality_tests[col] = {
                "test": test_name,
                "statistic": stat,
                "p_value": p_value,
                "is_normal": p_value > 0.05
            }
        
        self.results["normality_tests"] = normality_tests
        return normality_tests
    
    def test_independence(self):
        """Test independence between categorical variables."""
        categorical_columns = self.data.select_dtypes(include=['object']).columns
        independence_tests = {}
        
        for i, col1 in enumerate(categorical_columns):
            for col2 in categorical_columns[i+1:]:
                contingency_table = pd.crosstab(self.data[col1], self.data[col2])
                
                try:
                    chi2, p_value, dof, expected = chi2_contingency(contingency_table)
                    independence_tests[f"{col1}_vs_{col2}"] = {
                        "chi2_statistic": chi2,
                        "p_value": p_value,
                        "degrees_of_freedom": dof,
                        "is_independent": p_value > 0.05
                    }
                except ValueError:
                    # Handle cases where chi-square test is not appropriate
                    independence_tests[f"{col1}_vs_{col2}"] = {
                        "error": "Chi-square test not applicable",
                        "reason": "Insufficient data or zero frequencies"
                    }
        
        self.results["independence_tests"] = independence_tests
        return independence_tests
    
    def calculate_feature_importance(self):
        """Calculate feature importance using mutual information."""
        if not self.target or self.target not in self.data.columns:
            return {"error": "Target variable not specified or not found"}
        
        # Prepare features and target
        features = self.data.drop(columns=[self.target])
        target = self.data[self.target]
        
        # Handle missing values
        features_clean = features.fillna(features.median() if features.select_dtypes(include=[np.number]).shape[1] > 0 else features.mode().iloc[0])
        target_clean = target.fillna(target.mode().iloc[0] if target.dtype == 'object' else target.median())
        
        # Encode categorical features
        from sklearn.preprocessing import LabelEncoder
        categorical_columns = features_clean.select_dtypes(include=['object']).columns
        
        for col in categorical_columns:
            le = LabelEncoder()
            features_clean[col] = le.fit_transform(features_clean[col].astype(str))
        
        # Calculate mutual information
        if target.dtype == 'object':
            # Classification task
            mi_scores = mutual_info_classif(features_clean, target_clean)
        else:
            # Regression task
            mi_scores = mutual_info_regression(features_clean, target_clean)
        
        feature_importance = dict(zip(features_clean.columns, mi_scores))
        feature_importance = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True))
        
        self.results["feature_importance"] = feature_importance
        return feature_importance
```

### Automated Report Generation:
```python
from jinja2 import Template
import json
from datetime import datetime

class EDAReportGenerator:
    """Generate comprehensive EDA reports."""
    
    def __init__(self, explorer: DataExplorer):
        self.explorer = explorer
        self.insights = explorer.insights
    
    def generate_executive_summary(self):
        """Generate executive summary of findings."""
        summary = {
            "dataset_overview": {
                "rows": self.explorer.data.shape[0],
                "columns": self.explorer.data.shape[1],
                "memory_usage_mb": round(self.explorer.data.memory_usage(deep=True).sum() / 1024**2, 2),
                "missing_data_percentage": round((self.explorer.data.isnull().sum().sum() / self.explorer.data.size) * 100, 2)
            },
            "key_findings": [],
            "recommendations": [],
            "data_quality_score": self.calculate_data_quality_score()
        }
        
        # Generate key findings based on analysis
        if "data_quality" in self.insights:
            dq = self.insights["data_quality"]
            
            if dq["duplicate_rows"] > 0:
                summary["key_findings"].append(f"Found {dq['duplicate_rows']} duplicate rows")
                summary["recommendations"].append("Remove duplicate rows to improve data quality")
            
            high_missing = [col for col, missing in dq["missing_values"].items() if missing > len(self.explorer.data) * 0.3]
            if high_missing:
                summary["key_findings"].append(f"Features with >30% missing data: {', '.join(high_missing)}")
                summary["recommendations"].append("Consider dropping or imputing high-missing features")
        
        if "feature_relationships" in self.insights:
            fr = self.insights["feature_relationships"]
            if fr["high_correlations"]:
                summary["key_findings"].append(f"Found {len(fr['high_correlations'])} highly correlated feature pairs")
                summary["recommendations"].append("Consider feature selection to reduce multicollinearity")
        
        return summary
    
    def calculate_data_quality_score(self):
        """Calculate overall data quality score (0-100)."""
        score = 100
        
        if "data_quality" in self.insights:
            dq = self.insights["data_quality"]
            
            # Penalize for missing data
            missing_percentage = (sum(dq["missing_values"].values()) / self.explorer.data.size) * 100
            score -= min(missing_percentage * 2, 30)  # Max 30 point penalty
            
            # Penalize for duplicates
            duplicate_percentage = (dq["duplicate_rows"] / len(self.explorer.data)) * 100
            score -= min(duplicate_percentage * 3, 20)  # Max 20 point penalty
            
            # Penalize for outliers
            outlier_features = sum(1 for outlier_info in dq["outliers"].values() if outlier_info["percentage"] > 5)
            score -= min(outlier_features * 5, 25)  # Max 25 point penalty
        
        return max(score, 0)
    
    def generate_html_report(self, output_path: str = "eda_report.html"):
        """Generate comprehensive HTML report."""
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Data Exploration Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .header { background-color: #f8f9fa; padding: 20px; border-radius: 5px; }
                .section { margin: 30px 0; }
                .metric { display: inline-block; margin: 10px; padding: 15px; background-color: #e9ecef; border-radius: 5px; }
                .finding { background-color: #fff3cd; padding: 10px; margin: 5px 0; border-radius: 3px; }
                .recommendation { background-color: #d1ecf1; padding: 10px; margin: 5px 0; border-radius: 3px; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Data Exploration Report</h1>
                <p>Generated on: {{ timestamp }}</p>
                <div class="metric">
                    <strong>Data Quality Score:</strong> {{ summary.data_quality_score }}/100
                </div>
                <div class="metric">
                    <strong>Rows:</strong> {{ summary.dataset_overview.rows }}
                </div>
                <div class="metric">
                    <strong>Columns:</strong> {{ summary.dataset_overview.columns }}
                </div>
                <div class="metric">
                    <strong>Missing Data:</strong> {{ summary.dataset_overview.missing_data_percentage }}%
                </div>
            </div>
            
            <div class="section">
                <h2>Key Findings</h2>
                {% for finding in summary.key_findings %}
                <div class="finding">{{ finding }}</div>
                {% endfor %}
            </div>
            
            <div class="section">
                <h2>Recommendations</h2>
                {% for rec in summary.recommendations %}
                <div class="recommendation">{{ rec }}</div>
                {% endfor %}
            </div>
            
            {% if feature_importance %}
            <div class="section">
                <h2>Feature Importance</h2>
                <table>
                    <tr><th>Feature</th><th>Importance Score</th></tr>
                    {% for feature, score in feature_importance.items() %}
                    <tr><td>{{ feature }}</td><td>{{ "%.4f"|format(score) }}</td></tr>
                    {% endfor %}
                </table>
            </div>
            {% endif %}
        </body>
        </html>
        """
        
        template = Template(html_template)
        summary = self.generate_executive_summary()
        
        html_content = template.render(
            summary=summary,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            feature_importance=self.insights.get("feature_importance", {})
        )
        
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        return output_path
```

## Validation Checklist:
- [ ] Data loading and validation successful
- [ ] Statistical profiling complete with all metrics
- [ ] Data quality issues identified and documented
- [ ] Correlation analysis and multicollinearity detection performed
- [ ] Bias detection analysis completed
- [ ] Visualizations generated and saved
- [ ] Statistical tests performed where appropriate
- [ ] Feature importance calculated (if target provided)
- [ ] Comprehensive report generated
- [ ] Insights and recommendations provided

## Output:
- Comprehensive pandas profiling HTML report
- Statistical analysis results with normality and independence tests
- Data quality assessment with missing values and outlier analysis
- Feature correlation matrix and relationship analysis
- Bias detection report with sampling and class imbalance analysis
- Automated visualizations (distributions, correlations, missing values)
- Executive summary with key findings and recommendations
- Feature importance rankings (if target variable provided)
- Actionable insights for data preprocessing and modeling

## Notes:
- Start with automated profiling before deep-dive analysis
- Pay special attention to data quality issues early in the project
- Use statistical tests to validate assumptions about the data
- Consider domain expertise when interpreting statistical results
- Document all findings and assumptions for reproducibility
- Regular data exploration as new data becomes available
- Balance automation with manual investigation for critical insights