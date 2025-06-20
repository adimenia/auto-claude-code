# Python Code Review

Comprehensive code review workflow focusing on code quality, security, performance, and maintainability.

## What This Command Does
1. **Security Analysis**: Scans for vulnerabilities, secrets, and security anti-patterns
2. **Code Quality Review**: Analyzes complexity, maintainability, and adherence to standards
3. **Performance Assessment**: Identifies potential performance bottlenecks and optimization opportunities
4. **Architecture Review**: Evaluates design patterns, dependencies, and structure
5. **Test Coverage Analysis**: Reviews test quality and completeness
6. **Documentation Review**: Checks documentation completeness and quality

## Usage
```bash
/user:review-python [target-path] [review-type]
```

## Review Process

### 1. Pre-Review Setup
```bash
echo "🔍 Starting comprehensive Python code review..."

target_path=${1:-"src/"}
review_type=${2:-"full"}  # full, security, performance, quality

echo "📁 Target path: $target_path"
echo "🎯 Review type: $review_type"

# Create review reports directory
mkdir -p review_reports
timestamp=$(date +"%Y%m%d_%H%M%S")
report_dir="review_reports/review_$timestamp"
mkdir -p $report_dir

echo "📊 Reports will be saved to: $report_dir"
```

### 2. Security Review
```bash
if [[ "$review_type" == "full" || "$review_type" == "security" ]]; then
    echo ""
    echo "🔒 SECURITY REVIEW"
    echo "=================="

    # Static security analysis with bandit
    echo "🛡️  Running security vulnerability scan..."
    if command -v bandit &> /dev/null; then
        bandit -r $target_path \
            -f json \
            -o $report_dir/security_bandit.json \
            -l -i
        
        bandit -r $target_path \
            -f txt \
            -o $report_dir/security_bandit.txt \
            -l -i
        
        echo "✅ Bandit security scan complete"
    else
        echo "⚠️  Bandit not available - install with: pip install bandit"
    fi

    # Check for hardcoded secrets
    echo "🔐 Scanning for hardcoded secrets..."
    secret_patterns=(
        "password\s*=\s*['\"][^'\"]{1,}"
        "api[_-]?key\s*=\s*['\"][^'\"]{8,}"
        "secret[_-]?key\s*=\s*['\"][^'\"]{8,}"
        "token\s*=\s*['\"][^'\"]{8,}"
        "auth[_-]?token\s*=\s*['\"][^'\"]{8,}"
        "access[_-]?key\s*=\s*['\"][^'\"]{8,}"
    )

    echo "Potential secrets found:" > $report_dir/secrets_scan.txt
    for pattern in "${secret_patterns[@]}"; do
        grep -rn -i -E "$pattern" $target_path >> $report_dir/secrets_scan.txt 2>/dev/null || true
    done

    # SQL injection patterns
    echo "🗄️  Checking for SQL injection vulnerabilities..."
    sql_patterns=(
        "execute\s*\(\s*['\"].*%.*['\"]"
        "cursor\.execute\s*\(\s*f['\"]"
        "query\s*=\s*['\"].*%.*['\"]"
        "\.format\s*\(.*\)"
    )

    echo "Potential SQL injection risks:" > $report_dir/sql_injection_scan.txt
    for pattern in "${sql_patterns[@]}"; do
        grep -rn -i -E "$pattern" $target_path >> $report_dir/sql_injection_scan.txt 2>/dev/null || true
    done

    # Check dependency vulnerabilities
    echo "📦 Checking dependency vulnerabilities..."
    if command -v safety &> /dev/null; then
        safety check --json > $report_dir/dependency_vulnerabilities.json 2>/dev/null || \
        safety check > $report_dir/dependency_vulnerabilities.txt 2>/dev/null
        echo "✅ Dependency vulnerability check complete"
    else
        echo "⚠️  Safety not available - install with: pip install safety"
    fi

    echo "✅ Security review complete"
fi
```

### 3. Code Quality Review
```bash
if [[ "$review_type" == "full" || "$review_type" == "quality" ]]; then
    echo ""
    echo "📏 CODE QUALITY REVIEW"
    echo "======================"

    # Complexity analysis
    echo "🧮 Analyzing code complexity..."
    if command -v radon &> /dev/null; then
        # Cyclomatic complexity
        radon cc $target_path -s -j > $report_dir/complexity_cyclomatic.json
        radon cc $target_path -s > $report_dir/complexity_cyclomatic.txt
        
        # Halstead complexity
        radon hal $target_path -j > $report_dir/complexity_halstead.json
        radon hal $target_path > $report_dir/complexity_halstead.txt
        
        # Maintainability index
        radon mi $target_path -j > $report_dir/maintainability.json
        radon mi $target_path > $report_dir/maintainability.txt
        
        echo "✅ Complexity analysis complete"
    else
        echo "⚠️  Radon not available - install with: pip install radon"
    fi

    # Code duplication analysis
    echo "🔄 Checking for code duplication..."
    if command -v vulture &> /dev/null; then
        vulture $target_path > $report_dir/dead_code.txt 2>/dev/null || true
        echo "✅ Dead code analysis complete"
    fi

    # Linting analysis
    echo "🔎 Running comprehensive linting..."
    flake8 $target_path \
        --statistics \
        --format='%(path)s:%(row)d:%(col)d: %(code)s %(text)s' \
        --output-file=$report_dir/linting_flake8.txt

    # Type checking
    echo "🏷️  Performing type analysis..."
    mypy $target_path \
        --html-report $report_dir/type_checking \
        --txt-report $report_dir/ \
        --any-exprs-report $report_dir/ \
        --linecount-report $report_dir/ 2>/dev/null || \
    mypy $target_path > $report_dir/type_checking.txt 2>&1

    # Import analysis
    echo "📋 Analyzing imports..."
    python << EOF > $report_dir/import_analysis.txt
import ast
import os
from collections import defaultdict

def analyze_imports(directory):
    imports = defaultdict(list)
    unused_imports = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        tree = ast.parse(f.read())
                    
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                imports[alias.name].append(filepath)
                        elif isinstance(node, ast.ImportFrom):
                            module = node.module or ''
                            for alias in node.names:
                                imports[f"{module}.{alias.name}"].append(filepath)
                except:
                    continue
    
    print("Import Analysis Report")
    print("=" * 50)
    print(f"Total unique imports: {len(imports)}")
    print(f"Files analyzed: {sum(len(files) for files in imports.values())}")
    
    print("\nMost frequently imported modules:")
    sorted_imports = sorted(imports.items(), key=lambda x: len(x[1]), reverse=True)
    for module, files in sorted_imports[:10]:
        print(f"  {module}: {len(files)} files")

analyze_imports("$target_path")
EOF

    echo "✅ Code quality review complete"
fi
```

### 4. Performance Review
```bash
if [[ "$review_type" == "full" || "$review_type" == "performance" ]]; then
    echo ""
    echo "⚡ PERFORMANCE REVIEW"
    echo "===================="

    # Performance anti-patterns
    echo "🐌 Scanning for performance anti-patterns..."
    
    performance_patterns=(
        "for.*in.*range\(len\("                    # Use enumerate instead
        "\.append\(.*\)\s*$"                       # List comprehension might be faster
        "time\.sleep\("                            # Blocking sleep calls
        "requests\.get\(.*\)\s*$"                  # Synchronous HTTP calls
        "json\.loads\(.*json\.dumps\("             # Redundant serialization
        "list\(.*\.keys\(\)\)"                     # Direct iteration is faster
        "\.format\(.*\%"                          # Mixed string formatting
    )

    echo "Performance anti-patterns found:" > $report_dir/performance_antipatterns.txt
    for pattern in "${performance_patterns[@]}"; do
        echo "Pattern: $pattern" >> $report_dir/performance_antipatterns.txt
        grep -rn -E "$pattern" $target_path >> $report_dir/performance_antipatterns.txt 2>/dev/null || true
        echo "" >> $report_dir/performance_antipatterns.txt
    done

    # Database query patterns
    echo "🗄️  Analyzing database query patterns..."
    db_patterns=(
        "\.filter\(.*\.filter\("                   # N+1 query pattern
        "for.*in.*\.all\(\):"                      # Inefficient iteration
        "\.get\(.*\)\s*except"                     # Exception handling for flow control
        "SELECT \* FROM"                           # Select all anti-pattern
    )

    echo "Database query patterns:" > $report_dir/database_patterns.txt
    for pattern in "${db_patterns[@]}"; do
        echo "Pattern: $pattern" >> $report_dir/database_patterns.txt
        grep -rn -i -E "$pattern" $target_path >> $report_dir/database_patterns.txt 2>/dev/null || true
        echo "" >> $report_dir/database_patterns.txt
    done

    # Memory usage patterns
    echo "🧠 Checking memory usage patterns..."
    memory_patterns=(
        "\[\].*for.*in"                           # List comprehension opportunities
        "\.readlines\(\)"                         # Memory-intensive file reading
        "\.read\(\)"                              # Reading entire files
        "pandas\.read_csv\(.*\)"                  # Large CSV handling
    )

    echo "Memory usage patterns:" > $report_dir/memory_patterns.txt
    for pattern in "${memory_patterns[@]}"; do
        echo "Pattern: $pattern" >> $report_dir/memory_patterns.txt
        grep -rn -E "$pattern" $target_path >> $report_dir/memory_patterns.txt 2>/dev/null || true
        echo "" >> $report_dir/memory_patterns.txt
    done

    echo "✅ Performance review complete"
fi
```

### 5. Architecture and Design Review
```bash
if [[ "$review_type" == "full" || "$review_type" == "architecture" ]]; then
    echo ""
    echo "🏗️  ARCHITECTURE REVIEW"
    echo "======================="

    # Dependency analysis
    echo "📦 Analyzing project dependencies..."
    python << EOF > $report_dir/architecture_analysis.txt
import ast
import os
from collections import defaultdict, Counter

def analyze_architecture(directory):
    functions = []
    classes = []
    imports = defaultdict(set)
    file_sizes = {}
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        file_sizes[filepath] = len(content.splitlines())
                        tree = ast.parse(content)
                    
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            functions.append((filepath, node.name, len(node.body)))
                        elif isinstance(node, ast.ClassDef):
                            classes.append((filepath, node.name, len(node.body)))
                        elif isinstance(node, ast.Import):
                            for alias in node.names:
                                imports[filepath].add(alias.name)
                        elif isinstance(node, ast.ImportFrom):
                            module = node.module or ''
                            imports[filepath].add(module)
                except:
                    continue
    
    print("Architecture Analysis Report")
    print("=" * 50)
    
    print(f"\nProject Statistics:")
    print(f"  Total Python files: {len(file_sizes)}")
    print(f"  Total functions: {len(functions)}")
    print(f"  Total classes: {len(classes)}")
    print(f"  Average file size: {sum(file_sizes.values()) / len(file_sizes):.1f} lines")
    
    print(f"\nLargest files (potential refactoring candidates):")
    large_files = sorted(file_sizes.items(), key=lambda x: x[1], reverse=True)[:5]
    for filepath, size in large_files:
        print(f"  {filepath}: {size} lines")
    
    print(f"\nLargest functions (complexity candidates):")
    large_functions = sorted(functions, key=lambda x: x[2], reverse=True)[:5]
    for filepath, name, size in large_functions:
        print(f"  {name} in {filepath}: {size} statements")
    
    print(f"\nLargest classes:")
    large_classes = sorted(classes, key=lambda x: x[2], reverse=True)[:5]
    for filepath, name, size in large_classes:
        print(f"  {name} in {filepath}: {size} statements")
    
    print(f"\nMost imported external modules:")
    all_imports = [imp for imps in imports.values() for imp in imps]
    external_imports = [imp for imp in all_imports if not imp.startswith('.') and not imp in ['os', 'sys', 'json']]
    import_counts = Counter(external_imports)
    for module, count in import_counts.most_common(10):
        print(f"  {module}: {count} files")

analyze_architecture("$target_path")
EOF

    # Design patterns analysis
    echo "🎨 Analyzing design patterns..."
    design_patterns=(
        "class.*Factory"                           # Factory pattern
        "class.*Singleton"                         # Singleton pattern
        "class.*Observer"                          # Observer pattern
        "class.*Strategy"                          # Strategy pattern
        "def __enter__.*def __exit__"              # Context manager pattern
        "@property"                                # Property decorators
        "@staticmethod"                            # Static methods
        "@classmethod"                             # Class methods
        "abc\.ABC"                                 # Abstract base classes
    )

    echo "Design patterns detected:" > $report_dir/design_patterns.txt
    for pattern in "${design_patterns[@]}"; do
        echo "Pattern: $pattern" >> $report_dir/design_patterns.txt
        grep -rn -E "$pattern" $target_path >> $report_dir/design_patterns.txt 2>/dev/null || true
        echo "" >> $report_dir/design_patterns.txt
    done

    echo "✅ Architecture review complete"
fi
```

### 6. Test Coverage and Quality Review
```bash
if [[ "$review_type" == "full" || "$review_type" == "testing" ]]; then
    echo ""
    echo "🧪 TEST COVERAGE REVIEW"
    echo "======================="

    # Run coverage analysis
    echo "📊 Analyzing test coverage..."
    if command -v pytest &> /dev/null; then
        pytest --cov=$target_path \
            --cov-report=html:$report_dir/coverage_html \
            --cov-report=xml:$report_dir/coverage.xml \
            --cov-report=json:$report_dir/coverage.json \
            tests/ 2>/dev/null || echo "⚠️  No tests found or pytest failed"
    fi

    # Test quality analysis
    echo "🔍 Analyzing test quality..."
    if [ -d "tests/" ]; then
        test_patterns=(
            "def test_.*pass"                      # Empty test functions
            "assert True"                          # Trivial assertions
            "assert.*=="                           # Simple equality tests
            "pytest\.skip"                         # Skipped tests
            "@pytest\.mark\.skip"                  # Marked as skip
            "TODO"                                 # Incomplete tests
            "FIXME"                                # Broken tests
        )

        echo "Test quality issues:" > $report_dir/test_quality.txt
        for pattern in "${test_patterns[@]}"; do
            echo "Pattern: $pattern" >> $report_dir/test_quality.txt
            grep -rn -E "$pattern" tests/ >> $report_dir/test_quality.txt 2>/dev/null || true
            echo "" >> $report_dir/test_quality.txt
        done
    fi

    echo "✅ Test coverage review complete"
fi
```

### 7. Documentation Review
```bash
echo ""
echo "📚 DOCUMENTATION REVIEW"
echo "======================="

# Check docstring coverage
echo "📝 Analyzing docstring coverage..."
python << EOF > $report_dir/documentation_analysis.txt
import ast
import os

def check_docstrings(directory):
    total_functions = 0
    documented_functions = 0
    total_classes = 0
    documented_classes = 0
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        tree = ast.parse(f.read())
                    
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            total_functions += 1
                            if ast.get_docstring(node):
                                documented_functions += 1
                        elif isinstance(node, ast.ClassDef):
                            total_classes += 1
                            if ast.get_docstring(node):
                                documented_classes += 1
                except:
                    continue
    
    print("Documentation Analysis Report")
    print("=" * 50)
    print(f"Functions documented: {documented_functions}/{total_functions} ({documented_functions/total_functions*100:.1f}%)" if total_functions > 0 else "No functions found")
    print(f"Classes documented: {documented_classes}/{total_classes} ({documented_classes/total_classes*100:.1f}%)" if total_classes > 0 else "No classes found")

check_docstrings("$target_path")
EOF

# Check for documentation files
echo "📖 Checking documentation completeness..."
doc_files=("README.md" "CHANGELOG.md" "LICENSE" "CONTRIBUTING.md" "docs/")
missing_docs=()

for doc in "${doc_files[@]}"; do
    if [ ! -e "$doc" ]; then
        missing_docs+=("$doc")
    fi
done

if [ ${#missing_docs[@]} -gt 0 ]; then
    echo "Missing documentation files:" >> $report_dir/documentation_analysis.txt
    printf '%s\n' "${missing_docs[@]}" >> $report_dir/documentation_analysis.txt
fi

echo "✅ Documentation review complete"
```

### 8. Generate Comprehensive Report
```bash
echo ""
echo "📊 GENERATING COMPREHENSIVE REPORT"
echo "=================================="

# Create HTML report
cat > $report_dir/code_review_report.html << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Code Review Report - $(basename "$PWD")</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }
        .section { margin: 30px 0; padding: 20px; border-left: 4px solid #3498db; background: #f8f9fa; border-radius: 5px; }
        .critical { border-left-color: #e74c3c; background: #fdf2f2; }
        .warning { border-left-color: #f39c12; background: #fefbf3; }
        .success { border-left-color: #27ae60; background: #f2f8f2; }
        .metric { display: inline-block; margin: 15px; padding: 15px; background: white; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); min-width: 150px; text-align: center; }
        .metric h3 { margin: 0 0 10px 0; color: #2c3e50; }
        .metric .value { font-size: 24px; font-weight: bold; color: #3498db; }
        .links { margin: 20px 0; }
        .links a { margin-right: 20px; text-decoration: none; color: #3498db; padding: 8px 16px; border: 1px solid #3498db; border-radius: 5px; transition: all 0.3s; }
        .links a:hover { background: #3498db; color: white; }
        .file-list { max-height: 300px; overflow-y: auto; background: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 5px; font-family: monospace; }
        pre { background: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 5px; overflow-x: auto; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Code Review Report</h1>
            <p>Project: $(basename "$PWD") | Target: $target_path | Type: $review_type</p>
            <p>Generated: $(date) | Reviewer: Claude Code Assistant</p>
        </div>

        <div class="grid">
            <div class="metric">
                <h3>📊 Files Analyzed</h3>
                <div class="value">$(find $target_path -name "*.py" | wc -l)</div>
            </div>
            <div class="metric">
                <h3>🔒 Security Issues</h3>
                <div class="value">$(wc -l < $report_dir/security_bandit.txt 2>/dev/null || echo "N/A")</div>
            </div>
            <div class="metric">
                <h3>📏 Quality Issues</h3>
                <div class="value">$(wc -l < $report_dir/linting_flake8.txt 2>/dev/null || echo "N/A")</div>
            </div>
            <div class="metric">
                <h3>⚡ Performance Flags</h3>
                <div class="value">$(grep -c "Pattern:" $report_dir/performance_antipatterns.txt 2>/dev/null || echo "N/A")</div>
            </div>
        </div>

        <div class="section critical">
            <h2>🔒 Security Analysis</h2>
            <div class="links">
                <a href="security_bandit.html" target="_blank">📊 Bandit Report</a>
                <a href="secrets_scan.txt" target="_blank">🔐 Secrets Scan</a>
                <a href="dependency_vulnerabilities.json" target="_blank">📦 Dependencies</a>
            </div>
        </div>

        <div class="section warning">
            <h2>📏 Code Quality</h2>
            <div class="links">
                <a href="complexity_cyclomatic.txt" target="_blank">🧮 Complexity</a>
                <a href="linting_flake8.txt" target="_blank">🔎 Linting</a>
                <a href="type_checking/index.html" target="_blank">🏷️ Type Check</a>
                <a href="maintainability.txt" target="_blank">🔧 Maintainability</a>
            </div>
        </div>

        <div class="section">
            <h2>⚡ Performance Analysis</h2>
            <div class="links">
                <a href="performance_antipatterns.txt" target="_blank">🐌 Anti-patterns</a>
                <a href="database_patterns.txt" target="_blank">🗄️ Database</a>
                <a href="memory_patterns.txt" target="_blank">🧠 Memory</a>
            </div>
        </div>

        <div class="section success">
            <h2>🧪 Test Coverage</h2>
            <div class="links">
                <a href="coverage_html/index.html" target="_blank">📈 Coverage Report</a>
                <a href="test_quality.txt" target="_blank">🔍 Test Quality</a>
            </div>
        </div>

        <div class="section">
            <h2>🏗️ Architecture</h2>
            <div class="links">
                <a href="architecture_analysis.txt" target="_blank">📊 Structure Analysis</a>
                <a href="design_patterns.txt" target="_blank">🎨 Design Patterns</a>
            </div>
        </div>

        <div class="section">
            <h2>📚 Documentation</h2>
            <div class="links">
                <a href="documentation_analysis.txt" target="_blank">📝 Doc Coverage</a>
            </div>
        </div>
    </div>
</body>
</html>
EOF

# Generate executive summary
cat > $report_dir/executive_summary.txt << EOF
===============================================
🔍 CODE REVIEW EXECUTIVE SUMMARY
===============================================
Project: $(basename "$PWD")
Target Path: $target_path
Review Type: $review_type
Date: $(date)

OVERVIEW:
Files Analyzed: $(find $target_path -name "*.py" | wc -l) Python files

SECURITY ASSESSMENT:
$([ -f $report_dir/security_bandit.txt ] && echo "- Bandit scan: $(wc -l < $report_dir/security_bandit.txt) issues found" || echo "- Security scan: Not available")
$([ -f $report_dir/secrets_scan.txt ] && echo "- Secrets scan: $(grep -c ":" $report_dir/secrets_scan.txt 2>/dev/null || echo "0") potential issues" || echo "- Secrets scan: Not available")

CODE QUALITY:
$([ -f $report_dir/linting_flake8.txt ] && echo "- Linting issues: $(wc -l < $report_dir/linting_flake8.txt)" || echo "- Linting: Not available")
$([ -f $report_dir/complexity_cyclomatic.txt ] && echo "- Complexity analysis: Available" || echo "- Complexity analysis: Not available")

PERFORMANCE:
$([ -f $report_dir/performance_antipatterns.txt ] && echo "- Anti-patterns detected: $(grep -c "Pattern:" $report_dir/performance_antipatterns.txt)" || echo "- Performance scan: Not available")

RECOMMENDATIONS:
1. Review all security findings in the security reports
2. Address high-complexity functions and classes
3. Fix linting issues for code consistency
4. Improve test coverage if below 80%
5. Add docstrings to undocumented functions/classes
6. Consider refactoring large files (>500 lines)

NEXT STEPS:
1. Prioritize security issues (Critical > High > Medium)
2. Address code quality issues systematically
3. Implement performance optimizations where beneficial
4. Enhance test coverage for critical paths
5. Update documentation as needed

Report Location: $report_dir/
Main Report: code_review_report.html
===============================================
EOF

echo "✅ Comprehensive report generated"
echo ""
echo "📋 REVIEW COMPLETE"
echo "=================="
echo "📊 Main Report: $report_dir/code_review_report.html"
echo "📝 Executive Summary: $report_dir/executive_summary.txt"
echo "📁 All Reports: $report_dir/"

# Display executive summary
echo ""
cat $report_dir/executive_summary.txt

# Open report if possible
if command -v open &> /dev/null; then
    open $report_dir/code_review_report.html
elif command -v xdg-open &> /dev/null; then
    xdg-open $report_dir/code_review_report.html
fi
```

## Arguments
- **$1**: Target path (optional, defaults to "src/")
- **$2**: Review type (optional: "full", "security", "performance", "quality", "architecture", "testing")

## Examples
```bash
/user:review-python                    # Full review of src/ directory
/user:review-python app/ security      # Security-focused review of app/ directory
/user:review-python . performance      # Performance review of entire project
/user:review-python tests/ testing     # Review test quality and coverage
```

## Review Types
- **full**: Complete analysis (all categories)
- **security**: Focus on vulnerabilities and security issues
- **performance**: Identify performance bottlenecks and optimization opportunities
- **quality**: Code quality, complexity, and maintainability
- **architecture**: Design patterns, structure, and dependencies
- **testing**: Test coverage and quality analysis

## Generated Reports
- **HTML Dashboard**: Interactive report with links to all analyses
- **Security Reports**: Vulnerability scans, secret detection, dependency checks
- **Quality Reports**: Complexity analysis, linting, type checking
- **Performance Reports**: Anti-pattern detection, optimization opportunities
- **Architecture Reports**: Structure analysis, design pattern usage
- **Coverage Reports**: Test coverage with line-by-line analysis
- **Executive Summary**: High-level findings and recommendations

## Requirements
- Python 3.8+ with project dependencies installed
- Optional tools for enhanced analysis: bandit, safety, radon, vulture, mypy
- pytest for test coverage analysis

## What You Get
- ✅ Comprehensive security vulnerability assessment
- ✅ Code quality and complexity analysis
- ✅ Performance bottleneck identification
- ✅ Architecture and design pattern review
- ✅ Test coverage and quality evaluation
- ✅ Documentation completeness check
- ✅ Professional HTML reports with interactive navigation
- ✅ Actionable recommendations prioritized by impact
- ✅ Executive summary for stakeholders