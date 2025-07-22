# Airflow DAGs Examples

This repository contains a comprehensive collection of Apache Airflow DAG examples demonstrating various patterns, features, and best practices for workflow orchestration.

## Overview

The examples in this repository cover different aspects of Airflow development including:
- Asset-based workflows
- DAG triggering and chaining
- XCom data passing
- TaskFlow API usage
- Database operations
- File sensors
- Scheduling patterns
- Backfill operations

## DAG Examples

### 1. Asset-Based Workflow (`user_data_assets.py`)

Demonstrates Airflow's asset-based scheduling system where tasks are triggered based on data availability rather than time-based schedules.

**Key Features:**
- Source asset generating user data
- Transform assets for email extraction and domain parsing
- Sink asset combining multiple upstream data sources
- Asset dependencies and data lineage

**Assets:**
- `user_data`: Generates user information (source)
- `user_email`: Extracts email from user data
- `email_domain`: Parses domain from email
- `user_profile`: Creates complete user profile (sink)

### 2. Backfill and Catchup Examples

#### Backfill DAG (`backfill_dag.py`)
- Demonstrates manual backfill operations
- `catchup=False` to prevent automatic backfilling
- Command: `airflow backfill create --from-date 2025-06-06 --to-date 2025-06-08 --dag-id backfill_dag`

#### Catchup DAG (`catchup_dag.py`)
- Shows automatic catchup functionality
- `catchup=True` enables backfilling of missed runs
- Useful for ensuring data completeness

### 3. DAG Chaining and Triggering

#### Addition DAG (`dag_add.py`)
- Performs addition operation
- Uses `TriggerDagRunOperator` to trigger downstream DAG
- Passes results via XCom and DAG configuration
- Features deferrable task execution

#### Multiplication DAG (`dag_multiply.py`)
- Triggered by the addition DAG
- Receives data through DAG run configuration
- Demonstrates inter-DAG communication
- Pure trigger-based execution (`schedule=None`)

### 4. Scheduling Patterns

#### Cron Expression DAG (`dag_with_cron_expression.py`)
- Uses cron expression: `"0 3 * * Tue"` (3 AM on Tuesdays)
- Demonstrates advanced scheduling capabilities
- `catchup=True` for historical run processing

### 5. XCom Examples

#### Basic XCom (`hello_world_dag_v4.py`)
- Simple XCom data passing between tasks
- Parameter passing via `op_kwargs`
- Task dependency management

#### Multiple XCom (`multiple_xcoms_dag.py`)
- Multiple XCom values with custom keys
- Demonstrates complex data sharing patterns
- Key-based XCom retrieval

### 6. Database Operations

#### PostgreSQL Operator (`postgres_operator_dag.py`)
- Uses `SQLExecuteQueryOperator` for database operations
- Table creation and data selection
- Database connection management via `conn_id`

### 7. Python Dependencies

#### Dependency Management (`python_dependency_dag.py`)
- Demonstrates Python package usage in Airflow
- Version checking and validation
- Environment setup verification

### 8. File Sensors

#### Sensor Decorator (`sensor_decorator_demo_dag.py`)
- Modern sensor implementation using TaskFlow API
- File existence monitoring
- Configurable poke intervals and timeouts
- Best practices for sensor configuration

### 9. TaskFlow API

#### Modern DAG Definition (`taskflow_api_dag.py`)
- Uses `@task` decorator for cleaner code
- Multiple outputs handling
- Simplified data passing between tasks
- Pythonic DAG development approach

## Configuration Patterns

### Default Arguments
Common default arguments used across DAGs:
```python
default_args = {
    "owner": "seckindinc",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}
```

### DAG Configuration Best Practices
- `max_active_runs=1`: Prevents concurrent DAG runs
- `catchup=False`: Disables automatic backfilling (where appropriate)
- Proper start dates and scheduling
- Meaningful descriptions and tags

## Key Concepts Demonstrated

### 1. Asset-Based Scheduling
Modern approach to data pipeline orchestration where tasks run based on data availability rather than time schedules.

### 2. DAG Dependencies
- Task-level dependencies using `>>`
- Cross-DAG dependencies using `TriggerDagRunOperator`
- Data passing via XCom and DAG configurations

### 3. Error Handling and Retries
- Configurable retry policies
- Proper error handling in Python functions
- Input validation and fallback mechanisms

### 4. TaskFlow API Benefits
- Cleaner, more Pythonic code
- Automatic XCom handling
- Type hints and better IDE support
- Simplified task definition

### 5. Sensor Patterns
- File system monitoring
- Configurable polling intervals
- Timeout management
- Best practices for resource efficiency

## Usage Instructions

### Prerequisites
- Apache Airflow 3.x installed
- PostgreSQL connection configured (for database examples)
- Required Python packages installed

### Running the DAGs
1. Place DAG files in your Airflow DAGs directory
2. Ensure connections are properly configured
3. Enable DAGs in the Airflow UI
4. Monitor execution and logs

### Configuration Requirements
- PostgreSQL connection with ID `postgres` (for database examples)
- Appropriate file system permissions (for sensor examples)
- Python environment with required packages

## Best Practices Highlighted

1. **Asset-Based Design**: Use assets for data-driven workflows
2. **Error Handling**: Implement proper validation and fallbacks
3. **Resource Management**: Configure appropriate timeouts and intervals
4. **Documentation**: Use descriptive names, tags, and documentation
5. **Dependencies**: Clearly define task and DAG dependencies
6. **Testing**: Include validation logic in tasks
7. **Monitoring**: Use appropriate logging and error reporting

## File Structure
```
├── user_data_assets.py          # Asset-based workflow
├── backfill_dag.py              # Backfill operations
├── catchup_dag.py               # Catchup functionality
├── dag_add.py                   # Addition with DAG triggering
├── dag_multiply.py              # Multiplication (triggered)
├── dag_with_cron_expression.py  # Cron scheduling
├── hello_world_dag_v4.py        # Basic XCom usage
├── multiple_xcoms_dag.py        # Advanced XCom patterns
├── postgres_operator_dag.py     # Database operations
├── python_dependency_dag.py     # Dependency management
├── sensor_decorator_demo_dag.py # File sensors
└── taskflow_api_dag.py          # TaskFlow API patterns
```

## Contributing
When adding new DAG examples, ensure they:
- Follow established naming conventions
- Include proper documentation and comments
- Demonstrate specific Airflow features or patterns
- Include appropriate error handling
- Use meaningful tags and descriptions