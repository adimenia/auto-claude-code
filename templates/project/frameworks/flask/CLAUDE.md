# Flask Project - Claude Configuration

## Project Overview
This is a Flask-based web application project designed for building traditional web applications, RESTful APIs, or hybrid applications. Flask is a lightweight WSGI web application framework that provides flexibility and simplicity for Python web development.

**Key Technologies:**
- **Flask**: Micro web framework for Python
- **Jinja2**: Modern templating engine for Python
- **Werkzeug**: WSGI utility library
- **Flask-SQLAlchemy**: Flask extension for SQLAlchemy ORM
- **Flask-Migrate**: Database migration handling
- **Flask-Login**: User session management
- **Flask-WTF**: Form handling and CSRF protection
- **Gunicorn/uWSGI**: WSGI server for production deployment

## Architecture & Patterns

### Directory Structure
```
project/
├── app/
│   ├── __init__.py          # Application factory
│   ├── models.py            # Database models
│   ├── forms.py             # WTForms classes
│   ├── views.py             # View functions (simple projects)
│   ├── main/                # Main blueprint
│   │   ├── __init__.py
│   │   ├── views.py         # Main route handlers
│   │   └── forms.py         # Main forms
│   ├── auth/                # Authentication blueprint
│   │   ├── __init__.py
│   │   ├── views.py         # Auth routes
│   │   └── forms.py         # Auth forms
│   ├── api/                 # API blueprint (if building API)
│   │   ├── __init__.py
│   │   ├── views.py         # API endpoints
│   │   └── errors.py        # API error handlers
│   ├── static/              # Static files (CSS, JS, images)
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   ├── templates/           # Jinja2 templates
│   │   ├── base.html        # Base template
│   │   ├── index.html       # Home page
│   │   └── auth/            # Auth templates
│   └── utils.py             # Utility functions
├── migrations/              # Database migrations
├── tests/                   # Test files
├── config.py               # Configuration classes
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables
└── run.py                 # Application entry point
```

### Flask Patterns
- **Application Factory**: Use create_app() pattern for configuration flexibility
- **Blueprints**: Organize routes into logical modules
- **Configuration Classes**: Use classes for different environments (dev, test, prod)
- **Template Inheritance**: Use Jinja2 template inheritance for consistent layouts
- **Form Handling**: Use Flask-WTF for secure form processing
- **Error Handling**: Custom error pages and API error responses
- **Database Models**: SQLAlchemy models with relationships

## Development Workflow

### Common Commands
```bash
# Development server
flask run
flask run --host=0.0.0.0 --port=5000 --debug

# Set Flask app environment
export FLASK_APP=run.py
export FLASK_ENV=development

# Database operations
flask db init                       # Initialize migrations
flask db migrate -m "Description"  # Create migration
flask db upgrade                   # Apply migrations
flask db downgrade               # Rollback migration

# Shell context
flask shell                        # Interactive shell with app context

# Custom commands
flask create-admin                 # Custom command example
flask seed-db                     # Seed database with test data

# Testing
python -m pytest
python -m pytest -v               # Verbose output
python -m pytest --cov=app        # With coverage
python -m pytest tests/test_auth.py  # Specific test file

# Code quality
black app/ tests/                  # Code formatting
isort app/ tests/                  # Import sorting
flake8 app/ tests/                 # Linting
mypy app/                          # Type checking
```

### Development Process
1. **Plan application structure** - Define blueprints and models
2. **Create database models** - SQLAlchemy model definitions
3. **Design templates** - Create base template and page templates
4. **Build forms** - WTForms for user input validation
5. **Implement views** - Route handlers and business logic
6. **Add authentication** - User registration, login, session management
7. **Write tests** - Unit tests for models, views, and forms
8. **Style frontend** - CSS/JavaScript for user interface
9. **Configure deployment** - Production settings and WSGI server

### Git Workflow
- **Feature branches**: `feature/user-profile-page`
- **Blueprint organization**: Separate commits for different blueprints
- **Migration files**: Always review before committing
- **Template changes**: Include screenshots in PR descriptions
- **Static files**: Optimize images and minify CSS/JS before committing

## Code Quality & Standards

### Python Code Style
- **Follow PEP 8** with Black formatting
- **Type hints**: Use for function parameters and returns where helpful
- **Docstrings**: Google style for functions and classes
- **Import organization**: Group imports (standard, third-party, local)
- **Error handling**: Use try/except blocks and flash messages for user feedback

### Web Development Standards
- **Responsive design**: Mobile-first CSS approach
- **Accessibility**: ARIA labels, semantic HTML, keyboard navigation
- **SEO**: Proper meta tags, semantic structure, clean URLs
- **Security**: CSRF protection, input validation, secure headers
- **Performance**: Minimize HTTP requests, optimize images, use caching
- **Progressive enhancement**: Ensure functionality without JavaScript

### Template Standards
- **Template inheritance**: Use extends and blocks consistently
- **Naming conventions**: snake_case for template files and variables
- **Template organization**: Group templates by blueprint/feature
- **Static file organization**: Logical folder structure for assets
- **Template comments**: Document complex template logic

## Testing Strategy

### Test Types
```python
# Unit tests - Test models and utility functions
def test_user_model():
    user = User(username='test', email='test@example.com')
    assert user.username == 'test'
    assert user.is_authenticated

# View tests - Test route handlers
def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

# Form tests - Test form validation
def test_registration_form():
    form_data = {'username': 'test', 'email': 'test@example.com', 'password': 'password123'}
    form = RegistrationForm(data=form_data)
    assert form.validate()

# Integration tests - Test complete workflows
def test_user_registration_flow(client):
    # Test registration, login, and profile access
    pass
```

### Test Configuration
- **Test database**: Use SQLite in-memory database for testing
- **Test client**: Use Flask test client for route testing
- **Fixtures**: Create reusable test data and app configurations
- **Mocking**: Mock external services and email sending
- **Coverage targets**: Aim for >80% code coverage

## Environment Variables

### Required Variables
```bash
# Application
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_APP=run.py

# Database
DATABASE_URL=sqlite:///app.db
# or for PostgreSQL: postgresql://user:password@localhost/dbname
TEST_DATABASE_URL=sqlite:///:memory:

# Email (if using email features)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# External Services
REDIS_URL=redis://localhost:6379
CELERY_BROKER_URL=redis://localhost:6379

# Security
WTF_CSRF_SECRET_KEY=your-csrf-secret-key
SESSION_COOKIE_SECURE=True  # Production only
```

### Configuration Classes
```python
# config.py
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
```

## Template Development

### Jinja2 Best Practices
```html
<!-- Base template structure -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{% endblock %} - MyApp</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <nav>{% include 'nav.html' %}</nav>
    
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}
    
    <main>{% block content %}{% endblock %}</main>
    
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>
```

### Template Security
- **Always** escape user input with |e filter or use autoescape
- **Never** use |safe filter on user-generated content
- **Use** CSRF tokens in all forms
- **Validate** template variables before rendering

## Form Handling

### Flask-WTF Patterns
```python
# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Repeat Password', 
                             validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
```

### Form Processing
```python
# views.py
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Process form data
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.html', form=form)
```

## Critical Rules

### Security Requirements
- ⚠️ **NEVER** store passwords in plain text - use werkzeug.security
- ⚠️ **ALWAYS** use CSRF protection with Flask-WTF
- ⚠️ **NEVER** commit SECRET_KEY to version control
- ⚠️ **ALWAYS** validate and sanitize user input
- ⚠️ **ALWAYS** use |e filter or autoescape in templates
- ⚠️ **NEVER** use |safe filter on user-generated content
- ⚠️ **ALWAYS** use HTTPS in production

### Database Requirements
- ⚠️ **ALWAYS** use SQLAlchemy ORM, never raw SQL strings
- ⚠️ **ALWAYS** use database migrations for schema changes
- ⚠️ **NEVER** commit migration files without review
- ⚠️ **ALWAYS** backup database before running migrations in production
- ⚠️ **ALWAYS** use db.session.commit() in try/except blocks

### Template Requirements
- ⚠️ **ALWAYS** extend base.html template
- ⚠️ **NEVER** put business logic in templates
- ⚠️ **ALWAYS** use url_for() for internal links
- ⚠️ **ALWAYS** include CSRF tokens in forms
- ⚠️ **NEVER** hardcode static file paths

### Development Requirements
- ⚠️ **NEVER** run Flask development server in production
- ⚠️ **ALWAYS** use application factory pattern
- ⚠️ **ALWAYS** use blueprints for organizing routes
- ⚠️ **NEVER** put all routes in a single file
- ⚠️ **ALWAYS** handle errors with custom error pages

## Common Commands Reference

### Daily Development
```bash
# Start development server
flask run --debug

# Database operations
flask db migrate -m "Add user table"
flask db upgrade

# Shell with app context
flask shell

# Run tests
python -m pytest -v --cov=app

# Code formatting
black app/ tests/ && isort app/ tests/
```

### Database Commands
```bash
# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Reset database
flask db downgrade base
flask db upgrade

# Create admin user (custom command)
flask create-admin --username admin --email admin@example.com
```

### Production Commands
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# Check application health
curl http://localhost:5000/health
```

## Claude-Specific Instructions

### Code Generation Preferences
- **Always** use Flask application factory pattern
- **Always** organize routes into blueprints
- **Prefer** Flask-SQLAlchemy for database operations
- **Include** proper error handling and flash messages
- **Add** docstrings for view functions and models
- **Use** Flask-WTF for all form handling
- **Follow** Flask best practices for project structure

### Template Generation
- **Always** extend base template
- **Include** proper CSRF protection in forms
- **Use** Bootstrap or similar CSS framework classes
- **Add** proper form validation display
- **Include** flash message display
- **Use** semantic HTML structure

### Security Focus
- **Always** include CSRF protection
- **Use** proper password hashing
- **Implement** input validation and sanitization
- **Add** proper error handling without information disclosure
- **Include** secure session configuration
- **Consider** rate limiting for sensitive endpoints

### Development Patterns
- **Blueprint organization**: Group related functionality
- **Model relationships**: Use SQLAlchemy relationships properly
- **Form-view integration**: Connect forms with view functions
- **Template inheritance**: Maintain consistent layout
- **Static file organization**: Logical asset management
- **Testing coverage**: Include tests for all major functionality