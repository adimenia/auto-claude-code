# Data Migration

Create and manage database migrations, data transformations, and schema evolution strategies.

## Usage:
`/project:data-migration [--type] [--direction] [--dry-run]` or `/user:data-migration [--type]`

## Process:
1. **Migration Planning**: Analyze current schema and target requirements
2. **Backup Strategy**: Create comprehensive data backups before migration
3. **Migration Scripts**: Generate database-specific migration scripts
4. **Data Validation**: Implement pre and post-migration validation
5. **Rollback Planning**: Create rollback procedures for failed migrations
6. **Testing Strategy**: Test migrations in staging environment
7. **Execution Plan**: Create step-by-step execution plan with timing
8. **Monitoring Setup**: Implement migration progress monitoring and alerting

## Migration Types:
- **Schema Migration**: Table structure changes, indexes, constraints
- **Data Migration**: Moving data between systems or transforming data
- **Platform Migration**: Moving between different database systems
- **Version Migration**: Upgrading database engine versions
- **Cloud Migration**: Moving from on-premise to cloud databases

## Framework-Specific Migrations:
- **Django**: Django migrations with custom data migrations
- **FastAPI**: Alembic migrations with SQLAlchemy models
- **Flask**: Flask-Migrate with Alembic backend
- **Data Science**: Data pipeline migrations, ETL transformations

## Arguments:
- `--type`: Migration type (schema, data, platform, version, cloud)
- `--direction`: Migration direction (up, down, latest, specific-version)
- `--dry-run`: Preview migration without executing changes
- `--batch-size`: Batch size for large data migrations

## Examples:
- `/project:data-migration` - Create new migration based on model changes
- `/project:data-migration --type data --batch-size 1000` - Large data migration with batching
- `/project:data-migration --direction down --dry-run` - Preview rollback migration
- `/user:data-migration --type platform` - Cross-platform database migration

## Migration Planning:

### Schema Migration Example:
```python
# Django Migration
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        # Add new column with default value
        migrations.AddField(
            model_name='user',
            name='email_verified',
            field=models.BooleanField(default=False),
        ),
        
        # Create index for performance
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY idx_user_email ON myapp_user(email);",
            reverse_sql="DROP INDEX idx_user_email;"
        ),
        
        # Data migration function
        migrations.RunPython(
            code=migrate_user_data,
            reverse_code=reverse_migrate_user_data
        ),
    ]

def migrate_user_data(apps, schema_editor):
    """Migrate user data to new format."""
    User = apps.get_model('myapp', 'User')
    for user in User.objects.all():
        # Transform data logic here
        user.email_verified = '@' in user.email
        user.save()
```

### Alembic Migration (FastAPI/SQLAlchemy):
```python
"""Add user email verification

Revision ID: abc123
Revises: def456
Create Date: 2024-01-01 12:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

# revision identifiers
revision = 'abc123'
down_revision = 'def456'
branch_labels = None
depends_on = None

def upgrade():
    # Add new column
    op.add_column('users', 
        sa.Column('email_verified', sa.Boolean(), nullable=False, server_default='false')
    )
    
    # Create index
    op.create_index('idx_users_email', 'users', ['email'])
    
    # Data migration
    users_table = table('users',
        column('id', sa.Integer),
        column('email', sa.String),
        column('email_verified', sa.Boolean)
    )
    
    # Update existing records
    op.execute(
        users_table.update()
        .where(users_table.c.email.like('%@%'))
        .values(email_verified=True)
    )

def downgrade():
    op.drop_index('idx_users_email', 'users')
    op.drop_column('users', 'email_verified')
```

## Data Migration Strategies:

### Large Dataset Migration:
```python
import logging
from typing import Iterator, List
from dataclasses import dataclass

@dataclass
class MigrationProgress:
    total_records: int
    processed_records: int = 0
    failed_records: int = 0
    start_time: datetime = None
    
    @property
    def completion_percentage(self) -> float:
        return (self.processed_records / self.total_records) * 100

class BatchMigrator:
    """Handle large data migrations with batching and error recovery."""
    
    def __init__(self, batch_size: int = 1000, max_retries: int = 3):
        self.batch_size = batch_size
        self.max_retries = max_retries
        self.logger = logging.getLogger(__name__)
    
    def migrate_data(self, source_query, transform_func, target_model) -> MigrationProgress:
        """Migrate data in batches with error handling."""
        total_count = source_query.count()
        progress = MigrationProgress(total_records=total_count, start_time=datetime.now())
        
        for batch in self.get_batches(source_query):
            try:
                self.process_batch(batch, transform_func, target_model)
                progress.processed_records += len(batch)
                self.logger.info(f"Migration progress: {progress.completion_percentage:.1f}%")
                
            except Exception as e:
                self.logger.error(f"Batch migration failed: {e}")
                progress.failed_records += len(batch)
                
                if progress.failed_records > total_count * 0.1:  # 10% failure rate
                    raise Exception("Migration failure rate too high, aborting")
        
        return progress
    
    def get_batches(self, query) -> Iterator[List]:
        """Split query results into batches."""
        offset = 0
        while True:
            batch = query.offset(offset).limit(self.batch_size).all()
            if not batch:
                break
            yield batch
            offset += self.batch_size
```

### Cross-Platform Migration:
```python
class DatabaseMigrator:
    """Migrate data between different database platforms."""
    
    def __init__(self, source_db: str, target_db: str):
        self.source_engine = create_engine(source_db)
        self.target_engine = create_engine(target_db)
    
    def migrate_table(self, table_name: str, transform_func=None):
        """Migrate a single table between databases."""
        # Read data from source
        source_df = pd.read_sql_table(table_name, self.source_engine)
        
        # Apply transformations if needed
        if transform_func:
            source_df = transform_func(source_df)
        
        # Write to target database
        source_df.to_sql(
            table_name, 
            self.target_engine, 
            if_exists='append', 
            index=False,
            chunksize=1000
        )
    
    def migrate_schema(self, schema_mapping: dict):
        """Migrate entire schema with table mappings."""
        for source_table, target_config in schema_mapping.items():
            target_table = target_config.get('target_table', source_table)
            transform_func = target_config.get('transform_func')
            
            self.migrate_table(source_table, transform_func)
            print(f"Migrated {source_table} -> {target_table}")
```

## Backup and Recovery:

### Pre-Migration Backup:
```bash
# PostgreSQL backup
pg_dump -h localhost -U username -d database_name > backup_before_migration.sql

# MySQL backup  
mysqldump -h localhost -u username -p database_name > backup_before_migration.sql

# SQLite backup
cp database.db database_backup_$(date +%Y%m%d_%H%M%S).db
```

### Rollback Strategy:
```python
class MigrationRollback:
    """Handle migration rollbacks and recovery."""
    
    def __init__(self, migration_id: str):
        self.migration_id = migration_id
        self.backup_path = f"backups/migration_{migration_id}_backup.sql"
    
    def create_rollback_point(self):
        """Create a rollback point before migration."""
        # Create database backup
        self.create_backup()
        
        # Log migration start
        self.log_migration_start()
    
    def rollback_migration(self):
        """Rollback to pre-migration state."""
        try:
            # Restore from backup
            self.restore_backup()
            
            # Update migration tracking
            self.mark_migration_rolled_back()
            
            return True
        except Exception as e:
            logger.error(f"Rollback failed: {e}")
            return False
    
    def validate_rollback(self):
        """Validate that rollback was successful."""
        # Check data integrity
        # Verify expected state
        # Run validation queries
        pass
```

## Migration Testing:

### Test Environment Setup:
```python
class MigrationTester:
    """Test migrations in isolated environment."""
    
    def setUp(self):
        # Create test database
        self.test_db = create_test_database()
        
        # Load test data
        self.load_test_fixtures()
    
    def test_migration_forward(self):
        """Test migration in forward direction."""
        # Run migration
        result = self.run_migration('up')
        
        # Validate schema changes
        self.validate_schema()
        
        # Validate data integrity
        self.validate_data_integrity()
        
        assert result.success is True
    
    def test_migration_rollback(self):
        """Test migration rollback."""
        # Run migration forward
        self.run_migration('up')
        
        # Run rollback
        result = self.run_migration('down')
        
        # Validate original state restored
        self.validate_original_state()
        
        assert result.success is True
```

## Validation Checklist:
- [ ] Comprehensive backup created before migration
- [ ] Migration tested in staging environment
- [ ] Data integrity validation implemented
- [ ] Rollback procedures tested and documented
- [ ] Migration performance assessed for large datasets
- [ ] Index creation/updates planned for minimal downtime
- [ ] Application compatibility verified post-migration
- [ ] Monitoring and alerting configured for migration process

## Output:
- Database-specific migration scripts
- Data transformation and validation code
- Backup and recovery procedures
- Migration execution plan with timeline
- Rollback procedures and emergency contacts
- Performance optimization recommendations
- Testing suite for migration validation
- Documentation and post-migration verification steps

## Notes:
- Always test migrations in staging environment first
- Plan for downtime and communicate with stakeholders
- Monitor database performance during large migrations
- Use transactions where possible for atomicity
- Document all changes and provide rollback procedures
- Consider using online migration tools for zero-downtime
- Regular backup verification and recovery testing
- Keep migration scripts in version control