# Model Development

Design, train, and validate machine learning models with automated hyperparameter tuning and performance evaluation.

## Usage:
`/project:model-development [--model-type] [--target] [--validation]` or `/user:model-development [--model-type]`

## Process:
1. **Problem Definition**: Define ML problem type and success metrics
2. **Data Preprocessing**: Feature engineering, scaling, and encoding
3. **Model Selection**: Choose appropriate algorithms for the problem
4. **Training Pipeline**: Implement automated training with cross-validation
5. **Hyperparameter Tuning**: Optimize model parameters using grid/random search
6. **Model Validation**: Comprehensive evaluation with multiple metrics
7. **Feature Importance**: Analyze feature contributions and interpretability
8. **Model Persistence**: Save trained models with metadata and versioning

## Model Types:
- **Classification**: Binary, multiclass, multilabel classification problems
- **Regression**: Linear, polynomial, time series regression
- **Clustering**: K-means, hierarchical, density-based clustering
- **Dimensionality Reduction**: PCA, t-SNE, UMAP for visualization and compression
- **Ensemble Methods**: Random Forest, Gradient Boosting, Stacking
- **Deep Learning**: Neural networks, CNNs, RNNs for complex patterns

## Framework-Specific Implementation:
- **Data Science**: Scikit-learn, TensorFlow, PyTorch, XGBoost pipelines
- **FastAPI**: Model serving endpoints with prediction APIs
- **Django**: Model management interface, training job scheduling
- **Flask**: Model inference web applications and REST APIs

## Arguments:
- `--model-type`: Model type (classification, regression, clustering, deep-learning)
- `--target`: Target variable name for supervised learning
- `--validation`: Validation strategy (cv, holdout, time-series, stratified)
- `--automl`: Enable automated machine learning with multiple algorithms

## Examples:
- `/project:model-development --model-type classification --target churn` - Customer churn prediction
- `/project:model-development --model-type regression --validation time-series` - Time series forecasting
- `/project:model-development --automl` - Automated model selection and tuning
- `/user:model-development --model-type clustering` - Unsupervised clustering analysis

## Model Development Pipeline:

### Automated Model Training:
```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVC, SVR
from sklearn.metrics import classification_report, mean_squared_error, r2_score
import joblib
import mlflow
import mlflow.sklearn
from datetime import datetime

class ModelDeveloper:
    """Automated machine learning model development."""
    
    def __init__(self, data: pd.DataFrame, target_column: str, problem_type: str):
        self.data = data
        self.target = target_column
        self.problem_type = problem_type.lower()
        self.models = {}
        self.best_model = None
        self.preprocessor = None
        self.results = {}
        
    def prepare_data(self, test_size: float = 0.2, random_state: int = 42):
        """Prepare data for model training."""
        # Separate features and target
        X = self.data.drop(columns=[self.target])
        y = self.data[self.target]
        
        # Handle missing values in target
        if y.isnull().any():
            print(f"Warning: Target variable has {y.isnull().sum()} missing values. Removing them.")
            mask = y.notnull()
            X = X[mask]
            y = y[mask]
        
        # Identify numeric and categorical columns
        numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_features = X.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # Create preprocessing pipeline
        numeric_transformer = Pipeline(steps=[
            ('scaler', StandardScaler())
        ])
        
        categorical_transformer = Pipeline(steps=[
            ('onehot', OneHotEncoder(handle_unknown='ignore', drop='first'))
        ])
        
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ]
        )
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state,
            stratify=y if self.problem_type == 'classification' and y.nunique() > 1 else None
        )
        
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def get_model_candidates(self):
        """Get candidate models based on problem type."""
        if self.problem_type == 'classification':
            return {
                'random_forest': RandomForestClassifier(random_state=42),
                'logistic_regression': LogisticRegression(random_state=42, max_iter=1000),
                'svm': SVC(random_state=42, probability=True)
            }
        elif self.problem_type == 'regression':
            return {
                'random_forest': RandomForestRegressor(random_state=42),
                'linear_regression': LinearRegression(),
                'svr': SVR()
            }
        else:
            raise ValueError(f"Unsupported problem type: {self.problem_type}")
    
    def get_hyperparameter_grids(self):
        """Get hyperparameter grids for tuning."""
        if self.problem_type == 'classification':
            return {
                'random_forest': {
                    'model__n_estimators': [100, 200, 300],
                    'model__max_depth': [None, 10, 20, 30],
                    'model__min_samples_split': [2, 5, 10],
                    'model__min_samples_leaf': [1, 2, 4]
                },
                'logistic_regression': {
                    'model__C': [0.1, 1, 10, 100],
                    'model__penalty': ['l1', 'l2'],
                    'model__solver': ['liblinear', 'saga']
                },
                'svm': {
                    'model__C': [0.1, 1, 10],
                    'model__kernel': ['rbf', 'poly'],
                    'model__gamma': ['scale', 'auto']
                }
            }
        elif self.problem_type == 'regression':
            return {
                'random_forest': {
                    'model__n_estimators': [100, 200, 300],
                    'model__max_depth': [None, 10, 20, 30],
                    'model__min_samples_split': [2, 5, 10]
                },
                'linear_regression': {},  # No hyperparameters to tune
                'svr': {
                    'model__C': [0.1, 1, 10],
                    'model__kernel': ['rbf', 'poly'],
                    'model__gamma': ['scale', 'auto']
                }
            }
    
    def train_and_evaluate_models(self, cv_folds: int = 5):
        """Train and evaluate all candidate models."""
        model_candidates = self.get_model_candidates()
        param_grids = self.get_hyperparameter_grids()
        
        # Set up MLflow experiment
        mlflow.set_experiment(f"model_development_{self.problem_type}")
        
        for name, model in model_candidates.items():
            print(f"Training {name}...")
            
            with mlflow.start_run(run_name=f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
                # Create pipeline
                pipeline = Pipeline([
                    ('preprocessor', self.preprocessor),
                    ('model', model)
                ])
                
                # Hyperparameter tuning
                param_grid = param_grids.get(name, {})
                
                if param_grid:
                    grid_search = GridSearchCV(
                        pipeline, param_grid, cv=cv_folds,
                        scoring='accuracy' if self.problem_type == 'classification' else 'neg_mean_squared_error',
                        n_jobs=-1, verbose=1
                    )
                    grid_search.fit(self.X_train, self.y_train)
                    best_pipeline = grid_search.best_estimator_
                    best_params = grid_search.best_params_
                else:
                    pipeline.fit(self.X_train, self.y_train)
                    best_pipeline = pipeline
                    best_params = {}
                
                # Evaluate model
                train_score = best_pipeline.score(self.X_train, self.y_train)
                test_score = best_pipeline.score(self.X_test, self.y_test)
                
                # Cross-validation scores
                cv_scores = cross_val_score(
                    best_pipeline, self.X_train, self.y_train, cv=cv_folds,
                    scoring='accuracy' if self.problem_type == 'classification' else 'neg_mean_squared_error'
                )
                
                # Store results
                self.models[name] = {
                    'pipeline': best_pipeline,
                    'train_score': train_score,
                    'test_score': test_score,
                    'cv_scores': cv_scores,
                    'cv_mean': cv_scores.mean(),
                    'cv_std': cv_scores.std(),
                    'best_params': best_params
                }
                
                # Log to MLflow
                mlflow.log_params(best_params)
                mlflow.log_metric("train_score", train_score)
                mlflow.log_metric("test_score", test_score)
                mlflow.log_metric("cv_mean", cv_scores.mean())
                mlflow.log_metric("cv_std", cv_scores.std())
                mlflow.sklearn.log_model(best_pipeline, name)
        
        # Select best model
        if self.problem_type == 'classification':
            self.best_model = max(self.models.items(), key=lambda x: x[1]['cv_mean'])
        else:
            self.best_model = max(self.models.items(), key=lambda x: -x[1]['cv_mean'])  # Negative MSE
        
        return self.models
    
    def generate_detailed_evaluation(self):
        """Generate detailed evaluation report for the best model."""
        if not self.best_model:
            raise ValueError("No models trained yet. Run train_and_evaluate_models() first.")
        
        model_name, model_info = self.best_model
        pipeline = model_info['pipeline']
        
        # Predictions
        y_train_pred = pipeline.predict(self.X_train)
        y_test_pred = pipeline.predict(self.X_test)
        
        evaluation = {
            'model_name': model_name,
            'best_parameters': model_info['best_params'],
            'scores': {
                'train_score': model_info['train_score'],
                'test_score': model_info['test_score'],
                'cv_mean': model_info['cv_mean'],
                'cv_std': model_info['cv_std']
            }
        }
        
        if self.problem_type == 'classification':
            from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
            
            # Classification metrics
            evaluation['classification_report'] = classification_report(
                self.y_test, y_test_pred, output_dict=True
            )
            evaluation['confusion_matrix'] = confusion_matrix(self.y_test, y_test_pred).tolist()
            
            # ROC AUC for binary classification
            if len(np.unique(self.y_test)) == 2:
                y_test_proba = pipeline.predict_proba(self.X_test)[:, 1]
                evaluation['roc_auc'] = roc_auc_score(self.y_test, y_test_proba)
        
        elif self.problem_type == 'regression':
            from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
            
            # Regression metrics
            evaluation['regression_metrics'] = {
                'mae': mean_absolute_error(self.y_test, y_test_pred),
                'mse': mean_squared_error(self.y_test, y_test_pred),
                'rmse': np.sqrt(mean_squared_error(self.y_test, y_test_pred)),
                'r2': r2_score(self.y_test, y_test_pred)
            }
        
        self.results = evaluation
        return evaluation
    
    def analyze_feature_importance(self):
        """Analyze feature importance for the best model."""
        if not self.best_model:
            raise ValueError("No models trained yet.")
        
        model_name, model_info = self.best_model
        pipeline = model_info['pipeline']
        
        # Get feature names after preprocessing
        feature_names = self.get_feature_names()
        
        # Extract feature importance (if available)
        model = pipeline.named_steps['model']
        
        if hasattr(model, 'feature_importances_'):
            # Tree-based models
            importance = model.feature_importances_
        elif hasattr(model, 'coef_'):
            # Linear models
            importance = np.abs(model.coef_).flatten()
        else:
            print(f"Feature importance not available for {model_name}")
            return None
        
        # Create feature importance dataframe
        feature_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': importance
        }).sort_values('importance', ascending=False)
        
        return feature_importance
    
    def get_feature_names(self):
        """Get feature names after preprocessing."""
        # This is a simplified version - in practice, you'd need to handle
        # the column transformer more carefully
        numeric_features = self.X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_features = self.X_train.select_dtypes(include=['object', 'category']).columns.tolist()
        
        feature_names = numeric_features.copy()
        
        # For categorical features, we'd need to get the actual encoded column names
        # This is simplified - in practice, use get_feature_names_out() method
        for cat_feature in categorical_features:
            unique_values = self.X_train[cat_feature].unique()
            for value in unique_values[1:]:  # Skip first due to drop='first'
                feature_names.append(f"{cat_feature}_{value}")
        
        return feature_names
    
    def save_model(self, filepath: str = None):
        """Save the best model with metadata."""
        if not self.best_model:
            raise ValueError("No models trained yet.")
        
        if not filepath:
            filepath = f"best_model_{self.problem_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.joblib"
        
        model_name, model_info = self.best_model
        
        # Create model package
        model_package = {
            'model': model_info['pipeline'],
            'model_name': model_name,
            'problem_type': self.problem_type,
            'target_column': self.target,
            'feature_names': self.get_feature_names(),
            'evaluation': self.results,
            'training_date': datetime.now().isoformat(),
            'data_shape': self.data.shape
        }
        
        joblib.dump(model_package, filepath)
        print(f"Model saved to {filepath}")
        
        return filepath
```

### Deep Learning Integration:
```python
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np

class DeepLearningDeveloper:
    """Deep learning model development with TensorFlow/Keras."""
    
    def __init__(self, data: pd.DataFrame, target_column: str, problem_type: str):
        self.data = data
        self.target = target_column
        self.problem_type = problem_type
        self.model = None
        self.history = None
        
    def prepare_data_for_dl(self, test_size: float = 0.2, validation_size: float = 0.2):
        """Prepare data for deep learning."""
        X = self.data.drop(columns=[self.target])
        y = self.data[self.target]
        
        # Handle categorical features
        X = pd.get_dummies(X, drop_first=True)
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Split data
        X_train, X_temp, y_train, y_temp = train_test_split(
            X_scaled, y, test_size=test_size + validation_size, random_state=42
        )
        
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=test_size/(test_size + validation_size), random_state=42
        )
        
        return X_train, X_val, X_test, y_train, y_val, y_test
    
    def build_neural_network(self, input_shape: int, architecture: str = 'simple'):
        """Build neural network architecture."""
        if architecture == 'simple':
            model = keras.Sequential([
                keras.layers.Dense(64, activation='relu', input_shape=(input_shape,)),
                keras.layers.Dropout(0.3),
                keras.layers.Dense(32, activation='relu'),
                keras.layers.Dropout(0.3),
                keras.layers.Dense(16, activation='relu'),
            ])
        elif architecture == 'deep':
            model = keras.Sequential([
                keras.layers.Dense(128, activation='relu', input_shape=(input_shape,)),
                keras.layers.BatchNormalization(),
                keras.layers.Dropout(0.4),
                keras.layers.Dense(64, activation='relu'),
                keras.layers.BatchNormalization(),
                keras.layers.Dropout(0.3),
                keras.layers.Dense(32, activation='relu'),
                keras.layers.Dropout(0.2),
                keras.layers.Dense(16, activation='relu'),
            ])
        
        # Add output layer based on problem type
        if self.problem_type == 'classification':
            n_classes = self.data[self.target].nunique()
            if n_classes == 2:
                model.add(keras.layers.Dense(1, activation='sigmoid'))
                model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
            else:
                model.add(keras.layers.Dense(n_classes, activation='softmax'))
                model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        else:  # regression
            model.add(keras.layers.Dense(1))
            model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        
        self.model = model
        return model
    
    def train_with_callbacks(self, X_train, y_train, X_val, y_val, epochs: int = 100):
        """Train model with callbacks for optimal performance."""
        callbacks = [
            keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7
            ),
            keras.callbacks.ModelCheckpoint(
                'best_model.h5',
                monitor='val_loss',
                save_best_only=True
            )
        ]
        
        self.history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=32,
            callbacks=callbacks,
            verbose=1
        )
        
        return self.history
```

### AutoML Integration:
```python
try:
    import optuna
    from optuna.integration import SklearnStudy
    HAS_OPTUNA = True
except ImportError:
    HAS_OPTUNA = False

class AutoMLDeveloper:
    """Automated machine learning with hyperparameter optimization."""
    
    def __init__(self, data: pd.DataFrame, target_column: str, problem_type: str):
        self.data = data
        self.target = target_column
        self.problem_type = problem_type
        self.study = None
        self.best_model = None
        
    def objective(self, trial):
        """Objective function for Optuna optimization."""
        # Model selection
        model_name = trial.suggest_categorical('model', ['rf', 'lr', 'svm', 'xgb'])
        
        if model_name == 'rf':
            model = RandomForestClassifier(
                n_estimators=trial.suggest_int('rf_n_estimators', 10, 300),
                max_depth=trial.suggest_int('rf_max_depth', 3, 30),
                min_samples_split=trial.suggest_int('rf_min_samples_split', 2, 20),
                random_state=42
            )
        elif model_name == 'lr':
            model = LogisticRegression(
                C=trial.suggest_float('lr_C', 1e-4, 100.0, log=True),
                max_iter=1000,
                random_state=42
            )
        elif model_name == 'svm':
            model = SVC(
                C=trial.suggest_float('svm_C', 1e-4, 100.0, log=True),
                kernel=trial.suggest_categorical('svm_kernel', ['rbf', 'poly']),
                random_state=42
            )
        elif model_name == 'xgb':
            import xgboost as xgb
            model = xgb.XGBClassifier(
                n_estimators=trial.suggest_int('xgb_n_estimators', 10, 300),
                max_depth=trial.suggest_int('xgb_max_depth', 3, 10),
                learning_rate=trial.suggest_float('xgb_learning_rate', 0.01, 0.3),
                random_state=42
            )
        
        # Cross-validation
        scores = cross_val_score(model, self.X_train, self.y_train, cv=5, scoring='accuracy')
        return scores.mean()
    
    def run_automl(self, n_trials: int = 100):
        """Run automated machine learning optimization."""
        if not HAS_OPTUNA:
            raise ImportError("Optuna is required for AutoML. Install with: pip install optuna")
        
        # Prepare data
        X = self.data.drop(columns=[self.target])
        y = self.data[self.target]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Create study
        self.study = optuna.create_study(direction='maximize')
        self.study.optimize(self.objective, n_trials=n_trials)
        
        print(f"Best trial: {self.study.best_trial.number}")
        print(f"Best value: {self.study.best_value}")
        print(f"Best params: {self.study.best_params}")
        
        return self.study.best_params
```

## Validation Checklist:
- [ ] Problem type correctly identified and configured
- [ ] Data preprocessing pipeline implemented with proper handling
- [ ] Multiple model algorithms tested and compared
- [ ] Hyperparameter tuning performed systematically
- [ ] Cross-validation implemented for robust evaluation
- [ ] Model performance metrics appropriate for problem type
- [ ] Feature importance analysis completed
- [ ] Model persistence and versioning implemented
- [ ] Overfitting detection and prevention measures applied
- [ ] Results logged and tracked for reproducibility

## Output:
- Trained and validated machine learning models
- Comprehensive model evaluation reports with metrics
- Hyperparameter tuning results and best configurations
- Feature importance analysis and interpretability insights
- Model comparison matrix with performance statistics
- Serialized models with metadata and versioning
- MLflow experiment tracking for reproducibility
- Automated model selection recommendations
- Data preprocessing pipelines for production deployment
- Training and validation visualizations

## Notes:
- Start with simple models before moving to complex ones
- Always validate models on unseen test data
- Use appropriate evaluation metrics for your problem type
- Monitor for overfitting during training process
- Consider computational resources when selecting algorithms
- Document all assumptions and decisions for reproducibility
- Regular model retraining as new data becomes available
- Implement proper model versioning and metadata tracking