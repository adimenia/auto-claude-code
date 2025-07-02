# Experiment Tracking

Implement comprehensive ML experiment tracking, versioning, and reproducibility with MLflow, Weights & Biases, or similar tools.

## Usage:
`/project:experiment-tracking [--platform] [--experiment-name] [--auto-logging]` or `/user:experiment-tracking [--platform]`

## Process:
1. **Platform Setup**: Configure experiment tracking platform and workspace
2. **Experiment Design**: Define experiment structure and metadata schema
3. **Auto-logging Integration**: Set up automatic parameter and metric logging
4. **Artifact Management**: Track models, datasets, and analysis outputs
5. **Version Control**: Implement data and model versioning strategies
6. **Comparison Tools**: Create experiment comparison and visualization dashboards
7. **Reproducibility Setup**: Ensure experiments can be reproduced consistently
8. **Collaboration Features**: Enable team collaboration and experiment sharing

## Tracking Platforms:
- **MLflow**: Open-source platform with tracking, projects, models, and registry
- **Weights & Biases**: Cloud-based with advanced visualization and collaboration
- **Neptune**: Enterprise-grade with extensive integrations and governance
- **TensorBoard**: TensorFlow-native with real-time monitoring
- **Comet**: Cloud platform with experiment optimization and team features
- **DVC**: Git-based data and model versioning with pipeline tracking

## Framework-Specific Integration:
- **Data Science**: Jupyter notebooks, Python scripts, R markdown integration
- **FastAPI**: API endpoint tracking, model serving monitoring
- **Django**: Web interface for experiment management and visualization
- **Flask**: Lightweight experiment dashboard and result sharing

## Arguments:
- `--platform`: Tracking platform (mlflow, wandb, neptune, tensorboard, comet, dvc)
- `--experiment-name`: Name for the experiment group or project
- `--auto-logging`: Enable automatic logging (sklearn, tensorflow, pytorch, xgboost)
- `--remote-tracking`: Use remote tracking server instead of local

## Examples:
- `/project:experiment-tracking --platform mlflow` - Setup MLflow tracking
- `/project:experiment-tracking --platform wandb --experiment-name customer-churn` - W&B for churn prediction
- `/project:experiment-tracking --auto-logging` - Enable automatic parameter/metric logging
- `/user:experiment-tracking --platform neptune --remote-tracking` - Remote Neptune setup

## MLflow Integration:

### Complete MLflow Setup:
```python
import mlflow
import mlflow.sklearn
import mlflow.tensorflow
import mlflow.pytorch
from mlflow.tracking import MlflowClient
import os
import json
from datetime import datetime
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional

class MLflowExperimentTracker:
    """Comprehensive MLflow experiment tracking setup."""
    
    def __init__(self, experiment_name: str, tracking_uri: str = None):
        self.experiment_name = experiment_name
        self.client = MlflowClient()
        
        # Set tracking URI (local or remote)
        if tracking_uri:
            mlflow.set_tracking_uri(tracking_uri)
        else:
            # Default to local SQLite database
            mlflow.set_tracking_uri("sqlite:///mlflow.db")
        
        # Create or get experiment
        try:
            self.experiment_id = mlflow.create_experiment(experiment_name)
        except Exception:
            self.experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id
        
        mlflow.set_experiment(experiment_name)
    
    def start_run(self, run_name: str = None, tags: Dict[str, str] = None):
        """Start a new MLflow run with optional tags."""
        if not run_name:
            run_name = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.active_run = mlflow.start_run(run_name=run_name, tags=tags)
        return self.active_run
    
    def log_environment_info(self):
        """Log environment and system information."""
        import platform
        import psutil
        import sys
        
        env_info = {
            "python_version": sys.version,
            "platform": platform.platform(),
            "cpu_count": psutil.cpu_count(),
            "memory_gb": round(psutil.virtual_memory().total / 1024**3, 2),
            "mlflow_version": mlflow.__version__
        }
        
        for key, value in env_info.items():
            mlflow.log_param(f"env_{key}", value)
    
    def log_dataset_info(self, data: pd.DataFrame, dataset_name: str = "training_data"):
        """Log dataset information and statistics."""
        dataset_info = {
            f"{dataset_name}_shape": f"{data.shape[0]}x{data.shape[1]}",
            f"{dataset_name}_memory_mb": round(data.memory_usage(deep=True).sum() / 1024**2, 2),
            f"{dataset_name}_missing_values": data.isnull().sum().sum(),
            f"{dataset_name}_numeric_features": len(data.select_dtypes(include=[np.number]).columns),
            f"{dataset_name}_categorical_features": len(data.select_dtypes(include=['object']).columns)
        }
        
        mlflow.log_params(dataset_info)
        
        # Log data profile as artifact
        profile_path = f"{dataset_name}_profile.json"
        data_profile = {
            "columns": data.columns.tolist(),
            "dtypes": data.dtypes.astype(str).to_dict(),
            "missing_values": data.isnull().sum().to_dict(),
            "basic_stats": data.describe().to_dict() if len(data.select_dtypes(include=[np.number]).columns) > 0 else {}
        }
        
        with open(profile_path, 'w') as f:
            json.dump(data_profile, f, indent=2)
        
        mlflow.log_artifact(profile_path, "data_profiles")
        os.remove(profile_path)  # Clean up local file
    
    def log_model_with_signature(self, model, model_name: str, X_sample: pd.DataFrame):
        """Log model with input/output signature for validation."""
        from mlflow.models.signature import infer_signature
        
        # Infer signature from sample data
        predictions = model.predict(X_sample.head(5))
        signature = infer_signature(X_sample, predictions)
        
        # Log model based on type
        if hasattr(model, 'fit') and hasattr(model, 'predict'):
            # Scikit-learn compatible model
            mlflow.sklearn.log_model(
                model, 
                model_name, 
                signature=signature,
                input_example=X_sample.head(3)
            )
        else:
            # Generic Python model
            mlflow.pyfunc.log_model(
                model_name,
                python_model=model,
                signature=signature,
                input_example=X_sample.head(3)
            )
    
    def log_hyperparameters(self, params: Dict[str, Any], prefix: str = ""):
        """Log hyperparameters with optional prefix."""
        formatted_params = {}
        for key, value in params.items():
            param_key = f"{prefix}_{key}" if prefix else key
            # MLflow params must be strings
            formatted_params[param_key] = str(value)
        
        mlflow.log_params(formatted_params)
    
    def log_metrics_over_time(self, metrics: Dict[str, float], step: int = None):
        """Log metrics with optional step for time series tracking."""
        for metric_name, value in metrics.items():
            mlflow.log_metric(metric_name, value, step=step)
    
    def log_feature_importance(self, feature_names: list, importance_values: list):
        """Log feature importance as both metrics and visualization."""
        # Log top features as metrics
        importance_dict = dict(zip(feature_names, importance_values))
        sorted_importance = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)
        
        # Log top 10 features as metrics
        for i, (feature, importance) in enumerate(sorted_importance[:10]):
            mlflow.log_metric(f"feature_importance_{i+1}_{feature}", importance)
        
        # Create and log feature importance plot
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(10, 8))
        features, importances = zip(*sorted_importance[:20])  # Top 20 features
        plt.barh(range(len(features)), importances)
        plt.yticks(range(len(features)), features)
        plt.xlabel('Importance')
        plt.title('Feature Importance')
        plt.tight_layout()
        
        importance_plot_path = "feature_importance.png"
        plt.savefig(importance_plot_path, dpi=300, bbox_inches='tight')
        mlflow.log_artifact(importance_plot_path, "visualizations")
        plt.close()
        os.remove(importance_plot_path)
    
    def log_confusion_matrix(self, y_true, y_pred, labels: list = None):
        """Log confusion matrix as artifact."""
        from sklearn.metrics import confusion_matrix
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        cm = confusion_matrix(y_true, y_pred, labels=labels)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=labels, yticklabels=labels)
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        
        cm_path = "confusion_matrix.png"
        plt.savefig(cm_path, dpi=300, bbox_inches='tight')
        mlflow.log_artifact(cm_path, "visualizations")
        plt.close()
        os.remove(cm_path)
    
    def compare_experiments(self, metric_name: str = "accuracy"):
        """Compare experiments and return results."""
        experiment = mlflow.get_experiment_by_name(self.experiment_name)
        runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])
        
        if runs.empty:
            return "No runs found in this experiment"
        
        # Sort by metric
        if f"metrics.{metric_name}" in runs.columns:
            best_runs = runs.nlargest(10, f"metrics.{metric_name}")
        else:
            best_runs = runs.head(10)
        
        return best_runs[['run_id', 'start_time', f'metrics.{metric_name}', 'status']]
```

### Weights & Biases Integration:
```python
import wandb
import pandas as pd
from typing import Dict, Any, Optional

class WandBExperimentTracker:
    """Weights & Biases experiment tracking integration."""
    
    def __init__(self, project_name: str, entity: str = None):
        self.project_name = project_name
        self.entity = entity
        self.run = None
        
        # Initialize W&B
        wandb.login()
    
    def start_run(self, run_name: str = None, config: Dict[str, Any] = None, 
                  tags: list = None, notes: str = None):
        """Start a new W&B run."""
        self.run = wandb.init(
            project=self.project_name,
            entity=self.entity,
            name=run_name,
            config=config,
            tags=tags,
            notes=notes,
            reinit=True
        )
        return self.run
    
    def log_dataset_table(self, data: pd.DataFrame, table_name: str = "dataset"):
        """Log dataset as W&B table for exploration."""
        # Sample data for large datasets
        sample_size = min(1000, len(data))
        sample_data = data.sample(n=sample_size) if len(data) > sample_size else data
        
        # Create W&B table
        table = wandb.Table(dataframe=sample_data)
        wandb.log({table_name: table})
    
    def log_model_with_metadata(self, model_path: str, model_name: str, 
                               metadata: Dict[str, Any]):
        """Log model as W&B artifact with metadata."""
        artifact = wandb.Artifact(
            name=model_name,
            type="model",
            metadata=metadata
        )
        artifact.add_file(model_path)
        wandb.log_artifact(artifact)
    
    def log_hyperparameter_sweep(self, sweep_config: Dict[str, Any]):
        """Set up hyperparameter sweep configuration."""
        sweep_id = wandb.sweep(sweep_config, project=self.project_name)
        return sweep_id
    
    def log_custom_chart(self, data: Dict[str, Any], chart_type: str = "line"):
        """Log custom visualizations."""
        if chart_type == "line":
            wandb.log(data)
        elif chart_type == "histogram":
            wandb.log({f"histogram_{key}": wandb.Histogram(value) 
                      for key, value in data.items()})
        elif chart_type == "scatter":
            # Assumes data has 'x' and 'y' keys
            table = wandb.Table(data=list(zip(data['x'], data['y'])), 
                               columns=["x", "y"])
            wandb.log({"scatter_plot": wandb.plot.scatter(table, "x", "y")})
    
    def finish_run(self):
        """Finish the current W&B run."""
        if self.run:
            wandb.finish()
```

### DVC Integration for Data Versioning:
```python
import subprocess
import json
import os
from pathlib import Path

class DVCDataVersioning:
    """Data Version Control integration for experiment tracking."""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.dvc_dir = self.project_root / '.dvc'
        
        if not self.dvc_dir.exists():
            self.init_dvc()
    
    def init_dvc(self):
        """Initialize DVC in the project."""
        subprocess.run(['dvc', 'init'], cwd=self.project_root, check=True)
        print("DVC initialized successfully")
    
    def add_data(self, data_path: str, remote_storage: str = None):
        """Add data file to DVC tracking."""
        subprocess.run(['dvc', 'add', data_path], cwd=self.project_root, check=True)
        
        if remote_storage:
            subprocess.run(['dvc', 'remote', 'add', '-d', 'storage', remote_storage], 
                          cwd=self.project_root, check=True)
        
        print(f"Data file {data_path} added to DVC tracking")
    
    def create_pipeline_stage(self, stage_name: str, command: str, 
                             dependencies: list, outputs: list):
        """Create a DVC pipeline stage."""
        stage_config = {
            'cmd': command,
            'deps': dependencies,
            'outs': outputs
        }
        
        subprocess.run(['dvc', 'stage', 'add', '-n', stage_name] + 
                      [f'--deps={dep}' for dep in dependencies] +
                      [f'--outs={out}' for out in outputs] +
                      [command], cwd=self.project_root, check=True)
        
        print(f"Pipeline stage '{stage_name}' created")
    
    def reproduce_pipeline(self):
        """Reproduce the entire DVC pipeline."""
        result = subprocess.run(['dvc', 'repro'], cwd=self.project_root, 
                               capture_output=True, text=True)
        print("Pipeline reproduction completed")
        return result.stdout
    
    def get_data_version(self, data_path: str):
        """Get the current version hash of a data file."""
        dvc_file = f"{data_path}.dvc"
        if os.path.exists(dvc_file):
            with open(dvc_file, 'r') as f:
                dvc_config = yaml.safe_load(f)
                return dvc_config['outs'][0]['md5']
        return None
```

### Automated Experiment Logging:
```python
import functools
import time
import traceback
from typing import Callable, Any

def track_experiment(experiment_name: str = None, auto_log: bool = True):
    """Decorator for automatic experiment tracking."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Extract experiment name from function name if not provided
            exp_name = experiment_name or f"experiment_{func.__name__}"
            
            tracker = MLflowExperimentTracker(exp_name)
            
            with tracker.start_run(run_name=func.__name__):
                try:
                    # Log function parameters
                    if kwargs:
                        tracker.log_hyperparameters(kwargs, prefix="func_param")
                    
                    # Log environment info
                    tracker.log_environment_info()
                    
                    # Record start time
                    start_time = time.time()
                    
                    # Execute function
                    result = func(*args, **kwargs)
                    
                    # Log execution time
                    execution_time = time.time() - start_time
                    mlflow.log_metric("execution_time_seconds", execution_time)
                    
                    # Log success
                    mlflow.log_metric("success", 1)
                    
                    return result
                    
                except Exception as e:
                    # Log failure
                    mlflow.log_metric("success", 0)
                    mlflow.log_param("error_type", type(e).__name__)
                    mlflow.log_text(traceback.format_exc(), "error_traceback.txt")
                    raise e
        
        return wrapper
    return decorator

# Usage example
@track_experiment("customer_churn_prediction")
def train_churn_model(data_path: str, model_type: str = "random_forest", 
                     test_size: float = 0.2):
    """Train customer churn prediction model with automatic tracking."""
    # Model training code here
    pass
```

### Experiment Comparison Dashboard:
```python
import streamlit as st
import mlflow
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def create_experiment_dashboard():
    """Create Streamlit dashboard for experiment comparison."""
    st.title("ML Experiment Tracking Dashboard")
    
    # Sidebar for experiment selection
    st.sidebar.header("Experiment Selection")
    
    # Get available experiments
    client = mlflow.tracking.MlflowClient()
    experiments = client.list_experiments()
    experiment_names = [exp.name for exp in experiments]
    
    selected_experiment = st.sidebar.selectbox(
        "Select Experiment", experiment_names
    )
    
    if selected_experiment:
        experiment = mlflow.get_experiment_by_name(selected_experiment)
        runs_df = mlflow.search_runs(experiment_ids=[experiment.experiment_id])
        
        if not runs_df.empty:
            # Main dashboard
            st.header(f"Experiment: {selected_experiment}")
            
            # Run summary table
            st.subheader("Run Summary")
            summary_cols = ['run_id', 'start_time', 'status'] + \
                          [col for col in runs_df.columns if col.startswith('metrics.')]
            
            st.dataframe(runs_df[summary_cols].head(10))
            
            # Metrics comparison
            st.subheader("Metrics Comparison")
            metric_columns = [col for col in runs_df.columns if col.startswith('metrics.')]
            
            if metric_columns:
                selected_metric = st.selectbox("Select Metric", metric_columns)
                
                # Create bar chart
                fig = px.bar(
                    runs_df.head(10), 
                    x='run_id', 
                    y=selected_metric,
                    title=f"{selected_metric} Comparison"
                )
                st.plotly_chart(fig)
            
            # Parameter distribution
            st.subheader("Parameter Distribution")
            param_columns = [col for col in runs_df.columns if col.startswith('params.')]
            
            if param_columns:
                selected_param = st.selectbox("Select Parameter", param_columns)
                
                if runs_df[selected_param].notna().any():
                    fig = px.histogram(
                        runs_df, 
                        x=selected_param,
                        title=f"{selected_param} Distribution"
                    )
                    st.plotly_chart(fig)

if __name__ == "__main__":
    create_experiment_dashboard()
```

## Validation Checklist:
- [ ] Experiment tracking platform configured and accessible
- [ ] Automatic parameter and metric logging implemented
- [ ] Data versioning and artifact tracking set up
- [ ] Model versioning with signatures and metadata
- [ ] Environment and system information logged
- [ ] Visualization and plotting integrated with tracking
- [ ] Experiment comparison and analysis tools available
- [ ] Collaboration features configured for team access
- [ ] Reproducibility ensured with proper versioning
- [ ] Dashboard or UI available for experiment monitoring

## Output:
- Configured experiment tracking platform (MLflow, W&B, etc.)
- Automated logging decorators and utility functions
- Data and model versioning system with DVC integration
- Experiment comparison dashboard and visualization tools
- Collaborative workspace for team experiment sharing
- Reproducible experiment configurations and environments
- Comprehensive logging of parameters, metrics, and artifacts
- Model registry with versioning and deployment tracking
- Data lineage and experiment lineage documentation
- Best practices guide for experiment management

## Notes:
- Choose tracking platform based on team size and requirements
- Implement consistent naming conventions for experiments and runs
- Regularly clean up and archive old experiments to manage storage
- Use tags and metadata effectively for experiment organization
- Set up automated alerts for experiment failures or anomalies
- Integrate tracking with CI/CD pipelines for automated experiments
- Regular backup of experiment data and metadata
- Train team members on experiment tracking best practices