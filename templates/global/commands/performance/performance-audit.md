# Performance Audit

Comprehensive performance analysis and optimization recommendations for applications and systems.

## Usage:
`/project:performance-audit [--scope] [--depth]` or `/user:performance-audit [--scope]`

## Process:
1. **Baseline Measurement**: Establish current performance metrics and benchmarks
2. **Code Analysis**: Identify algorithmic complexity and performance bottlenecks
3. **Database Performance**: Analyze query performance, indexing, and connection patterns
4. **Memory Profiling**: Check for memory leaks, inefficient allocations, and GC pressure
5. **I/O Analysis**: Evaluate file system, network, and database I/O patterns
6. **Concurrency Review**: Assess threading, async patterns, and resource contention
7. **Frontend Performance**: Analyze client-side performance and user experience metrics
8. **Optimization Plan**: Generate prioritized recommendations with impact estimates

## Performance Metrics:
- **Response Time**: API endpoints, page load times, database queries
- **Throughput**: Requests per second, transactions per minute
- **Resource Usage**: CPU, memory, disk I/O, network bandwidth
- **Scalability**: Performance under increasing load
- **User Experience**: Time to first byte, time to interactive, cumulative layout shift

## Framework-Specific Analysis:
- **FastAPI**: Async performance, dependency injection overhead, serialization costs
- **Django**: ORM query optimization, middleware performance, template rendering
- **Flask**: Request handling, blueprint efficiency, extension overhead
- **Data Science**: Algorithm complexity, vectorization, memory usage in data processing
- **CLI Tools**: Startup time, argument parsing, file processing efficiency

## Arguments:
- `--scope`: Analysis scope (frontend, backend, database, full-stack)
- `--depth`: Analysis depth (basic, standard, comprehensive, deep-dive)
- `--benchmark`: Performance benchmarking against industry standards
- `--profile`: Enable detailed profiling with performance tools

## Examples:
- `/project:performance-audit` - Comprehensive performance analysis
- `/project:performance-audit --scope backend --depth deep-dive` - Deep backend analysis
- `/project:performance-audit --benchmark --profile` - Benchmarked analysis with profiling
- `/user:performance-audit --scope frontend` - Frontend-focused performance review

## Analysis Categories:

### Code Performance:
- **Algorithm Complexity**: O(n) analysis, nested loops, recursive calls
- **Data Structures**: Efficient data structure usage, cache locality
- **Memory Management**: Object creation patterns, garbage collection impact
- **Function Overhead**: Call stack depth, function inlining opportunities

### Database Performance:
- **Query Analysis**: Slow queries, N+1 problems, missing indexes
- **Connection Management**: Connection pooling, idle connections
- **Schema Design**: Normalization vs. denormalization, data types
- **Caching Strategy**: Query result caching, application-level caching

### System Performance:
- **Resource Utilization**: CPU usage patterns, memory consumption
- **I/O Operations**: File system access, network calls, disk usage
- **Concurrency**: Thread safety, deadlock potential, async efficiency
- **Scalability**: Horizontal vs. vertical scaling considerations

## Profiling Tools Integration:
- **Python**: cProfile, line_profiler, memory_profiler, py-spy
- **JavaScript**: Chrome DevTools, Lighthouse, WebPageTest
- **Database**: EXPLAIN plans, query analyzers, index analyzers
- **System**: top, htop, iostat, perf, flamegraphs

## Performance Testing:

### Micro-benchmarks:
```python
import timeit
import memory_profiler

def benchmark_function(func, *args, **kwargs):
    """Benchmark function execution time and memory usage."""
    # Time measurement
    execution_time = timeit.timeit(
        lambda: func(*args, **kwargs), 
        number=1000
    )
    
    # Memory measurement
    mem_usage = memory_profiler.memory_usage(
        (func, args, kwargs), 
        interval=0.1
    )
    
    return {
        'avg_time': execution_time / 1000,
        'memory_peak': max(mem_usage),
        'memory_growth': max(mem_usage) - min(mem_usage)
    }
```

### Load Testing Setup:
```python
# Example load test configuration
LOAD_TEST_CONFIG = {
    'scenarios': [
        {
            'name': 'normal_load',
            'users': 100,
            'spawn_rate': 10,
            'duration': '5m'
        },
        {
            'name': 'peak_load',
            'users': 500,
            'spawn_rate': 50,
            'duration': '10m'
        },
        {
            'name': 'stress_test',
            'users': 1000,
            'spawn_rate': 100,
            'duration': '15m'
        }
    ],
    'thresholds': {
        'response_time_95th': 500,  # ms
        'error_rate': 0.01,  # 1%
        'throughput_min': 100  # req/s
    }
}
```

## Optimization Recommendations:

### High Impact (Quick Wins):
- Database index optimization
- Query result caching
- Static asset compression
- CDN implementation
- Connection pooling

### Medium Impact:
- Algorithm optimization
- Data structure improvements
- Async/await implementation
- Memory usage optimization
- Code splitting and lazy loading

### Low Impact (Long-term):
- Architecture refactoring
- Technology stack changes
- Infrastructure scaling
- Advanced caching strategies

## Validation Checklist:
- [ ] Baseline performance metrics captured
- [ ] All performance bottlenecks identified and prioritized
- [ ] Database query performance analyzed and optimized
- [ ] Memory usage patterns documented
- [ ] Frontend performance metrics measured
- [ ] Load testing scenarios executed successfully
- [ ] Optimization recommendations provided with impact estimates
- [ ] Performance monitoring setup configured

## Output:
- Comprehensive performance analysis report
- Detailed profiling results and flame graphs
- Database query optimization recommendations
- Frontend performance audit with Core Web Vitals
- Load testing results and scalability assessment
- Prioritized optimization roadmap with effort estimates
- Performance monitoring dashboard configuration
- Best practices guide for ongoing performance management

## Notes:
- Establish performance baselines before making changes
- Focus on user-perceived performance metrics
- Consider performance impact of all code changes
- Implement continuous performance monitoring
- Regular performance audits as part of development cycle
- Balance performance optimization with code maintainability
- Document performance requirements and SLAs