# Model Deployment

Deploy machine learning models to production with automated serving, versioning, A/B testing, and monitoring capabilities.

## Usage:
`/project:model-deployment [--platform] [--strategy] [--monitoring]` or `/user:model-deployment [--platform]`

## Process:
1. **Model Packaging**: Package trained models with dependencies and metadata
2. **Serving Infrastructure**: Set up scalable model serving infrastructure
3. **API Endpoints**: Create prediction APIs with authentication and rate limiting
4. **Version Management**: Implement model versioning and rollback capabilities
5. **A/B Testing**: Set up model comparison and gradual rollout strategies
6. **Performance Monitoring**: Monitor prediction latency, throughput, and accuracy
7. **Auto-scaling**: Configure automatic scaling based on traffic and performance
8. **Health Checks**: Implement model health monitoring and alerting

## Deployment Platforms:
- **Cloud Platforms**: AWS SageMaker, Google Cloud AI Platform, Azure ML
- **Container Orchestration**: Kubernetes, Docker Swarm, OpenShift
- **Serverless**: AWS Lambda, Google Cloud Functions, Azure Functions
- **Edge Deployment**: TensorFlow Lite, ONNX Runtime, edge computing platforms
- **Real-time Streaming**: Apache Kafka, Apache Pulsar, event-driven architectures
- **Batch Processing**: Apache Spark, Apache Beam, scheduled batch inference

## Framework-Specific Implementation:
- **Data Science**: MLflow Models, TensorFlow Serving, PyTorch Serve, Seldon Core
- **FastAPI**: High-performance ML APIs with async processing and caching
- **Django**: Model management interface with deployment orchestration
- **Flask**: Lightweight model serving with monitoring and logging

## Arguments:
- `--platform`: Deployment platform (sagemaker, kubernetes, serverless, edge)
- `--strategy`: Deployment strategy (blue-green, canary, rolling, shadow)
- `--monitoring`: Monitoring level (basic, comprehensive, real-time)
- `--scaling`: Auto-scaling configuration (cpu, memory, custom-metrics)

## Examples:
- `/project:model-deployment --platform kubernetes --strategy canary` - Kubernetes canary deployment
- `/project:model-deployment --platform sagemaker --monitoring comprehensive` - AWS SageMaker with full monitoring
- `/project:model-deployment --strategy blue-green --scaling cpu` - Blue-green deployment with CPU scaling
- `/user:model-deployment --platform serverless` - Serverless deployment configuration

## MLflow Model Deployment:

### Production Model Serving with MLflow:
```python
import mlflow
import mlflow.pyfunc
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from typing import Dict, Any, List
import logging
import time
from prometheus_client import Counter, Histogram, generate_latest
import os
from datetime import datetime

class MLflowModelServer:
    """Production MLflow model serving with monitoring and scaling."""
    
    def __init__(self, model_uri: str, model_name: str, model_version: str = None):
        self.model_uri = model_uri
        self.model_name = model_name
        self.model_version = model_version
        self.model = None
        self.load_model()
        
        # Monitoring metrics
        self.prediction_counter = Counter('ml_predictions_total', 'Total predictions', ['model', 'version'])
        self.prediction_latency = Histogram('ml_prediction_duration_seconds', 'Prediction latency', ['model', 'version'])
        self.error_counter = Counter('ml_prediction_errors_total', 'Prediction errors', ['model', 'version', 'error_type'])
        
        # Model metadata
        self.metadata = self.get_model_metadata()
        
    def load_model(self):
        """Load MLflow model with error handling."""
        try:
            if self.model_version:
                model_uri = f"models:/{self.model_name}/{self.model_version}"
            else:
                model_uri = self.model_uri
                
            self.model = mlflow.pyfunc.load_model(model_uri)
            logging.info(f"Model loaded successfully: {model_uri}")
            
        except Exception as e:
            logging.error(f"Failed to load model: {str(e)}")
            raise
    
    def get_model_metadata(self) -> Dict[str, Any]:
        """Get model metadata and signature."""
        try:
            if self.model_version:
                client = mlflow.tracking.MlflowClient()
                model_version = client.get_model_version(self.model_name, self.model_version)
                
                return {
                    "name": self.model_name,
                    "version": self.model_version,
                    "stage": model_version.current_stage,
                    "description": model_version.description,
                    "creation_timestamp": model_version.creation_timestamp,
                    "last_updated_timestamp": model_version.last_updated_timestamp,
                    "signature": str(self.model.metadata.signature) if self.model.metadata.signature else None
                }
        except Exception as e:
            logging.warning(f"Could not retrieve model metadata: {str(e)}")
            return {"name": self.model_name, "version": self.model_version or "latest"}
    
    def validate_input(self, data: Dict[str, Any]) -> pd.DataFrame:
        """Validate and prepare input data."""
        try:
            # Convert to DataFrame
            if isinstance(data, dict):
                if 'instances' in data:
                    df = pd.DataFrame(data['instances'])
                elif 'data' in data:
                    df = pd.DataFrame(data['data'])
                else:
                    df = pd.DataFrame([data])
            else:
                df = pd.DataFrame(data)
            
            # Validate against model signature if available
            if self.model.metadata.signature:
                signature = self.model.metadata.signature
                expected_columns = [input.name for input in signature.inputs.inputs]
                
                missing_columns = set(expected_columns) - set(df.columns)
                if missing_columns:
                    raise ValueError(f"Missing required columns: {missing_columns}")
                
                # Select only expected columns in correct order
                df = df[expected_columns]
            
            return df
            
        except Exception as e:
            self.error_counter.labels(
                model=self.model_name, 
                version=self.model_version or "latest",
                error_type="validation_error"
            ).inc()
            raise ValueError(f"Input validation failed: {str(e)}")
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make predictions with monitoring and error handling."""
        start_time = time.time()
        
        try:
            # Validate input
            input_df = self.validate_input(data)
            
            # Make prediction
            predictions = self.model.predict(input_df)
            
            # Format output
            if isinstance(predictions, np.ndarray):
                if predictions.ndim == 1:
                    predictions = predictions.tolist()
                else:
                    predictions = [pred.tolist() if isinstance(pred, np.ndarray) else pred for pred in predictions]
            
            # Record metrics
            self.prediction_counter.labels(
                model=self.model_name, 
                version=self.model_version or "latest"
            ).inc()
            
            latency = time.time() - start_time
            self.prediction_latency.labels(
                model=self.model_name, 
                version=self.model_version or "latest"
            ).observe(latency)
            
            return {
                "predictions": predictions,
                "model_name": self.model_name,
                "model_version": self.model_version or "latest",
                "prediction_time": datetime.now().isoformat(),
                "latency_seconds": round(latency, 4)
            }
            
        except Exception as e:
            self.error_counter.labels(
                model=self.model_name, 
                version=self.model_version or "latest",
                error_type=type(e).__name__
            ).inc()
            
            logging.error(f"Prediction failed: {str(e)}")
            raise
    
    def health_check(self) -> Dict[str, Any]:
        """Check model health and readiness."""
        try:
            # Simple prediction with dummy data to test model
            if self.model.metadata.signature:
                dummy_data = {}
                for input_spec in self.model.metadata.signature.inputs.inputs:
                    if input_spec.type.name == "double":
                        dummy_data[input_spec.name] = 0.0
                    elif input_spec.type.name == "long":
                        dummy_data[input_spec.name] = 0
                    else:
                        dummy_data[input_spec.name] = "test"
                
                test_df = pd.DataFrame([dummy_data])
                _ = self.model.predict(test_df)
            
            return {
                "status": "healthy",
                "model_name": self.model_name,
                "model_version": self.model_version or "latest",
                "metadata": self.metadata,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


# Flask Application for Model Serving
app = Flask(__name__)

# Initialize model server
MODEL_URI = os.getenv("MODEL_URI", "models:/my-model/latest")
MODEL_NAME = os.getenv("MODEL_NAME", "my-model")
MODEL_VERSION = os.getenv("MODEL_VERSION")

model_server = MLflowModelServer(MODEL_URI, MODEL_NAME, MODEL_VERSION)

@app.route('/predict', methods=['POST'])
def predict():
    """Prediction endpoint."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        result = model_server.predict(data)
        return jsonify(result)
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    health_status = model_server.health_check()
    status_code = 200 if health_status["status"] == "healthy" else 503
    return jsonify(health_status), status_code

@app.route('/metadata', methods=['GET'])
def metadata():
    """Model metadata endpoint."""
    return jsonify(model_server.metadata)

@app.route('/metrics', methods=['GET'])
def metrics():
    """Prometheus metrics endpoint."""
    return generate_latest()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Kubernetes Deployment Configuration:
```yaml
# model-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-model-server
  labels:
    app: ml-model-server
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ml-model-server
  template:
    metadata:
      labels:
        app: ml-model-server
        version: v1
    spec:
      containers:
      - name: model-server
        image: ml-model-server:latest
        ports:
        - containerPort: 5000
        env:
        - name: MODEL_URI
          value: "models:/customer-churn/production"
        - name: MODEL_NAME
          value: "customer-churn"
        - name: MODEL_VERSION
          value: "3"
        - name: MLFLOW_TRACKING_URI
          value: "http://mlflow-server:5000"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: ml-model-service
spec:
  selector:
    app: ml-model-server
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
  type: LoadBalancer

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ml-model-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ml-model-server
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### AWS SageMaker Deployment:
```python
import boto3
import sagemaker
from sagemaker.mlflow import MLflowModel
from sagemaker.model_monitor import DataCaptureConfig
from datetime import datetime

class SageMakerDeployment:
    """Deploy MLflow models to AWS SageMaker."""
    
    def __init__(self, role_arn: str, region: str = "us-east-1"):
        self.role = role_arn
        self.region = region
        self.sagemaker_session = sagemaker.Session()
        self.sm_client = boto3.client('sagemaker', region_name=region)
        
    def deploy_model(self, model_uri: str, model_name: str, 
                    instance_type: str = "ml.m5.large",
                    instance_count: int = 1,
                    enable_data_capture: bool = True) -> str:
        """Deploy MLflow model to SageMaker endpoint."""
        
        # Create MLflow model
        mlflow_model = MLflowModel(
            model_uri=model_uri,
            role=self.role,
            sagemaker_session=self.sagemaker_session
        )
        
        # Configure data capture for monitoring
        data_capture_config = None
        if enable_data_capture:
            data_capture_config = DataCaptureConfig(
                enable_capture=True,
                sampling_percentage=100,
                destination_s3_uri=f"s3://ml-model-monitoring/{model_name}/data-capture"
            )
        
        # Deploy to endpoint
        endpoint_name = f"{model_name}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        predictor = mlflow_model.deploy(
            initial_instance_count=instance_count,
            instance_type=instance_type,
            endpoint_name=endpoint_name,
            data_capture_config=data_capture_config,
            wait=True
        )
        
        return endpoint_name
    
    def create_auto_scaling(self, endpoint_name: str, variant_name: str = "AllTraffic"):
        """Configure auto-scaling for the endpoint."""
        
        # Register scalable target
        autoscaling_client = boto3.client('application-autoscaling', region_name=self.region)
        
        resource_id = f"endpoint/{endpoint_name}/variant/{variant_name}"
        
        autoscaling_client.register_scalable_target(
            ServiceNamespace='sagemaker',
            ResourceId=resource_id,
            ScalableDimension='sagemaker:variant:DesiredInstanceCount',
            MinCapacity=1,
            MaxCapacity=10,
            RoleARN=self.role
        )
        
        # Create scaling policy
        autoscaling_client.put_scaling_policy(
            PolicyName=f"{endpoint_name}-scaling-policy",
            ServiceNamespace='sagemaker',
            ResourceId=resource_id,
            ScalableDimension='sagemaker:variant:DesiredInstanceCount',
            PolicyType='TargetTrackingScaling',
            TargetTrackingScalingPolicyConfiguration={
                'TargetValue': 70.0,
                'PredefinedMetricSpecification': {
                    'PredefinedMetricType': 'SageMakerVariantInvocationsPerInstance'
                },
                'ScaleOutCooldown': 300,
                'ScaleInCooldown': 300
            }
        )
```

### A/B Testing Framework:
```python
import random
from typing import Dict, Any, Optional
import logging
from dataclasses import dataclass
from enum import Enum

class TrafficSplitStrategy(Enum):
    RANDOM = "random"
    CANARY = "canary"
    BLUE_GREEN = "blue_green"

@dataclass
class ModelVariant:
    """Model variant configuration."""
    name: str
    model_uri: str
    traffic_percentage: float
    metadata: Dict[str, Any] = None

class ABTestingFramework:
    """A/B testing framework for model deployment."""
    
    def __init__(self, strategy: TrafficSplitStrategy = TrafficSplitStrategy.RANDOM):
        self.strategy = strategy
        self.variants: List[ModelVariant] = []
        self.metrics_collector = MetricsCollector()
        
    def add_variant(self, variant: ModelVariant):
        """Add a model variant to the test."""
        # Validate traffic percentages
        total_traffic = sum(v.traffic_percentage for v in self.variants) + variant.traffic_percentage
        if total_traffic > 100:
            raise ValueError("Total traffic percentage cannot exceed 100%")
        
        self.variants.append(variant)
        logging.info(f"Added variant {variant.name} with {variant.traffic_percentage}% traffic")
    
    def route_request(self, request_id: str = None) -> ModelVariant:
        """Route request to appropriate model variant."""
        if not self.variants:
            raise ValueError("No variants configured")
        
        if self.strategy == TrafficSplitStrategy.RANDOM:
            return self._random_routing()
        elif self.strategy == TrafficSplitStrategy.CANARY:
            return self._canary_routing()
        elif self.strategy == TrafficSplitStrategy.BLUE_GREEN:
            return self._blue_green_routing()
    
    def _random_routing(self) -> ModelVariant:
        """Random traffic splitting based on percentages."""
        random_value = random.uniform(0, 100)
        cumulative_percentage = 0
        
        for variant in self.variants:
            cumulative_percentage += variant.traffic_percentage
            if random_value <= cumulative_percentage:
                return variant
        
        # Fallback to first variant
        return self.variants[0]
    
    def _canary_routing(self) -> ModelVariant:
        """Canary deployment routing."""
        # Route small percentage to canary, rest to stable
        canary_variants = [v for v in self.variants if v.metadata and v.metadata.get("type") == "canary"]
        stable_variants = [v for v in self.variants if not (v.metadata and v.metadata.get("type") == "canary")]
        
        if canary_variants:
            canary_traffic = sum(v.traffic_percentage for v in canary_variants)
            if random.uniform(0, 100) <= canary_traffic:
                return random.choice(canary_variants)
        
        return random.choice(stable_variants) if stable_variants else self.variants[0]
    
    def _blue_green_routing(self) -> ModelVariant:
        """Blue-green deployment routing."""
        active_variants = [v for v in self.variants if v.metadata and v.metadata.get("active", True)]
        return random.choice(active_variants) if active_variants else self.variants[0]

class MetricsCollector:
    """Collect and compare metrics across model variants."""
    
    def __init__(self):
        self.metrics = {}
    
    def record_prediction(self, variant_name: str, latency: float, 
                         prediction: Any, actual: Any = None):
        """Record prediction metrics for a variant."""
        if variant_name not in self.metrics:
            self.metrics[variant_name] = {
                "predictions": 0,
                "total_latency": 0,
                "errors": 0,
                "accuracy_sum": 0
            }
        
        self.metrics[variant_name]["predictions"] += 1
        self.metrics[variant_name]["total_latency"] += latency
        
        if actual is not None:
            # Calculate accuracy for classification or error for regression
            if isinstance(actual, (int, str)):  # Classification
                if prediction == actual:
                    self.metrics[variant_name]["accuracy_sum"] += 1
            else:  # Regression
                error = abs(prediction - actual)
                self.metrics[variant_name]["accuracy_sum"] += error
    
    def get_comparison_report(self) -> Dict[str, Any]:
        """Generate comparison report across variants."""
        report = {}
        
        for variant_name, metrics in self.metrics.items():
            avg_latency = metrics["total_latency"] / max(metrics["predictions"], 1)
            accuracy = metrics["accuracy_sum"] / max(metrics["predictions"], 1)
            
            report[variant_name] = {
                "predictions": metrics["predictions"],
                "avg_latency_seconds": round(avg_latency, 4),
                "accuracy": round(accuracy, 4),
                "error_rate": metrics["errors"] / max(metrics["predictions"], 1)
            }
        
        return report
```

## Validation Checklist:
- [ ] Model packaging completed with all dependencies and metadata
- [ ] Serving infrastructure configured and tested
- [ ] API endpoints implemented with proper authentication and rate limiting
- [ ] Model versioning and rollback capabilities implemented
- [ ] A/B testing framework configured for model comparison
- [ ] Performance monitoring set up with latency and throughput tracking
- [ ] Auto-scaling configured based on traffic and resource utilization
- [ ] Health checks and alerting implemented for model availability
- [ ] Security measures applied (HTTPS, authentication, input validation)
- [ ] Documentation completed for deployment and operations

## Output:
- Production-ready model serving infrastructure
- Scalable API endpoints with authentication and monitoring
- Model versioning system with rollback capabilities
- A/B testing framework for gradual model rollout
- Comprehensive monitoring dashboard with performance metrics
- Auto-scaling configuration based on traffic patterns
- Health check and alerting system for operational monitoring
- Security-hardened deployment with input validation
- Deployment automation scripts and CI/CD integration
- Operations runbook for model management and troubleshooting

## Notes:
- Choose deployment platform based on scalability and latency requirements
- Implement proper model versioning to enable safe rollbacks
- Monitor model performance continuously for drift detection
- Use A/B testing for safe model updates and comparison
- Implement proper security measures for production environments
- Plan for disaster recovery and backup strategies
- Regular performance optimization and capacity planning
- Maintain comprehensive logging for debugging and auditing