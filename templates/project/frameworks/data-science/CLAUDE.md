# Data Science Project - Claude Configuration

## Project Overview
This is a data science project focused on data analysis, machine learning, and research workflows. The project emphasizes reproducible research, interactive development with Jupyter notebooks, and modern data science best practices including experiment tracking and model deployment.

**Key Technologies:**
- **Jupyter/JupyterLab**: Interactive computing environment for data exploration
- **pandas**: Data manipulation and analysis library
- **NumPy**: Numerical computing with arrays and mathematical functions
- **scikit-learn**: Machine learning library for classification, regression, clustering
- **matplotlib/seaborn/plotly**: Data visualization libraries
- **TensorFlow/PyTorch**: Deep learning frameworks
- **MLflow/Weights & Biases**: Experiment tracking and model management
- **Streamlit/Gradio**: Interactive web applications for model deployment

## Architecture & Patterns

### Directory Structure
```
project/
├── data/
│   ├── raw/                 # Original, immutable data
│   ├── interim/            # Intermediate data transformations
│   ├── processed/          # Final datasets for modeling
│   └── external/           # Third-party data sources
├── notebooks/
│   ├── 01_exploration/     # Initial data exploration
│   ├── 02_preprocessing/   # Data cleaning and preparation
│   ├── 03_modeling/        # Model development and training
│   ├── 04_evaluation/      # Model evaluation and validation
│   └── 05_reporting/       # Final analysis and reporting
├── src/
│   ├── __init__.py
│   ├── data/               # Data processing modules
│   │   ├── __init__.py
│   │   ├── load_data.py    # Data loading functions
│   │   ├── clean_data.py   # Data cleaning utilities
│   │   └── make_dataset.py # Dataset creation pipeline
│   ├── features/           # Feature engineering
│   │   ├── __init__.py
│   │   ├── build_features.py
│   │   └── feature_selection.py
│   ├── models/             # Model training and prediction
│   │   ├── __init__.py
│   │   ├── train_model.py
│   │   ├── predict_model.py
│   │   └── evaluate_model.py
│   ├── visualization/      # Plotting and visualization
│   │   ├── __init__.py
│   │   ├── visualize.py
│   │   └── dashboard.py
│   └── utils/              # Utility functions
│       ├── __init__.py
│       ├── config.py
│       └── helpers.py
├── models/                 # Trained model artifacts
├── reports/                # Analysis reports and documentation
│   ├── figures/           # Generated graphics and figures
│   └── presentations/     # Slides and presentation materials
├── tests/                 # Unit tests for source code
├── requirements.txt       # Python dependencies
├── environment.yml        # Conda environment specification
├── .env                   # Environment variables
└── README.md              # Project documentation
```

### Data Science Patterns
- **Data pipeline**: Raw → Interim → Processed → Model → Results
- **Reproducible research**: Version control for data, code, and experiments
- **Notebook organization**: Structured approach from exploration to deployment
- **Modular code**: Separate notebooks from reusable Python modules
- **Experiment tracking**: Log parameters, metrics, and artifacts
- **Data validation**: Schema validation and data quality checks
- **Feature stores**: Centralized feature management for consistency

## Development Workflow

### Common Commands
```bash
# Environment management
conda create -n project-name python=3.9
conda activate project-name
conda install --file requirements.txt
pip install -r requirements.txt

# Jupyter Lab/Notebook
jupyter lab                          # Start JupyterLab
jupyter notebook                     # Start classic notebook
jupyter lab --port=8889             # Custom port
jupyter nbconvert notebook.ipynb --to html  # Convert to HTML
jupyter nbconvert notebook.ipynb --to python  # Convert to .py

# Data processing
python src/data/make_dataset.py     # Create processed datasets
python src/features/build_features.py  # Feature engineering
python src/models/train_model.py    # Train models
python src/models/evaluate_model.py # Evaluate model performance

# MLflow experiment tracking
mlflow server --host 0.0.0.0 --port 5000
mlflow ui                           # View experiment tracking UI
mlflow run . -P alpha=0.5          # Run MLflow project

# Streamlit applications
streamlit run app.py                # Launch Streamlit app
streamlit run dashboard.py --port 8501

# Testing and quality
pytest tests/                       # Run unit tests
pytest --cov=src tests/            # Test with coverage
black src/ tests/                   # Code formatting
flake8 src/ tests/                  # Linting
mypy src/                          # Type checking

# Data quality checks
great_expectations checkpoint run   # Data validation
dvc repro                          # Reproduce DVC pipeline
dvc dag                            # View pipeline DAG
```

### Development Process
1. **Data exploration** - Understand data characteristics and quality
2. **Data cleaning** - Handle missing values, outliers, inconsistencies
3. **Feature engineering** - Create and select relevant features
4. **Model development** - Train and tune machine learning models
5. **Model evaluation** - Assess performance using appropriate metrics
6. **Experiment tracking** - Log all experiments with parameters and results
7. **Model deployment** - Create production-ready model endpoints
8. **Monitoring** - Track model performance and data drift in production

### Git Workflow
- **Feature branches**: `feature/customer-segmentation-model`
- **Data versioning**: Use DVC or similar for large datasets
- **Notebook commits**: Clean outputs before committing notebooks
- **Model artifacts**: Store in model registry, not in Git
- **Experiment tracking**: Link experiments to Git commits

## Code Quality & Standards

### Python Code Style
- **Follow PEP 8** with Black formatting for all source code
- **Type hints**: Use for function parameters and returns in src/ modules
- **Docstrings**: NumPy style for all functions and classes
- **Modular design**: Keep notebooks focused, move reusable code to src/
- **Error handling**: Robust error handling for data processing pipelines

### Data Science Standards
- **Reproducible results**: Set random seeds for all stochastic operations
- **Data documentation**: Document data sources, schemas, and transformations
- **Code organization**: Separate exploration from production code
- **Version control**: Track data, code, and model versions
- **Testing**: Unit tests for data processing and model functions
- **Documentation**: Clear README with setup and usage instructions

### Notebook Standards
- **Consistent structure**: Title, imports, parameters, analysis, conclusions
- **Clear markdown**: Explain objectives, methodology, and findings
- **Clean outputs**: Remove or minimize outputs before committing
- **Modular cells**: One concept per cell, clear cell dependencies
- **Performance**: Profile memory usage and execution time for large datasets

## Testing Strategy

### Test Types
```python
# Data validation tests
def test_data_schema():
    df = load_raw_data()
    assert set(df.columns) == set(EXPECTED_COLUMNS)
    assert df['price'].dtype == 'float64'
    assert not df['id'].duplicated().any()

# Feature engineering tests
def test_feature_creation():
    df = create_features(sample_data)
    assert 'feature_engineered' in df.columns
    assert df['feature_engineered'].notna().all()

# Model tests
def test_model_prediction():
    model = load_model('models/trained_model.pkl')
    prediction = model.predict(test_features)
    assert prediction.shape[0] == test_features.shape[0]
    assert all(0 <= p <= 1 for p in prediction)  # For probability predictions

# Pipeline tests
def test_data_pipeline():
    result = run_full_pipeline(sample_input)
    assert result is not None
    assert 'predictions' in result
```

### Data Quality Assurance
- **Schema validation**: Ensure data types and column names are correct
- **Range checks**: Verify numerical values are within expected ranges
- **Completeness**: Check for missing data and handle appropriately
- **Consistency**: Validate relationships between different data fields
- **Distribution checks**: Monitor for data drift over time

## Environment Variables

### Required Variables
```bash
# Data sources
DATA_SOURCE_URL=https://api.example.com/data
DATABASE_URL=postgresql://user:password@localhost/datadb
S3_BUCKET_NAME=my-data-bucket
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key

# Model serving
MODEL_REGISTRY_URL=http://localhost:5000
MLFLOW_TRACKING_URI=http://localhost:5000
WANDB_API_KEY=your-wandb-key

# Jupyter configuration
JUPYTER_PORT=8888
JUPYTER_TOKEN=your-secure-token

# Application settings
STREAMLIT_SERVER_PORT=8501
DEBUG=True
LOG_LEVEL=INFO
```

### Environment Management
```bash
# Conda environment
conda env export > environment.yml
conda env create -f environment.yml

# pip requirements
pip freeze > requirements.txt
pip install -r requirements.txt

# Development vs Production
requirements-dev.txt  # Development dependencies
requirements.txt      # Production dependencies
```

## Experiment Tracking & MLOps

### MLflow Integration
```python
import mlflow
import mlflow.sklearn

# Start experiment
mlflow.set_experiment("customer_segmentation")

with mlflow.start_run():
    # Log parameters
    mlflow.log_param("n_clusters", 5)
    mlflow.log_param("algorithm", "kmeans")
    
    # Train model
    model = train_model(data, n_clusters=5)
    
    # Log metrics
    mlflow.log_metric("silhouette_score", score)
    mlflow.log_metric("inertia", model.inertia_)
    
    # Log model
    mlflow.sklearn.log_model(model, "model")
    
    # Log artifacts
    mlflow.log_artifact("plots/clusters.png")
```

### Model Deployment Patterns
- **Batch prediction**: Scheduled model runs on new data
- **Real-time API**: REST API endpoints for online prediction
- **Streamlit apps**: Interactive web applications for model demos
- **Model registry**: Centralized storage and versioning of trained models

## Visualization & Reporting

### Plotting Standards
```python
# Matplotlib/Seaborn best practices
import matplotlib.pyplot as plt
import seaborn as sns

# Set style and context
sns.set_style("whitegrid")
sns.set_context("notebook", font_scale=1.1)

# Figure sizing and DPI
plt.figure(figsize=(10, 6), dpi=100)

# Clear titles and labels
plt.title("Customer Segmentation Analysis", fontsize=14, fontweight='bold')
plt.xlabel("Feature 1", fontsize=12)
plt.ylabel("Feature 2", fontsize=12)

# Save high-quality figures
plt.savefig('reports/figures/analysis.png', dpi=300, bbox_inches='tight')
```

### Dashboard Development
- **Streamlit**: Interactive dashboards for model exploration
- **Plotly Dash**: Complex interactive applications
- **Jupyter Widgets**: Interactive notebooks for stakeholder demos
- **Static reports**: Automated HTML reports with findings and recommendations

## Critical Rules

### Data Security & Privacy
- ⚠️ **NEVER** commit raw data files to version control
- ⚠️ **NEVER** include API keys or credentials in notebooks or code
- ⚠️ **ALWAYS** anonymize or pseudonymize personal data
- ⚠️ **ALWAYS** follow data governance and privacy regulations
- ⚠️ **NEVER** share sensitive data outside authorized environments
- ⚠️ **ALWAYS** use secure connections for data transfer

### Reproducibility Requirements
- ⚠️ **ALWAYS** set random seeds for all stochastic operations
- ⚠️ **ALWAYS** version control code, not just data
- ⚠️ **NEVER** modify raw data files - always create processed versions
- ⚠️ **ALWAYS** document data sources and processing steps
- ⚠️ **ALWAYS** use environment management (conda/pip requirements)
- ⚠️ **NEVER** hardcode file paths - use configuration files

### Model Development
- ⚠️ **ALWAYS** use proper train/validation/test splits
- ⚠️ **NEVER** use test data for model selection or hyperparameter tuning
- ⚠️ **ALWAYS** validate model assumptions and check for overfitting
- ⚠️ **ALWAYS** document model limitations and potential biases
- ⚠️ **NEVER** deploy models without proper evaluation and testing
- ⚠️ **ALWAYS** monitor model performance in production

### Code Quality
- ⚠️ **NEVER** write all code in notebooks - modularize into src/
- ⚠️ **ALWAYS** write unit tests for data processing functions
- ⚠️ **ALWAYS** handle missing data and edge cases gracefully
- ⚠️ **NEVER** ignore data quality issues or anomalies
- ⚠️ **ALWAYS** optimize code for performance with large datasets

## Common Commands Reference

### Daily Development
```bash
# Start development environment
conda activate project-name
jupyter lab

# Run data pipeline
python src/data/make_dataset.py
python src/features/build_features.py

# Train and evaluate model
python src/models/train_model.py --experiment baseline
python src/models/evaluate_model.py --model baseline

# Start MLflow tracking
mlflow ui

# Format and lint code
black src/ tests/ && flake8 src/ tests/
```

### Data Management
```bash
# DVC data versioning
dvc add data/raw/dataset.csv
dvc push
dvc pull

# Data validation
great_expectations suite new
great_expectations checkpoint run

# Database operations
python src/data/load_data.py --source postgres --table customers
```

### Model Operations
```bash
# Model training with different configurations
python src/models/train_model.py --config configs/baseline.yaml
python src/models/train_model.py --config configs/advanced.yaml

# Model deployment
python src/models/serve_model.py --model-path models/best_model.pkl
streamlit run src/visualization/dashboard.py
```

## Claude-Specific Instructions

### Code Generation Preferences
- **Always** include proper imports for data science libraries
- **Always** use pandas best practices for data manipulation
- **Prefer** scikit-learn patterns for model development
- **Include** proper error handling for data processing pipelines
- **Add** type hints and docstrings for all functions in src/
- **Use** logging for pipeline steps and model training progress
- **Follow** reproducible research practices with random seeds

### Notebook Development
- **Always** start notebooks with proper imports and configuration
- **Include** markdown cells explaining objectives and methodology
- **Use** consistent variable naming and clear cell organization
- **Add** data quality checks and exploratory analysis
- **Include** visualization of results and model performance
- **End** with clear conclusions and next steps

### Data Analysis Focus
- **Start** with exploratory data analysis (EDA) before modeling
- **Include** data quality assessment and missing value analysis
- **Use** appropriate statistical tests and validation methods
- **Consider** feature importance and model interpretability
- **Add** performance metrics appropriate for the problem type
- **Include** visualization of model results and data patterns

### MLOps Integration
- **Use** experiment tracking for all model training runs
- **Include** model versioning and artifact management
- **Add** data validation and monitoring capabilities
- **Consider** model deployment patterns and serving infrastructure
- **Include** A/B testing frameworks for model comparison
- **Add** automated retraining and model updating pipelines