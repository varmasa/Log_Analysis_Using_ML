import random
import pandas as pd

random.seed(42)

categories = {
    'Database': {
        'severity': ['High', 'Medium'],
        'logs': [
            'Connection timeout to DB server',
            'Database connection refused',
            'MySQL service unavailable',
            'PostgreSQL authentication failed',
            'ORA-12541 TNS no listener',
            'JDBC connection pool exhausted',
            'Database query execution timeout',
            'MongoDB replication failed',
            'Redis connection timeout',
            'Slow query execution detected'
        ],
        'root_causes': [
            'Database unavailable', 'Authentication failure',
            'Connection pool exhausted', 'Query timeout'
        ],
        'fixes': [
            'Restart DB service', 'Verify DB credentials',
            'Check DB connectivity', 'Optimize query performance'
        ]
    },
    'Jenkins': {
        'severity': ['High', 'Medium', 'Low'],
        'logs': [
            'Jenkins build failed',
            'Pipeline execution failed',
            'Git checkout failed in Jenkins',
            'Jenkins agent disconnected',
            'Artifact upload timeout',
            'Build aborted due to timeout',
            'Workspace cleanup failed'
        ],
        'root_causes': [
            'Pipeline script issue', 'Git authentication issue',
            'Agent unavailable', 'Dependency failure'
        ],
        'fixes': [
            'Check Jenkins logs', 'Reconnect Jenkins agent',
            'Verify Git access', 'Retry pipeline'
        ]
    },
    'Kubernetes': {
        'severity': ['High', 'Medium'],
        'logs': [
            'Pod CrashLoopBackOff',
            'ImagePullBackOff error occurred',
            'Node entered NotReady state',
            'Pod evicted due to memory pressure',
            'Helm deployment failed',
            'Ingress backend unavailable',
            'Failed scheduling pod'
        ],
        'root_causes': [
            'Container startup issue', 'Image pull failure',
            'Resource shortage', 'Node unavailable'
        ],
        'fixes': [
            'Check pod logs', 'Verify image registry',
            'Increase resources', 'Restart node'
        ]
    },
    'AWS': {
        'severity': ['High', 'Medium', 'Low'],
        'logs': [
            'EC2 instance failed status check',
            'RDS connection timeout',
            'IAM permission denied',
            'ALB target unhealthy',
            'Lambda function timeout',
            'CloudWatch agent stopped reporting',
            'S3 access denied'
        ],
        'root_causes': [
            'IAM issue', 'Instance failure',
            'Service unavailable', 'Timeout issue'
        ],
        'fixes': [
            'Check IAM permissions', 'Restart AWS resource',
            'Review CloudWatch logs', 'Verify networking'
        ]
    },
    'Docker': {
        'severity': ['High', 'Medium'],
        'logs': [
            'Docker daemon not running',
            'Container exited with code 137',
            'Failed to pull image from registry',
            'Port binding failed',
            'Docker build failed'
        ],
        'root_causes': [
            'Container crash', 'Registry issue',
            'Port conflict', 'Build issue'
        ],
        'fixes': [
            'Restart Docker service', 'Verify image URL',
            'Check container logs', 'Free conflicting port'
        ]
    },
    'Linux': {
        'severity': ['High', 'Medium'],
        'logs': [
            'Disk usage exceeded 95 percent',
            'Permission denied while executing script',
            'SSH connection timeout',
            'Kernel panic detected',
            'Cron job execution failed',
            'System load average too high'
        ],
        'root_causes': [
            'Disk full', 'Permission issue',
            'OS instability', 'CPU overload'
        ],
        'fixes': [
            'Clean disk space', 'Fix permissions',
            'Restart service', 'Investigate system logs'
        ]
    },
    'Monitoring': {
        'severity': ['Medium', 'Low'],
        'logs': [
            'Prometheus target down',
            'Grafana datasource unavailable',
            'Node exporter unavailable',
            'Alertmanager notification failed'
        ],
        'root_causes': [
            'Monitoring outage', 'Datasource failure'
        ],
        'fixes': [
            'Restart monitoring service', 'Check endpoint availability'
        ]
    },
    'Networking': {
        'severity': ['High', 'Medium'],
        'logs': [
            'DNS lookup failed',
            'Packet loss above threshold',
            'VPN tunnel disconnected',
            'SSL handshake failed',
            'Firewall blocked outgoing traffic'
        ],
        'root_causes': [
            'Network outage', 'DNS failure', 'Firewall rule issue'
        ],
        'fixes': [
            'Check firewall rules', 'Verify DNS config',
            'Restart network service'
        ]
    },
}

servers = ['dev-server-01', 'prod-server-02', 'qa-server-03', 'eks-node-01', 'jenkins-agent-01']
envs = ['DEV', 'QA', 'UAT', 'PROD']

rows = []
for _ in range(5000):
    category = random.choice(list(categories.keys()))
    data = categories[category]

    log_message = random.choice(data['logs'])
    severity = random.choice(data['severity'])
    root_cause = random.choice(data['root_causes'])
    fix = random.choice(data['fixes'])

    final_log = f"[{random.choice(envs)}] {random.choice(servers)} - {log_message}"

    rows.append([
        final_log,
        category,
        severity,
        root_cause,
        fix
    ])

columns = [
    'log_message',
    'category',
    'severity',
    'root_cause',
    'suggested_fix'
]

df = pd.DataFrame(rows, columns=columns)

# Save CSV
file_name = 'devops_logs_5000.csv'
df.to_csv(file_name, index=False)

print(f'Dataset generated successfully: {file_name}')
print(df.head())
