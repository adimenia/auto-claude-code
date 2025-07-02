# Load Test

Generate and execute comprehensive load testing scenarios to validate application performance under various traffic conditions.

## Usage:
`/project:load-test [--scenario] [--tool] [--duration]` or `/user:load-test [--scenario]`

## Process:
1. **Test Planning**: Define load testing objectives and success criteria
2. **Scenario Design**: Create realistic user journey and traffic patterns
3. **Test Environment**: Set up isolated testing environment matching production
4. **Baseline Measurement**: Establish performance baselines before testing
5. **Load Test Execution**: Run progressive load testing scenarios
6. **Real-time Monitoring**: Monitor application and infrastructure metrics
7. **Results Analysis**: Analyze performance data and identify bottlenecks
8. **Report Generation**: Create comprehensive performance testing report

## Load Testing Scenarios:
- **Smoke Test**: Verify basic functionality with minimal load
- **Load Test**: Normal expected traffic patterns
- **Stress Test**: Beyond normal capacity to find breaking points
- **Spike Test**: Sudden traffic increases and decreases
- **Volume Test**: Large amounts of data processing
- **Endurance Test**: Extended periods of normal load

## Framework-Specific Testing:
- **FastAPI**: API endpoint testing, async performance, WebSocket load
- **Django**: View performance, ORM behavior under load, admin interface
- **Flask**: Blueprint performance, template rendering, session handling
- **Data Science**: Model inference performance, batch processing, data pipeline load
- **CLI Tools**: Concurrent execution, file processing, resource consumption

## Arguments:
- `--scenario`: Test scenario (smoke, load, stress, spike, volume, endurance)
- `--tool`: Testing tool (locust, k6, artillery, jmeter, wrk)
- `--duration`: Test duration (30s, 5m, 1h, 24h)
- `--users`: Virtual user count and ramp-up pattern

## Examples:
- `/project:load-test` - Basic load test with default parameters
- `/project:load-test --scenario stress --users 1000` - Stress test with 1000 users
- `/project:load-test --tool k6 --duration 10m` - 10-minute test using k6
- `/user:load-test --scenario spike` - Spike testing for traffic bursts

## Testing Tools Configuration:

### Locust (Python):
```python
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Login or setup tasks"""
        self.client.post("/auth/login", json={
            "username": "test_user",
            "password": "test_pass"
        })
    
    @task(3)
    def view_homepage(self):
        self.client.get("/")
    
    @task(2)
    def view_profile(self):
        self.client.get("/profile")
    
    @task(1)
    def create_post(self):
        self.client.post("/posts", json={
            "title": "Load Test Post",
            "content": "This is a test post"
        })
```

### k6 (JavaScript):
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  scenarios: {
    load_test: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 100 },
        { duration: '5m', target: 100 },
        { duration: '2m', target: 200 },
        { duration: '5m', target: 200 },
        { duration: '2m', target: 0 },
      ],
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.1'],
  },
};

export default function() {
  const response = http.get('http://localhost:8000/api/users');
  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1);
}
```

### Artillery (YAML):
```yaml
config:
  target: 'http://localhost:8000'
  phases:
    - duration: 60
      arrivalRate: 10
      name: "Warm up"
    - duration: 300
      arrivalRate: 50
      name: "Sustained load"
    - duration: 60
      arrivalRate: 100
      name: "Peak load"
  processor: "./test-functions.js"

scenarios:
  - name: "User Journey"
    weight: 70
    flow:
      - post:
          url: "/auth/login"
          json:
            username: "test_user"
            password: "test_pass"
      - get:
          url: "/dashboard"
      - think: 2
      - get:
          url: "/api/data"

  - name: "API Only"
    weight: 30
    flow:
      - get:
          url: "/api/health"
      - get:
          url: "/api/metrics"
```

## Performance Metrics:
- **Response Time**: Average, median, 95th percentile, 99th percentile
- **Throughput**: Requests per second, transactions per minute
- **Error Rate**: HTTP errors, application errors, timeouts
- **Resource Usage**: CPU, memory, disk I/O, network bandwidth
- **Scalability**: Performance degradation under increasing load

## Test Scenarios Configuration:

### Progressive Load Testing:
```yaml
scenarios:
  smoke_test:
    users: 1-5
    duration: 1m
    purpose: Verify basic functionality
    
  load_test:
    users: 10-100
    duration: 10m
    purpose: Normal expected load
    
  stress_test:
    users: 100-500
    duration: 15m
    purpose: Find breaking point
    
  spike_test:
    pattern: "0→200→0→500→0"
    duration: 5m
    purpose: Sudden traffic changes
    
  endurance_test:
    users: 50
    duration: 2h
    purpose: Memory leaks, degradation
```

## Monitoring Integration:
- **Application Metrics**: Response times, error rates, throughput
- **Infrastructure Metrics**: CPU, memory, disk, network usage
- **Database Metrics**: Connection pools, query performance, locks
- **Custom Metrics**: Business KPIs, user experience metrics

## Results Analysis:

### Performance Thresholds:
```python
PERFORMANCE_THRESHOLDS = {
    'response_time': {
        'p50': 100,  # ms
        'p95': 500,  # ms
        'p99': 1000, # ms
    },
    'error_rate': 0.01,  # 1%
    'throughput': {
        'min': 100,  # req/s
        'target': 500,  # req/s
    },
    'resource_usage': {
        'cpu': 80,    # %
        'memory': 85, # %
        'disk_io': 90 # %
    }
}
```

### Bottleneck Identification:
- Database connection exhaustion
- Memory leaks and garbage collection
- CPU-intensive operations
- Network bandwidth limitations
- Third-party service dependencies

## Validation Checklist:
- [ ] Test environment matches production specifications
- [ ] Realistic user scenarios and data volumes configured
- [ ] Performance thresholds defined and documented
- [ ] All load testing scenarios executed successfully
- [ ] Infrastructure monitoring captured during tests
- [ ] Performance bottlenecks identified and documented
- [ ] Test results analyzed and recommendations provided
- [ ] Load testing integrated into CI/CD pipeline

## Output:
- Comprehensive load testing report with metrics and graphs
- Performance threshold compliance analysis
- Bottleneck identification and impact assessment
- Scalability recommendations and capacity planning
- Test script configurations for automated testing
- Monitoring dashboard for ongoing performance tracking
- Performance regression test suite
- Load testing best practices and guidelines

## Notes:
- Always test in an environment similar to production
- Start with smoke tests before running full load tests
- Monitor both application and infrastructure metrics
- Consider geographic distribution of users in test scenarios
- Regular load testing as part of development cycle
- Coordinate with infrastructure team for large-scale tests
- Document and version test scenarios for repeatability
- Consider cost implications of cloud-based load testing