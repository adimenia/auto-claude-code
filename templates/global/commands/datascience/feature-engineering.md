# Feature Engineering

Automated feature selection, transformation, and engineering pipelines for optimal machine learning model performance.

## Usage:
`/project:feature-engineering [--methods] [--target] [--automation-level]` or `/user:feature-engineering [--methods]`

## Process:
1. **Feature Analysis**: Analyze existing features for importance and relationships
2. **Feature Selection**: Automated selection using statistical and ML-based methods
3. **Feature Transformation**: Apply scaling, encoding, and mathematical transformations
4. **Feature Creation**: Generate new features through combinations and domain knowledge
5. **Feature Validation**: Validate new features for performance improvement
6. **Pipeline Creation**: Build automated feature engineering pipelines
7. **Feature Store**: Set up feature storage and versioning system
8. **Monitoring Integration**: Monitor feature performance and drift over time

## Feature Engineering Methods:
- **Statistical Selection**: Correlation analysis, chi-square tests, ANOVA F-tests
- **ML-based Selection**: Recursive feature elimination, LASSO regularization, tree-based importance
- **Transformation**: Scaling, normalization, log transformation, polynomial features
- **Encoding**: One-hot encoding, target encoding, binary encoding, embedding
- **Domain Features**: Time-based features, text features, geographic features
- **Interaction Features**: Feature combinations, ratios, polynomial interactions

## Framework-Specific Implementation:
- **Data Science**: Scikit-learn pipelines, Feature-engine, Featuretools integration
- **FastAPI**: Feature serving APIs with caching and real-time transformation
- **Django**: Feature management interface with pipeline orchestration
- **Flask**: Lightweight feature transformation services

## Arguments:
- `--methods`: Feature engineering methods (selection, transformation, creation, all)
- `--target`: Target variable for supervised feature selection
- `--automation-level`: Automation level (manual, semi-automated, fully-automated)
- `--validation`: Validation strategy (cross-validation, holdout, time-series)

## Examples:
- `/project:feature-engineering --methods selection,transformation --target churn` - Feature selection and transformation for churn prediction
- `/project:feature-engineering --automation-level fully-automated` - Fully automated feature engineering
- `/project:feature-engineering --methods creation --validation cross-validation` - Feature creation with cross-validation
- `/user:feature-engineering --methods all` - Complete feature engineering setup

## Automated Feature Engineering Pipeline:

### Comprehensive Feature Engineering System:
```python
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple, Optional, Union
from sklearn.feature_selection import (
    SelectKBest, SelectFromModel, RFE, SequentialFeatureSelector,
    chi2, f_classif, f_regression, mutual_info_classif, mutual_info_regression
)
from sklearn.preprocessing import (
    StandardScaler, MinMaxScaler, RobustScaler, PowerTransformer,
    PolynomialFeatures, QuantileTransformer
)
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import Lasso, LassoCV
from sklearn.model_selection import cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import warnings
warnings.filterwarnings('ignore')

class FeatureAnalyzer:
    """Analyze features for importance, correlation, and characteristics."""
    
    def __init__(self, data: pd.DataFrame, target: str = None):
        self.data = data.copy()
        self.target = target
        self.feature_analysis = {}
        
    def analyze_feature_types(self) -> Dict[str, List[str]]:
        """Categorize features by data type and characteristics."""
        
        feature_types = {
            "numerical": [],
            "categorical": [],
            "binary": [],
            "datetime": [],
            "high_cardinality": [],
            "missing_heavy": []
        }
        
        for column in self.data.columns:
            if column == self.target:
                continue
                
            col_data = self.data[column]
            
            # Check for datetime
            if pd.api.types.is_datetime64_any_dtype(col_data):
                feature_types["datetime"].append(column)
            
            # Check for numerical
            elif pd.api.types.is_numeric_dtype(col_data):
                unique_values = col_data.nunique()
                
                # Binary numerical
                if unique_values == 2:
                    feature_types["binary"].append(column)
                else:
                    feature_types["numerical"].append(column)
            
            # Check for categorical
            else:
                unique_values = col_data.nunique()
                
                # Binary categorical
                if unique_values == 2:
                    feature_types["binary"].append(column)
                # High cardinality categorical
                elif unique_values > 50:
                    feature_types["high_cardinality"].append(column)
                else:
                    feature_types["categorical"].append(column)
            
            # Check for missing-heavy features
            missing_ratio = col_data.isnull().sum() / len(col_data)
            if missing_ratio > 0.5:
                feature_types["missing_heavy"].append(column)
        
        self.feature_analysis["types"] = feature_types
        return feature_types
    
    def calculate_feature_importance(self, method: str = "random_forest") -> Dict[str, float]:
        """Calculate feature importance using various methods."""
        
        if not self.target or self.target not in self.data.columns:
            raise ValueError("Target variable required for importance calculation")
        
        # Prepare data
        X = self.data.drop(columns=[self.target])
        y = self.data[self.target]
        
        # Handle missing values and categorical variables
        X_processed = self._preprocess_for_importance(X)
        
        importance_scores = {}
        
        if method == "random_forest":
            if y.dtype == 'object' or y.nunique() < 10:
                model = RandomForestClassifier(n_estimators=100, random_state=42)
            else:
                model = RandomForestRegressor(n_estimators=100, random_state=42)
            
            model.fit(X_processed, y)
            importance_scores = dict(zip(X_processed.columns, model.feature_importances_))
        
        elif method == "mutual_info":
            if y.dtype == 'object' or y.nunique() < 10:
                scores = mutual_info_classif(X_processed, y, random_state=42)
            else:
                scores = mutual_info_regression(X_processed, y, random_state=42)
            
            importance_scores = dict(zip(X_processed.columns, scores))
        
        elif method == "correlation":
            correlations = X_processed.corrwith(y).abs()
            importance_scores = correlations.to_dict()
        
        # Sort by importance
        importance_scores = dict(sorted(importance_scores.items(), 
                                     key=lambda x: x[1], reverse=True))
        
        self.feature_analysis["importance"] = importance_scores
        return importance_scores
    
    def _preprocess_for_importance(self, X: pd.DataFrame) -> pd.DataFrame:
        """Preprocess features for importance calculation."""
        X_processed = X.copy()
        
        # Handle missing values
        for column in X_processed.columns:
            if X_processed[column].dtype in ['int64', 'float64']:
                X_processed[column] = X_processed[column].fillna(X_processed[column].median())
            else:
                X_processed[column] = X_processed[column].fillna(X_processed[column].mode()[0] if len(X_processed[column].mode()) > 0 else 'missing')
        
        # Encode categorical variables
        categorical_columns = X_processed.select_dtypes(include=['object', 'category']).columns
        X_processed = pd.get_dummies(X_processed, columns=categorical_columns, drop_first=True)
        
        return X_processed
    
    def detect_feature_interactions(self, max_features: int = 10) -> List[Tuple[str, str, float]]:
        """Detect potential feature interactions."""
        
        if not self.target:
            return []
        
        # Get top numerical features
        numerical_features = self.data.select_dtypes(include=[np.number]).columns.tolist()
        if self.target in numerical_features:
            numerical_features.remove(self.target)
        
        numerical_features = numerical_features[:max_features]
        
        interactions = []
        
        for i, feat1 in enumerate(numerical_features):
            for feat2 in numerical_features[i+1:]:
                # Create interaction feature
                interaction = self.data[feat1] * self.data[feat2]
                correlation = interaction.corr(self.data[self.target])
                
                if not np.isnan(correlation):
                    interactions.append((feat1, feat2, abs(correlation)))
        
        # Sort by correlation strength
        interactions.sort(key=lambda x: x[2], reverse=True)
        
        self.feature_analysis["interactions"] = interactions[:10]
        return interactions[:10]


class FeatureSelector:
    """Feature selection using multiple methods."""
    
    def __init__(self, data: pd.DataFrame, target: str):
        self.data = data.copy()
        self.target = target
        self.selected_features = {}
        
    def select_statistical(self, method: str = "f_test", k: int = 10) -> List[str]:
        """Select features using statistical tests."""
        
        X = self.data.drop(columns=[self.target])
        y = self.data[self.target]
        
        # Preprocess data
        X_processed = self._preprocess_data(X)
        
        # Choose statistical test
        if method == "f_test":
            if y.dtype == 'object' or y.nunique() < 10:
                score_func = f_classif
            else:
                score_func = f_regression
        elif method == "chi2":
            score_func = chi2
            # Ensure non-negative values for chi2
            X_processed = X_processed - X_processed.min() + 1
        elif method == "mutual_info":
            if y.dtype == 'object' or y.nunique() < 10:
                score_func = mutual_info_classif
            else:
                score_func = mutual_info_regression
        
        # Select features
        selector = SelectKBest(score_func=score_func, k=min(k, X_processed.shape[1]))
        selector.fit(X_processed, y)
        
        selected_features = X_processed.columns[selector.get_support()].tolist()
        self.selected_features[f"statistical_{method}"] = selected_features
        
        return selected_features
    
    def select_model_based(self, method: str = "random_forest", max_features: int = 20) -> List[str]:
        """Select features using model-based importance."""
        
        X = self.data.drop(columns=[self.target])
        y = self.data[self.target]
        
        X_processed = self._preprocess_data(X)
        
        if method == "random_forest":
            if y.dtype == 'object' or y.nunique() < 10:
                model = RandomForestClassifier(n_estimators=100, random_state=42)
            else:
                model = RandomForestRegressor(n_estimators=100, random_state=42)
        
        elif method == "lasso":
            model = LassoCV(cv=5, random_state=42, max_iter=1000)
        
        # Fit model and select features
        selector = SelectFromModel(model, max_features=max_features)
        selector.fit(X_processed, y)
        
        selected_features = X_processed.columns[selector.get_support()].tolist()
        self.selected_features[f"model_{method}"] = selected_features
        
        return selected_features
    
    def select_recursive(self, estimator=None, n_features: int = 10) -> List[str]:
        """Select features using recursive feature elimination."""
        
        X = self.data.drop(columns=[self.target])
        y = self.data[self.target]
        
        X_processed = self._preprocess_data(X)
        
        if estimator is None:
            if y.dtype == 'object' or y.nunique() < 10:
                estimator = RandomForestClassifier(n_estimators=50, random_state=42)
            else:
                estimator = RandomForestRegressor(n_estimators=50, random_state=42)
        
        selector = RFE(estimator, n_features_to_select=min(n_features, X_processed.shape[1]))
        selector.fit(X_processed, y)
        
        selected_features = X_processed.columns[selector.get_support()].tolist()
        self.selected_features["recursive"] = selected_features
        
        return selected_features
    
    def select_sequential(self, direction: str = "forward", n_features: int = 10) -> List[str]:
        """Select features using sequential feature selection."""
        
        X = self.data.drop(columns=[self.target])
        y = self.data[self.target]
        
        X_processed = self._preprocess_data(X)
        
        if y.dtype == 'object' or y.nunique() < 10:
            estimator = RandomForestClassifier(n_estimators=50, random_state=42)
        else:
            estimator = RandomForestRegressor(n_estimators=50, random_state=42)
        
        selector = SequentialFeatureSelector(
            estimator, 
            n_features_to_select=min(n_features, X_processed.shape[1]),
            direction=direction,
            cv=3
        )
        
        selector.fit(X_processed, y)
        
        selected_features = X_processed.columns[selector.get_support()].tolist()
        self.selected_features[f"sequential_{direction}"] = selected_features
        
        return selected_features
    
    def _preprocess_data(self, X: pd.DataFrame) -> pd.DataFrame:
        """Preprocess data for feature selection."""
        X_processed = X.copy()
        
        # Handle missing values
        for column in X_processed.columns:
            if X_processed[column].dtype in ['int64', 'float64']:
                X_processed[column] = X_processed[column].fillna(X_processed[column].median())
            else:
                X_processed[column] = X_processed[column].fillna(X_processed[column].mode()[0] if len(X_processed[column].mode()) > 0 else 'missing')
        
        # Encode categorical variables
        categorical_columns = X_processed.select_dtypes(include=['object', 'category']).columns
        X_processed = pd.get_dummies(X_processed, columns=categorical_columns, drop_first=True)
        
        return X_processed
    
    def get_consensus_features(self, min_methods: int = 2) -> List[str]:
        """Get features selected by multiple methods."""
        
        if not self.selected_features:
            return []
        
        # Count how many methods selected each feature
        feature_counts = {}
        for method, features in self.selected_features.items():
            for feature in features:
                feature_counts[feature] = feature_counts.get(feature, 0) + 1
        
        # Get features selected by at least min_methods
        consensus_features = [feature for feature, count in feature_counts.items() 
                            if count >= min_methods]
        
        return consensus_features


class FeatureTransformer:
    """Transform features using various methods."""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()
        self.transformers = {}
        
    def create_scaling_pipeline(self, method: str = "standard") -> ColumnTransformer:
        """Create scaling pipeline for numerical features."""
        
        numerical_features = self.data.select_dtypes(include=[np.number]).columns.tolist()
        
        if method == "standard":
            scaler = StandardScaler()
        elif method == "minmax":
            scaler = MinMaxScaler()
        elif method == "robust":
            scaler = RobustScaler()
        elif method == "quantile":
            scaler = QuantileTransformer(output_distribution='normal')
        elif method == "power":
            scaler = PowerTransformer(method='yeo-johnson')
        
        transformer = ColumnTransformer([
            ('scaler', scaler, numerical_features)
        ], remainder='passthrough')
        
        self.transformers[f"scaling_{method}"] = transformer
        return transformer
    
    def create_polynomial_features(self, degree: int = 2, interaction_only: bool = False) -> PolynomialFeatures:
        """Create polynomial features."""
        
        poly_transformer = PolynomialFeatures(
            degree=degree,
            interaction_only=interaction_only,
            include_bias=False
        )
        
        self.transformers[f"polynomial_degree_{degree}"] = poly_transformer
        return poly_transformer
    
    def create_log_features(self, columns: List[str] = None) -> pd.DataFrame:
        """Create log-transformed features."""
        
        if columns is None:
            columns = self.data.select_dtypes(include=[np.number]).columns.tolist()
        
        log_features = pd.DataFrame()
        
        for column in columns:
            if column in self.data.columns:
                # Add small constant to avoid log(0)
                col_data = self.data[column]
                if (col_data > 0).all():
                    log_features[f"{column}_log"] = np.log(col_data)
                elif (col_data >= 0).all():
                    log_features[f"{column}_log1p"] = np.log1p(col_data)
        
        return log_features
    
    def create_binned_features(self, columns: List[str] = None, n_bins: int = 5) -> pd.DataFrame:
        """Create binned categorical features from numerical features."""
        
        if columns is None:
            columns = self.data.select_dtypes(include=[np.number]).columns.tolist()
        
        binned_features = pd.DataFrame()
        
        for column in columns:
            if column in self.data.columns:
                binned_features[f"{column}_binned"] = pd.cut(
                    self.data[column], 
                    bins=n_bins, 
                    labels=False
                )
        
        return binned_features
    
    def create_datetime_features(self, columns: List[str] = None) -> pd.DataFrame:
        """Extract features from datetime columns."""
        
        if columns is None:
            columns = self.data.select_dtypes(include=['datetime64']).columns.tolist()
        
        datetime_features = pd.DataFrame()
        
        for column in columns:
            if column in self.data.columns:
                dt_col = pd.to_datetime(self.data[column])
                
                datetime_features[f"{column}_year"] = dt_col.dt.year
                datetime_features[f"{column}_month"] = dt_col.dt.month
                datetime_features[f"{column}_day"] = dt_col.dt.day
                datetime_features[f"{column}_weekday"] = dt_col.dt.weekday
                datetime_features[f"{column}_hour"] = dt_col.dt.hour
                datetime_features[f"{column}_is_weekend"] = (dt_col.dt.weekday >= 5).astype(int)
        
        return datetime_features
    
    def create_interaction_features(self, feature_pairs: List[Tuple[str, str]]) -> pd.DataFrame:
        """Create interaction features from feature pairs."""
        
        interaction_features = pd.DataFrame()
        
        for feat1, feat2 in feature_pairs:
            if feat1 in self.data.columns and feat2 in self.data.columns:
                if (self.data[feat1].dtype in [np.number] and 
                    self.data[feat2].dtype in [np.number]):
                    
                    # Multiplication interaction
                    interaction_features[f"{feat1}_x_{feat2}"] = self.data[feat1] * self.data[feat2]
                    
                    # Division interaction (avoid division by zero)
                    with np.errstate(divide='ignore', invalid='ignore'):
                        ratio = self.data[feat1] / self.data[feat2]
                        ratio = ratio.replace([np.inf, -np.inf], np.nan)
                        interaction_features[f"{feat1}_div_{feat2}"] = ratio
        
        return interaction_features


class AutomatedFeatureEngineer:
    """Automated feature engineering pipeline."""
    
    def __init__(self, data: pd.DataFrame, target: str = None):
        self.data = data.copy()
        self.target = target
        self.analyzer = FeatureAnalyzer(data, target)
        self.selector = FeatureSelector(data, target) if target else None
        self.transformer = FeatureTransformer(data)
        self.engineered_features = pd.DataFrame()
        self.pipeline = None
        
    def run_automated_engineering(self, max_features: int = 50) -> pd.DataFrame:
        """Run automated feature engineering pipeline."""
        
        print("Starting automated feature engineering...")
        
        # 1. Analyze existing features
        print("1. Analyzing feature types...")
        feature_types = self.analyzer.analyze_feature_types()
        
        # 2. Create transformed features
        print("2. Creating transformed features...")
        transformed_features = self._create_transformed_features(feature_types)
        
        # 3. Create interaction features
        print("3. Creating interaction features...")
        interaction_features = self._create_interaction_features()
        
        # 4. Create datetime features
        print("4. Creating datetime features...")
        datetime_features = self._create_datetime_features(feature_types)
        
        # 5. Combine all features
        print("5. Combining features...")
        all_features = pd.concat([
            self.data,
            transformed_features,
            interaction_features,
            datetime_features
        ], axis=1)
        
        # 6. Select best features if target is provided
        if self.target and self.selector:
            print("6. Selecting best features...")
            selected_features = self._select_best_features(all_features, max_features)
            final_features = all_features[selected_features + [self.target]]
        else:
            final_features = all_features
        
        self.engineered_features = final_features
        
        print(f"Feature engineering completed. Original features: {self.data.shape[1]}, "
              f"Engineered features: {final_features.shape[1]}")
        
        return final_features
    
    def _create_transformed_features(self, feature_types: Dict[str, List[str]]) -> pd.DataFrame:
        """Create transformed features."""
        
        transformed_features = pd.DataFrame()
        
        # Log features for numerical columns
        numerical_features = feature_types.get("numerical", [])
        if numerical_features:
            log_features = self.transformer.create_log_features(numerical_features[:10])
            transformed_features = pd.concat([transformed_features, log_features], axis=1)
        
        # Binned features
        if numerical_features:
            binned_features = self.transformer.create_binned_features(numerical_features[:5])
            transformed_features = pd.concat([transformed_features, binned_features], axis=1)
        
        return transformed_features
    
    def _create_interaction_features(self) -> pd.DataFrame:
        """Create interaction features from top correlated features."""
        
        if not self.target:
            return pd.DataFrame()
        
        # Get top interactions
        interactions = self.analyzer.detect_feature_interactions(max_features=5)
        feature_pairs = [(feat1, feat2) for feat1, feat2, _ in interactions[:10]]
        
        if feature_pairs:
            return self.transformer.create_interaction_features(feature_pairs)
        
        return pd.DataFrame()
    
    def _create_datetime_features(self, feature_types: Dict[str, List[str]]) -> pd.DataFrame:
        """Create datetime features."""
        
        datetime_columns = feature_types.get("datetime", [])
        if datetime_columns:
            return self.transformer.create_datetime_features(datetime_columns)
        
        return pd.DataFrame()
    
    def _select_best_features(self, all_features: pd.DataFrame, max_features: int) -> List[str]:
        """Select best features using multiple methods."""
        
        # Update selector with new data
        self.selector = FeatureSelector(all_features, self.target)
        
        # Run multiple selection methods
        statistical_features = self.selector.select_statistical("f_test", k=max_features//3)
        model_features = self.selector.select_model_based("random_forest", max_features=max_features//3)
        
        # Get consensus features
        consensus_features = self.selector.get_consensus_features(min_methods=1)
        
        # Combine and limit
        all_selected = list(set(statistical_features + model_features + consensus_features))
        
        # Remove target if it was included
        if self.target in all_selected:
            all_selected.remove(self.target)
        
        return all_selected[:max_features]
    
    def create_feature_pipeline(self) -> Pipeline:
        """Create scikit-learn pipeline for feature engineering."""
        
        # Identify feature types
        numerical_features = self.data.select_dtypes(include=[np.number]).columns.tolist()
        categorical_features = self.data.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # Remove target from features
        if self.target:
            if self.target in numerical_features:
                numerical_features.remove(self.target)
            if self.target in categorical_features:
                categorical_features.remove(self.target)
        
        # Create preprocessing pipeline
        preprocessor = ColumnTransformer([
            ('num', StandardScaler(), numerical_features),
            ('cat', 'passthrough', categorical_features)  # Would need encoder in practice
        ])
        
        # Create full pipeline
        pipeline = Pipeline([
            ('preprocessor', preprocessor)
        ])
        
        self.pipeline = pipeline
        return pipeline
```

### Feature Store Integration:
```python
import pickle
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

class FeatureStore:
    """Simple feature store for versioning and serving features."""
    
    def __init__(self, store_path: str = "feature_store"):
        self.store_path = Path(store_path)
        self.store_path.mkdir(exist_ok=True)
        
    def save_features(self, features: pd.DataFrame, 
                     feature_set_name: str, version: str = None) -> str:
        """Save feature set with versioning."""
        
        if version is None:
            version = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create feature set directory
        feature_dir = self.store_path / feature_set_name
        feature_dir.mkdir(exist_ok=True)
        
        # Save features
        feature_path = feature_dir / f"features_v{version}.parquet"
        features.to_parquet(feature_path)
        
        # Save metadata
        metadata = {
            "feature_set_name": feature_set_name,
            "version": version,
            "shape": features.shape,
            "columns": features.columns.tolist(),
            "dtypes": features.dtypes.astype(str).to_dict(),
            "created_at": datetime.now().isoformat()
        }
        
        metadata_path = feature_dir / f"metadata_v{version}.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return f"{feature_set_name}:v{version}"
    
    def load_features(self, feature_set_name: str, version: str = "latest") -> pd.DataFrame:
        """Load feature set by name and version."""
        
        feature_dir = self.store_path / feature_set_name
        
        if version == "latest":
            # Find latest version
            feature_files = list(feature_dir.glob("features_v*.parquet"))
            if not feature_files:
                raise FileNotFoundError(f"No features found for {feature_set_name}")
            
            latest_file = max(feature_files, key=lambda x: x.stat().st_mtime)
            return pd.read_parquet(latest_file)
        else:
            feature_path = feature_dir / f"features_v{version}.parquet"
            return pd.read_parquet(feature_path)
    
    def list_feature_sets(self) -> List[Dict[str, Any]]:
        """List all available feature sets."""
        
        feature_sets = []
        
        for feature_dir in self.store_path.iterdir():
            if feature_dir.is_dir():
                metadata_files = list(feature_dir.glob("metadata_v*.json"))
                
                for metadata_file in metadata_files:
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                    feature_sets.append(metadata)
        
        return feature_sets
```

## Validation Checklist:
- [ ] Feature analysis completed with type categorization and importance scoring
- [ ] Multiple feature selection methods implemented and compared
- [ ] Feature transformation pipeline created with scaling and encoding
- [ ] Automated feature creation implemented (interactions, datetime, domain features)
- [ ] Feature validation performed with cross-validation and performance metrics
- [ ] Feature engineering pipeline created and tested
- [ ] Feature store implemented for versioning and serving
- [ ] Feature monitoring integrated for drift detection
- [ ] Documentation completed for all engineered features
- [ ] Performance impact validated with model training

## Output:
- Comprehensive feature analysis report with importance rankings
- Automated feature selection pipeline with multiple methods
- Feature transformation system with scaling and encoding
- Engineered feature datasets with interactions and domain features
- Validated feature engineering pipeline for production use
- Feature store system for versioning and serving features
- Feature monitoring integration for drift detection
- Performance evaluation comparing original vs engineered features
- Documentation of all feature engineering decisions and processes
- Reproducible feature engineering workflow for future use

## Notes:
- Start with domain knowledge when creating new features
- Validate feature engineering impact with cross-validation
- Consider computational cost of feature transformations in production
- Monitor feature importance and drift over time
- Document all feature engineering decisions for reproducibility
- Balance automation with domain expertise and manual review
- Regular evaluation of feature engineering pipeline performance
- Consider feature storage and serving requirements for production systems