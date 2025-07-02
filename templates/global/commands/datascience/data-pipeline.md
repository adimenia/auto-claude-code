# Data Pipeline

Create robust ETL/ELT data pipelines with automated scheduling, monitoring, and error handling for scalable data processing.

## Usage:
`/project:data-pipeline [--pipeline-type] [--orchestrator] [--schedule]` or `/user:data-pipeline [--pipeline-type]`

## Process:
1. **Pipeline Architecture**: Design scalable pipeline architecture with clear stages
2. **Data Source Integration**: Connect to various data sources (databases, APIs, files)
3. **Transformation Logic**: Implement data cleaning, validation, and transformation steps
4. **Error Handling**: Add comprehensive error handling and retry mechanisms
5. **Scheduling Setup**: Configure automated pipeline execution with orchestration tools
6. **Monitoring Integration**: Add logging, metrics, and alerting for pipeline health
7. **Testing Framework**: Implement unit and integration tests for pipeline components
8. **Deployment Configuration**: Set up production deployment with CI/CD integration

## Pipeline Types:
- **ETL (Extract-Transform-Load)**: Traditional batch processing with staging area
- **ELT (Extract-Load-Transform)**: Load raw data first, transform in target system
- **Streaming**: Real-time data processing with event-driven architecture
- **Micro-batch**: Small batch processing with near real-time capabilities
- **Lambda Architecture**: Combination of batch and streaming for hybrid processing
- **Data Lake Pipeline**: Ingestion and organization of structured/unstructured data

## Framework-Specific Implementation:
- **Data Science**: Apache Airflow, Prefect, Luigi, Dagster orchestration
- **FastAPI**: Real-time data processing APIs with async capabilities
- **Django**: Data pipeline management interface with job scheduling
- **Flask**: Lightweight pipeline monitoring dashboard and controls

## Arguments:
- `--pipeline-type`: Pipeline type (etl, elt, streaming, micro-batch, lambda)
- `--orchestrator`: Orchestration tool (airflow, prefect, dagster, luigi, manual)
- `--schedule`: Pipeline schedule (hourly, daily, weekly, event-driven, manual)
- `--data-sources`: Source types (database, api, files, kafka, s3)

## Examples:
- `/project:data-pipeline --pipeline-type etl --orchestrator airflow` - ETL pipeline with Airflow
- `/project:data-pipeline --pipeline-type streaming --data-sources kafka` - Streaming pipeline
- `/project:data-pipeline --schedule daily --orchestrator prefect` - Daily batch pipeline
- `/user:data-pipeline --pipeline-type elt` - ELT pipeline with default configuration

## Apache Airflow Implementation:

### Complete Airflow DAG Setup:
```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.filesystem import FileSensor
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import Variable
import pandas as pd
import logging
import boto3
from typing import Dict, Any, List

# DAG Configuration
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(hours=2),
}

class DataPipelineDAG:
    """Comprehensive data pipeline using Apache Airflow."""
    
    def __init__(self, dag_id: str, description: str, schedule_interval: str):
        self.dag_id = dag_id
        self.dag = DAG(
            dag_id=dag_id,
            default_args=default_args,
            description=description,
            schedule_interval=schedule_interval,
            start_date=datetime(2024, 1, 1),
            catchup=False,
            tags=['data-pipeline', 'etl'],
            max_active_runs=1,
        )
        
    def extract_from_database(self, **context):
        """Extract data from source database."""
        try:
            # Get connection from Airflow connections
            postgres_hook = PostgresHook(postgres_conn_id='source_db')
            
            # Define extraction query
            sql_query = """
                SELECT * FROM sales_data 
                WHERE created_at >= %(start_date)s 
                AND created_at < %(end_date)s
            """
            
            # Get execution date for incremental loading
            execution_date = context['execution_date']
            start_date = execution_date
            end_date = execution_date + timedelta(days=1)
            
            # Execute query and get data
            df = postgres_hook.get_pandas_df(
                sql=sql_query,
                parameters={
                    'start_date': start_date,
                    'end_date': end_date
                }
            )
            
            # Save to temporary location
            temp_path = f"/tmp/extracted_data_{execution_date.strftime('%Y%m%d')}.csv"
            df.to_csv(temp_path, index=False)
            
            # Log extraction metrics
            logging.info(f"Extracted {len(df)} records from source database")
            
            # Store metadata in XCom
            context['task_instance'].xcom_push(
                key='extraction_metrics',
                value={
                    'record_count': len(df),
                    'file_path': temp_path,
                    'extraction_date': execution_date.isoformat()
                }
            )
            
            return temp_path
            
        except Exception as e:
            logging.error(f"Data extraction failed: {str(e)}")
            raise
    
    def transform_data(self, **context):
        """Transform and clean extracted data."""
        try:
            # Get file path from previous task
            extraction_metrics = context['task_instance'].xcom_pull(
                task_ids='extract_data',
                key='extraction_metrics'
            )
            
            file_path = extraction_metrics['file_path']
            df = pd.read_csv(file_path)
            
            # Data transformation steps
            df_transformed = self._perform_transformations(df)
            
            # Data quality validation
            quality_report = self._validate_data_quality(df_transformed)
            
            # Save transformed data
            transformed_path = file_path.replace('extracted', 'transformed')
            df_transformed.to_csv(transformed_path, index=False)
            
            # Store transformation metrics
            context['task_instance'].xcom_push(
                key='transformation_metrics',
                value={
                    'input_records': len(df),
                    'output_records': len(df_transformed),
                    'quality_score': quality_report['overall_score'],
                    'file_path': transformed_path
                }
            )
            
            logging.info(f"Transformed {len(df)} -> {len(df_transformed)} records")
            
            return transformed_path
            
        except Exception as e:
            logging.error(f"Data transformation failed: {str(e)}")
            raise
    
    def _perform_transformations(self, df: pd.DataFrame) -> pd.DataFrame:
        """Perform data transformations."""
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Handle missing values
        df = df.fillna({
            'amount': 0,
            'category': 'unknown',
            'customer_id': 'anonymous'
        })
        
        # Data type conversions
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        df['created_at'] = pd.to_datetime(df['created_at'])
        
        # Business logic transformations
        df['revenue_category'] = df['amount'].apply(
            lambda x: 'high' if x > 1000 else 'medium' if x > 100 else 'low'
        )
        
        # Add derived columns
        df['processing_date'] = datetime.now()
        df['month_year'] = df['created_at'].dt.to_period('M')
        
        return df
    
    def _validate_data_quality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validate data quality."""
        total_records = len(df)
        
        quality_checks = {
            'completeness': {
                'missing_amount': df['amount'].isnull().sum(),
                'missing_customer_id': df['customer_id'].isnull().sum(),
            },
            'validity': {
                'negative_amounts': (df['amount'] < 0).sum(),
                'future_dates': (df['created_at'] > datetime.now()).sum(),
            },
            'consistency': {
                'duplicate_count': df.duplicated().sum(),
            }
        }
        
        # Calculate overall quality score
        total_issues = sum([
            sum(quality_checks['completeness'].values()),
            sum(quality_checks['validity'].values()),
            sum(quality_checks['consistency'].values())
        ])
        
        quality_score = max(0, 100 - (total_issues / total_records * 100))
        
        return {
            'checks': quality_checks,
            'overall_score': quality_score,
            'total_records': total_records,
            'total_issues': total_issues
        }
    
    def load_to_warehouse(self, **context):
        """Load transformed data to data warehouse."""
        try:
            # Get transformation metrics
            transformation_metrics = context['task_instance'].xcom_pull(
                task_ids='transform_data',
                key='transformation_metrics'
            )
            
            file_path = transformation_metrics['file_path']
            df = pd.read_csv(file_path)
            
            # Load to data warehouse
            warehouse_hook = PostgresHook(postgres_conn_id='warehouse_db')
            
            # Use COPY for efficient bulk loading
            df.to_sql(
                name='sales_fact',
                con=warehouse_hook.get_sqlalchemy_engine(),
                if_exists='append',
                index=False,
                method='multi'
            )
            
            # Update metadata table
            self._update_pipeline_metadata(warehouse_hook, context)
            
            # Store loading metrics
            context['task_instance'].xcom_push(
                key='loading_metrics',
                value={
                    'records_loaded': len(df),
                    'table_name': 'sales_fact',
                    'load_timestamp': datetime.now().isoformat()
                }
            )
            
            logging.info(f"Loaded {len(df)} records to data warehouse")
            
            # Cleanup temporary files
            import os
            os.remove(file_path)
            os.remove(file_path.replace('transformed', 'extracted'))
            
        except Exception as e:
            logging.error(f"Data loading failed: {str(e)}")
            raise
    
    def _update_pipeline_metadata(self, hook: PostgresHook, context: Dict[str, Any]):
        """Update pipeline execution metadata."""
        metadata_sql = """
            INSERT INTO pipeline_executions 
            (dag_id, execution_date, status, records_processed, quality_score)
            VALUES (%(dag_id)s, %(execution_date)s, %(status)s, %(records)s, %(quality)s)
        """
        
        transformation_metrics = context['task_instance'].xcom_pull(
            task_ids='transform_data',
            key='transformation_metrics'
        )
        
        hook.run(
            sql=metadata_sql,
            parameters={
                'dag_id': context['dag'].dag_id,
                'execution_date': context['execution_date'],
                'status': 'success',
                'records': transformation_metrics['output_records'],
                'quality': transformation_metrics['quality_score']
            }
        )
    
    def send_notification(self, **context):
        """Send pipeline completion notification."""
        try:
            # Gather all metrics
            extraction_metrics = context['task_instance'].xcom_pull(
                task_ids='extract_data',
                key='extraction_metrics'
            )
            transformation_metrics = context['task_instance'].xcom_pull(
                task_ids='transform_data',
                key='transformation_metrics'
            )
            loading_metrics = context['task_instance'].xcom_pull(
                task_ids='load_data',
                key='loading_metrics'
            )
            
            # Create notification message
            message = f"""
            Pipeline Execution Summary:
            - DAG: {context['dag'].dag_id}
            - Execution Date: {context['execution_date']}
            - Records Extracted: {extraction_metrics['record_count']}
            - Records Transformed: {transformation_metrics['output_records']}
            - Records Loaded: {loading_metrics['records_loaded']}
            - Data Quality Score: {transformation_metrics['quality_score']:.2f}%
            - Status: Success
            """
            
            # Send notification (implement your preferred method)
            self._send_slack_notification(message)
            
            logging.info("Pipeline completion notification sent")
            
        except Exception as e:
            logging.error(f"Notification failed: {str(e)}")
            # Don't fail the pipeline for notification issues
    
    def _send_slack_notification(self, message: str):
        """Send Slack notification."""
        # Implement Slack notification
        # This is a placeholder - implement based on your setup
        pass
    
    def create_dag(self):
        """Create the complete DAG with all tasks."""
        
        # File sensor to wait for new data
        wait_for_data = FileSensor(
            task_id='wait_for_source_data',
            filepath='/data/source/trigger.txt',
            poke_interval=60,
            timeout=300,
            dag=self.dag
        )
        
        # Data extraction task
        extract_task = PythonOperator(
            task_id='extract_data',
            python_callable=self.extract_from_database,
            dag=self.dag
        )
        
        # Data transformation task
        transform_task = PythonOperator(
            task_id='transform_data',
            python_callable=self.transform_data,
            dag=self.dag
        )
        
        # Data loading task
        load_task = PythonOperator(
            task_id='load_data',
            python_callable=self.load_to_warehouse,
            dag=self.dag
        )
        
        # Data quality check
        quality_check = BashOperator(
            task_id='run_quality_checks',
            bash_command='python /opt/airflow/scripts/quality_check.py {{ ds }}',
            dag=self.dag
        )
        
        # Notification task
        notify_task = PythonOperator(
            task_id='send_notification',
            python_callable=self.send_notification,
            trigger_rule='all_done',  # Run even if upstream tasks fail
            dag=self.dag
        )
        
        # Define task dependencies
        wait_for_data >> extract_task >> transform_task >> load_task >> quality_check >> notify_task
        
        return self.dag

# Create DAG instance
sales_pipeline = DataPipelineDAG(
    dag_id='sales_data_pipeline',
    description='Daily ETL pipeline for sales data processing',
    schedule_interval='0 2 * * *'  # Daily at 2 AM
)

# Export DAG for Airflow
dag = sales_pipeline.create_dag()
```

### Streaming Pipeline with Apache Kafka:
```python
from kafka import KafkaConsumer, KafkaProducer
import json
import pandas as pd
from typing import Dict, Any
import logging
from datetime import datetime

class StreamingDataPipeline:
    """Real-time data pipeline using Apache Kafka."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.consumer = KafkaConsumer(
            config['source_topic'],
            bootstrap_servers=config['kafka_servers'],
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='latest',
            group_id=config['consumer_group']
        )
        self.producer = KafkaProducer(
            bootstrap_servers=config['kafka_servers'],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        
    def process_stream(self):
        """Process streaming data with real-time transformations."""
        try:
            for message in self.consumer:
                # Extract message data
                data = message.value
                
                # Transform data
                transformed_data = self.transform_message(data)
                
                # Validate data quality
                if self.validate_message(transformed_data):
                    # Send to output topic
                    self.producer.send(
                        self.config['output_topic'],
                        value=transformed_data
                    )
                    
                    # Update metrics
                    self.update_metrics(transformed_data)
                else:
                    # Send to error topic
                    self.producer.send(
                        self.config['error_topic'],
                        value={
                            'original_data': data,
                            'error': 'validation_failed',
                            'timestamp': datetime.now().isoformat()
                        }
                    )
                
        except Exception as e:
            logging.error(f"Stream processing error: {str(e)}")
            raise
    
    def transform_message(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform individual message."""
        # Add processing timestamp
        data['processed_at'] = datetime.now().isoformat()
        
        # Normalize fields
        if 'amount' in data:
            data['amount'] = float(data['amount'])
        
        # Add derived fields
        if 'user_id' in data and 'action' in data:
            data['event_key'] = f"{data['user_id']}_{data['action']}"
        
        return data
    
    def validate_message(self, data: Dict[str, Any]) -> bool:
        """Validate message data quality."""
        required_fields = ['user_id', 'timestamp', 'action']
        return all(field in data for field in required_fields)
    
    def update_metrics(self, data: Dict[str, Any]):
        """Update real-time metrics."""
        # Implement metrics collection (e.g., to InfluxDB, CloudWatch)
        pass
```

### Prefect Pipeline Alternative:
```python
from prefect import flow, task, get_run_logger
from prefect.task_runners import ConcurrentTaskRunner
import pandas as pd
from typing import List

@task(retries=3, retry_delay_seconds=60)
def extract_data(source_config: dict) -> pd.DataFrame:
    """Extract data from source system."""
    logger = get_run_logger()
    logger.info("Starting data extraction")
    
    # Implement data extraction logic
    # This is a placeholder
    df = pd.DataFrame({
        'id': range(1000),
        'value': range(1000),
        'category': ['A'] * 500 + ['B'] * 500
    })
    
    logger.info(f"Extracted {len(df)} records")
    return df

@task
def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transform extracted data."""
    logger = get_run_logger()
    logger.info("Starting data transformation")
    
    # Data transformations
    df_transformed = df.copy()
    df_transformed['value_doubled'] = df_transformed['value'] * 2
    df_transformed['processed_at'] = datetime.now()
    
    logger.info(f"Transformed {len(df_transformed)} records")
    return df_transformed

@task
def validate_data(df: pd.DataFrame) -> bool:
    """Validate data quality."""
    logger = get_run_logger()
    
    # Quality checks
    checks = {
        'no_nulls': df.isnull().sum().sum() == 0,
        'positive_values': (df['value'] >= 0).all(),
        'valid_categories': df['category'].isin(['A', 'B']).all()
    }
    
    all_passed = all(checks.values())
    logger.info(f"Data validation: {checks}")
    
    return all_passed

@task
def load_data(df: pd.DataFrame, destination_config: dict) -> int:
    """Load data to destination."""
    logger = get_run_logger()
    logger.info("Starting data loading")
    
    # Implement data loading logic
    # This is a placeholder
    records_loaded = len(df)
    
    logger.info(f"Loaded {records_loaded} records")
    return records_loaded

@flow(task_runner=ConcurrentTaskRunner())
def data_pipeline_flow(source_config: dict, destination_config: dict):
    """Main data pipeline flow."""
    logger = get_run_logger()
    logger.info("Starting data pipeline")
    
    # Extract data
    raw_data = extract_data(source_config)
    
    # Transform data
    transformed_data = transform_data(raw_data)
    
    # Validate data
    is_valid = validate_data(transformed_data)
    
    if is_valid:
        # Load data
        records_loaded = load_data(transformed_data, destination_config)
        logger.info(f"Pipeline completed successfully: {records_loaded} records")
    else:
        logger.error("Data validation failed - pipeline aborted")
        raise ValueError("Data quality validation failed")

# Pipeline configuration
if __name__ == "__main__":
    source_config = {"type": "database", "connection": "source_db"}
    destination_config = {"type": "warehouse", "connection": "warehouse_db"}
    
    data_pipeline_flow(source_config, destination_config)
```

## Validation Checklist:
- [ ] Pipeline architecture designed with clear stages and dependencies
- [ ] Data source connections configured and tested
- [ ] Transformation logic implemented with error handling
- [ ] Data quality validation integrated at each stage
- [ ] Orchestration tool configured with proper scheduling
- [ ] Monitoring and alerting set up for pipeline health
- [ ] Error handling and retry mechanisms implemented
- [ ] Testing framework covering unit and integration tests
- [ ] Documentation completed for all pipeline components
- [ ] Deployment and CI/CD integration configured

## Output:
- Complete pipeline architecture with orchestration tool configuration
- Data extraction, transformation, and loading modules
- Comprehensive error handling and retry mechanisms
- Monitoring dashboard with metrics and alerting
- Data quality validation framework
- Testing suite for pipeline components
- Deployment scripts and CI/CD integration
- Documentation and runbook for pipeline operations
- Performance optimization recommendations
- Scalability planning for future growth

## Notes:
- Choose orchestration tool based on team expertise and infrastructure
- Implement comprehensive logging and monitoring from day one
- Design for idempotency to handle reruns safely
- Use configuration files for environment-specific settings
- Plan for data schema evolution and backward compatibility
- Regular performance monitoring and optimization
- Implement proper secret management for credentials
- Consider data lineage tracking for compliance and debugging