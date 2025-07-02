# Backup Strategy

Design and implement comprehensive backup and disaster recovery procedures for data protection and business continuity.

## Usage:
`/project:backup-strategy [--scope] [--frequency] [--retention]` or `/user:backup-strategy [--scope]`

## Process:
1. **Risk Assessment**: Identify critical data and potential failure scenarios
2. **RTO/RPO Planning**: Define Recovery Time Objective and Recovery Point Objective
3. **Backup Design**: Design multi-tier backup strategy with various methods
4. **Storage Planning**: Plan backup storage locations and redundancy
5. **Automation Setup**: Implement automated backup scheduling and monitoring
6. **Recovery Procedures**: Create step-by-step recovery documentation
7. **Testing Protocol**: Establish regular backup testing and validation
8. **Compliance Setup**: Ensure backup strategy meets regulatory requirements

## Backup Scope:
- **Database Backups**: Full, incremental, and transaction log backups
- **Application Data**: User uploads, configuration files, application state
- **Code Repository**: Source code, documentation, deployment scripts
- **Infrastructure**: Server configurations, security certificates, secrets
- **System State**: Operating system configurations, installed software

## Framework-Specific Strategies:
- **FastAPI**: Database backups, file storage, Redis state, configuration
- **Django**: Database, media files, static files, migration history
- **Flask**: Database, uploaded files, session storage, application config
- **Data Science**: Datasets, trained models, notebooks, experiment logs

## Arguments:
- `--scope`: Backup scope (database, files, full-system, application)
- `--frequency`: Backup frequency (hourly, daily, weekly, monthly)
- `--retention`: Retention policy (7days, 30days, 1year, compliance-based)
- `--storage`: Storage type (local, cloud, hybrid, offsite)

## Examples:
- `/project:backup-strategy` - Comprehensive backup strategy design
- `/project:backup-strategy --scope database --frequency daily` - Daily database backups
- `/project:backup-strategy --retention compliance-based` - Compliance-driven retention
- `/user:backup-strategy --storage hybrid` - Hybrid cloud/local backup strategy

## Backup Strategy Design:

### 3-2-1 Backup Rule:
- **3 copies** of important data (1 primary + 2 backups)
- **2 different storage types** (local + cloud, disk + tape)
- **1 offsite backup** (geographic separation)

### Backup Types:
```yaml
Full Backup:
  frequency: Weekly
  description: Complete copy of all data
  pros: Simple recovery, complete restore point
  cons: Large storage requirement, longer backup time

Incremental Backup:
  frequency: Daily
  description: Only changes since last backup
  pros: Fast backup, minimal storage
  cons: Complex recovery, dependency chain

Differential Backup:
  frequency: Daily
  description: Changes since last full backup
  pros: Faster recovery than incremental
  cons: Growing backup size

Transaction Log Backup:
  frequency: Every 15 minutes
  description: Database transaction logs
  pros: Point-in-time recovery
  cons: Database-specific, complex management
```

## Database Backup Implementation:

### PostgreSQL Automated Backup:
```bash
#!/bin/bash
# PostgreSQL backup script with rotation

DB_NAME="production_db"
DB_USER="backup_user"
BACKUP_DIR="/backups/postgresql"
RETENTION_DAYS=30

# Create backup directory
mkdir -p $BACKUP_DIR

# Create timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Full backup
pg_dump -h localhost -U $DB_USER -d $DB_NAME | gzip > \
  $BACKUP_DIR/full_backup_${TIMESTAMP}.sql.gz

# Incremental backup using WAL-E (Write Ahead Log)
wal-e backup-push $BACKUP_DIR/wal_backup_${TIMESTAMP}

# Cleanup old backups
find $BACKUP_DIR -name "*.sql.gz" -mtime +$RETENTION_DAYS -delete

# Upload to cloud storage
aws s3 sync $BACKUP_DIR s3://my-backup-bucket/postgresql/

# Verify backup integrity
if pg_restore --list $BACKUP_DIR/full_backup_${TIMESTAMP}.sql.gz > /dev/null; then
    echo "Backup verification successful"
    # Send success notification
    curl -X POST "https://hooks.slack.com/webhook" \
         -d '{"text":"Database backup completed successfully"}'
else
    echo "Backup verification failed"
    # Send failure alert
    curl -X POST "https://hooks.slack.com/webhook" \
         -d '{"text":"⚠️ Database backup verification FAILED"}'
fi
```

### MongoDB Backup Strategy:
```javascript
// MongoDB backup with sharding support
const { MongoClient } = require('mongodb');
const { spawn } = require('child_process');

class MongoBackupManager {
    constructor(config) {
        this.config = config;
        this.client = new MongoClient(config.connectionString);
    }
    
    async createBackup() {
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const backupPath = `${this.config.backupDir}/mongodb_backup_${timestamp}`;
        
        try {
            // For replica sets and sharded clusters
            const mongodump = spawn('mongodump', [
                '--uri', this.config.connectionString,
                '--out', backupPath,
                '--oplog',  // Include oplog for point-in-time recovery
                '--gzip'    // Compress output
            ]);
            
            mongodump.on('close', (code) => {
                if (code === 0) {
                    console.log('Backup completed successfully');
                    this.uploadToCloud(backupPath);
                    this.cleanOldBackups();
                } else {
                    console.error('Backup failed with code', code);
                    this.sendAlert('Backup failed');
                }
            });
            
        } catch (error) {
            console.error('Backup error:', error);
            this.sendAlert('Backup error: ' + error.message);
        }
    }
    
    async restoreFromBackup(backupPath, targetDb) {
        const mongorestore = spawn('mongorestore', [
            '--uri', this.config.connectionString,
            '--db', targetDb,
            '--oplogReplay',
            '--gzip',
            backupPath
        ]);
        
        return new Promise((resolve, reject) => {
            mongorestore.on('close', (code) => {
                if (code === 0) {
                    resolve('Restore completed successfully');
                } else {
                    reject(new Error(`Restore failed with code ${code}`));
                }
            });
        });
    }
}
```

## Application Backup Implementation:

### File System Backup:
```python
import os
import shutil
import tarfile
from datetime import datetime, timedelta
from pathlib import Path

class FileSystemBackup:
    """Backup application files and data."""
    
    def __init__(self, config):
        self.config = config
        self.backup_dir = Path(config['backup_directory'])
        self.retention_days = config.get('retention_days', 30)
    
    def create_backup(self, source_paths: list, backup_name: str = None):
        """Create compressed backup of specified paths."""
        if not backup_name:
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        backup_file = self.backup_dir / f"{backup_name}.tar.gz"
        
        with tarfile.open(backup_file, 'w:gz') as tar:
            for path in source_paths:
                if os.path.exists(path):
                    tar.add(path, arcname=os.path.basename(path))
                    print(f"Added {path} to backup")
        
        # Verify backup
        if self.verify_backup(backup_file):
            print(f"Backup created successfully: {backup_file}")
            return backup_file
        else:
            raise Exception("Backup verification failed")
    
    def verify_backup(self, backup_file: Path) -> bool:
        """Verify backup integrity."""
        try:
            with tarfile.open(backup_file, 'r:gz') as tar:
                # Check if archive can be read
                members = tar.getmembers()
                return len(members) > 0
        except Exception as e:
            print(f"Backup verification failed: {e}")
            return False
    
    def cleanup_old_backups(self):
        """Remove backups older than retention period."""
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)
        
        for backup_file in self.backup_dir.glob("backup_*.tar.gz"):
            if backup_file.stat().st_mtime < cutoff_date.timestamp():
                backup_file.unlink()
                print(f"Removed old backup: {backup_file}")
    
    def restore_backup(self, backup_file: Path, restore_path: Path):
        """Restore from backup file."""
        with tarfile.open(backup_file, 'r:gz') as tar:
            tar.extractall(path=restore_path)
        print(f"Restored backup to {restore_path}")
```

### Docker Volume Backup:
```bash
#!/bin/bash
# Docker volume backup script

CONTAINER_NAME="app_container"
VOLUME_NAME="app_data"
BACKUP_DIR="/backups/docker"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Create backup directory
mkdir -p $BACKUP_DIR

# Stop container (if needed for consistency)
docker stop $CONTAINER_NAME

# Create volume backup
docker run --rm \
  -v $VOLUME_NAME:/data \
  -v $BACKUP_DIR:/backup \
  alpine tar czf /backup/volume_backup_${TIMESTAMP}.tar.gz -C /data .

# Restart container
docker start $CONTAINER_NAME

# Upload to cloud storage
aws s3 cp $BACKUP_DIR/volume_backup_${TIMESTAMP}.tar.gz \
  s3://my-backup-bucket/docker-volumes/

echo "Docker volume backup completed: volume_backup_${TIMESTAMP}.tar.gz"
```

## Cloud Backup Integration:

### AWS S3 Backup:
```python
import boto3
from botocore.exceptions import ClientError

class S3BackupManager:
    """Manage backups in AWS S3."""
    
    def __init__(self, bucket_name, region='us-east-1'):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3', region_name=region)
    
    def upload_backup(self, local_file, s3_key):
        """Upload backup file to S3."""
        try:
            self.s3_client.upload_file(
                local_file, 
                self.bucket_name, 
                s3_key,
                ExtraArgs={
                    'ServerSideEncryption': 'AES256',
                    'StorageClass': 'STANDARD_IA'  # Infrequent Access for backups
                }
            )
            print(f"Backup uploaded to S3: s3://{self.bucket_name}/{s3_key}")
            return True
        except ClientError as e:
            print(f"Upload failed: {e}")
            return False
    
    def setup_lifecycle_policy(self):
        """Setup S3 lifecycle policy for backup retention."""
        lifecycle_config = {
            'Rules': [
                {
                    'ID': 'BackupRetentionPolicy',
                    'Status': 'Enabled',
                    'Filter': {'Prefix': 'backups/'},
                    'Transitions': [
                        {
                            'Days': 30,
                            'StorageClass': 'GLACIER'
                        },
                        {
                            'Days': 365,
                            'StorageClass': 'DEEP_ARCHIVE'
                        }
                    ],
                    'Expiration': {
                        'Days': 2555  # 7 years retention
                    }
                }
            ]
        }
        
        self.s3_client.put_bucket_lifecycle_configuration(
            Bucket=self.bucket_name,
            LifecycleConfiguration=lifecycle_config
        )
```

## Disaster Recovery Planning:

### Recovery Procedures:
```yaml
Disaster_Recovery_Plan:
  RTO: 4 hours  # Recovery Time Objective
  RPO: 15 minutes  # Recovery Point Objective
  
  Recovery_Steps:
    1. Assess_Damage:
       - Identify affected systems
       - Determine data loss extent
       - Evaluate infrastructure status
    
    2. Activate_DR_Site:
       - Start backup infrastructure
       - Configure network routing
       - Restore application services
    
    3. Data_Recovery:
       - Restore from latest full backup
       - Apply incremental backups
       - Verify data integrity
    
    4. Service_Restoration:
       - Start application services
       - Test functionality
       - Update DNS/load balancers
    
    5. Validation:
       - Run system health checks
       - Verify user access
       - Monitor performance
```

## Backup Monitoring:

### Automated Monitoring:
```python
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta

class BackupMonitor:
    """Monitor backup operations and send alerts."""
    
    def __init__(self, config):
        self.config = config
    
    def check_backup_freshness(self):
        """Check if recent backups exist."""
        backup_dir = Path(self.config['backup_directory'])
        now = datetime.now()
        
        # Check for backups in last 24 hours
        recent_backups = [
            f for f in backup_dir.glob("backup_*.tar.gz")
            if (now - datetime.fromtimestamp(f.stat().st_mtime)) < timedelta(hours=24)
        ]
        
        if not recent_backups:
            self.send_alert("No recent backups found!")
            return False
        
        return True
    
    def verify_backup_integrity(self, backup_file):
        """Verify backup can be read."""
        try:
            # Perform integrity check
            result = self.test_restore(backup_file)
            if not result:
                self.send_alert(f"Backup integrity check failed: {backup_file}")
            return result
        except Exception as e:
            self.send_alert(f"Backup verification error: {e}")
            return False
    
    def send_alert(self, message):
        """Send backup alert notification."""
        # Email notification
        msg = MIMEText(f"Backup Alert: {message}")
        msg['Subject'] = 'Backup System Alert'
        msg['From'] = self.config['alert_from']
        msg['To'] = self.config['alert_to']
        
        with smtplib.SMTP(self.config['smtp_server']) as server:
            server.send_message(msg)
        
        # Slack notification (if configured)
        if 'slack_webhook' in self.config:
            requests.post(self.config['slack_webhook'], 
                json={'text': f"🚨 {message}"})
```

## Validation Checklist:
- [ ] RTO and RPO requirements clearly defined
- [ ] Full, incremental, and differential backup strategies implemented
- [ ] 3-2-1 backup rule followed (3 copies, 2 media types, 1 offsite)
- [ ] Automated backup scheduling configured
- [ ] Backup integrity verification implemented
- [ ] Disaster recovery procedures documented and tested
- [ ] Backup monitoring and alerting operational
- [ ] Compliance requirements met (retention, encryption, audit trail)
- [ ] Recovery procedures tested regularly
- [ ] Team trained on backup and recovery processes

## Output:
- Comprehensive backup strategy documentation
- Automated backup scripts and schedules
- Disaster recovery procedures and runbooks
- Backup monitoring and alerting setup
- Cloud storage configuration and lifecycle policies
- Recovery testing protocols and schedules
- Compliance documentation and audit trails
- Emergency contact information and escalation procedures

## Notes:
- Test backup restoration regularly, not just backup creation
- Encrypt backups both in transit and at rest
- Document and practice disaster recovery procedures
- Consider compliance requirements (GDPR, HIPAA, SOX)
- Monitor backup storage costs and optimize retention policies
- Maintain multiple backup locations for geographic redundancy
- Keep backup procedures updated as systems evolve
- Train multiple team members on backup and recovery procedures