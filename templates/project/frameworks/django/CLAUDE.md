# Django Project - Claude Configuration

## Project Overview
This is a Django-based web application following Django best practices with a focus on maintainable, scalable architecture. Django provides a batteries-included framework with ORM, admin interface, authentication, and robust security features out of the box.

## Architecture
- **Framework**: Django with MTV (Model-Template-View) pattern
- **Database**: PostgreSQL with Django ORM
- **Authentication**: Django's built-in authentication system with custom user model
- **API**: Django REST Framework for API endpoints
- **Frontend**: Django templates with Bootstrap/Tailwind CSS
- **Testing**: Django's TestCase with factory_boy for test data
- **Deployment**: Docker with gunicorn and nginx

## Project Structure
```
django-project/
├── config/                     # Project configuration
│   ├── __init__.py
│   ├── settings/              # Split settings by environment
│   │   ├── __init__.py
│   │   ├── base.py           # Base settings
│   │   ├── development.py    # Development settings
│   │   ├── testing.py        # Test settings
│   │   └── production.py     # Production settings
│   ├── urls.py               # Main URL configuration
│   ├── wsgi.py               # WSGI configuration
│   └── asgi.py               # ASGI configuration (for async)
├── apps/                      # Django applications
│   ├── accounts/             # User management app
│   │   ├── models.py         # User models
│   │   ├── views.py          # Authentication views
│   │   ├── serializers.py    # DRF serializers
│   │   ├── admin.py          # Admin configuration
│   │   └── urls.py           # App URLs
│   ├── core/                 # Core/shared functionality
│   │   ├── models.py         # Abstract base models
│   │   ├── permissions.py    # Custom permissions
│   │   ├── mixins.py         # View mixins
│   │   └── utils.py          # Utility functions
│   └── api/                  # API app
│       ├── v1/               # API version 1
│       │   ├── views.py      # API views
│       │   ├── serializers.py # API serializers
│       │   └── urls.py       # API URLs
│       └── permissions.py    # API permissions
├── templates/                 # Django templates
│   ├── base.html             # Base template
│   ├── accounts/             # Account templates
│   └── core/                 # Core templates
├── static/                    # Static files
│   ├── css/                  # Stylesheets
│   ├── js/                   # JavaScript
│   └── images/               # Images
├── media/                     # User uploads
├── tests/                     # Test files
│   ├── factories/            # Factory boy factories
│   ├── test_models.py        # Model tests
│   ├── test_views.py         # View tests
│   └── test_api.py           # API tests
├── requirements/              # Split requirements
│   ├── base.txt              # Base requirements
│   ├── development.txt       # Development requirements
│   └── production.txt        # Production requirements
├── scripts/                   # Management scripts
├── locale/                    # Internationalization files
└── manage.py                 # Django management script
```

## Development Workflow
```bash
# Setup and activation
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -r requirements/development.txt

# Database setup and migrations
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Development server
python manage.py runserver 0.0.0.0:8000

# Testing workflow
python manage.py test
python manage.py test apps.accounts
coverage run --source='.' manage.py test
coverage report

# Code quality checks
black .
isort .
flake8 .
mypy .

# Static files and media
python manage.py collectstatic
python manage.py compress  # If using django-compressor

# Django shell for debugging
python manage.py shell
python manage.py shell_plus  # If using django-extensions

# Database operations
python manage.py dbshell
python manage.py dumpdata > fixtures/initial_data.json
python manage.py loaddata fixtures/initial_data.json
```

## Django-Specific Development Patterns

### Model Definition Pattern
```python
# ✅ Preferred Django model pattern
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimestampedModel

class User(AbstractUser):
    """Custom user model with additional fields."""
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    is_verified = models.BooleanField(_('verified'), default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        
    def __str__(self) -> str:
        return f"{self.get_full_name()} ({self.email})"
    
    def get_absolute_url(self) -> str:
        return reverse('accounts:profile', kwargs={'pk': self.pk})

class Profile(TimestampedModel):
    """User profile with additional information."""
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='profile'
    )
    bio = models.TextField(_('bio'), max_length=500, blank=True)
    avatar = models.ImageField(
        _('avatar'), 
        upload_to='avatars/', 
        blank=True, 
        null=True
    )
    
    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
    
    def __str__(self) -> str:
        return f"Profile for {self.user.get_full_name()}"
```

### View Pattern (Class-Based Views)
```python
# ✅ Preferred Django view pattern
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.utils.translation import gettext_lazy as _
from apps.core.mixins import OwnerRequiredMixin
from .models import Profile
from .forms import ProfileForm

class ProfileDetailView(LoginRequiredMixin, DetailView):
    """Display user profile details."""
    model = Profile
    template_name = 'accounts/profile_detail.html'
    context_object_name = 'profile'
    
    def get_object(self, queryset=None):
        """Get profile for current user."""
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

class ProfileUpdateView(
    LoginRequiredMixin, 
    OwnerRequiredMixin, 
    SuccessMessageMixin,
    UpdateView
):
    """Update user profile."""
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile_form.html'
    success_message = _('Profile updated successfully!')
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self, queryset=None):
        """Get profile for current user."""
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
    
    def form_valid(self, form):
        """Add user to form instance before saving."""
        form.instance.user = self.request.user
        return super().form_valid(form)
```

### Django REST Framework API Pattern
```python
# ✅ Preferred DRF API pattern
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, ProfileSerializer
from .permissions import IsOwnerOrReadOnly

User = get_user_model()

class UserListCreateAPIView(generics.ListCreateAPIView):
    """List all users or create a new user."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter queryset based on user permissions."""
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """Retrieve or update a user instance."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def perform_update(self, serializer):
        """Custom update logic."""
        # Add any custom logic before saving
        instance = serializer.save()
        # Add any post-save logic
        return instance

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    """Change user password."""
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    
    if not user.check_password(old_password):
        return Response(
            {'error': 'Invalid old password'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user.set_password(new_password)
    user.save()
    
    return Response(
        {'message': 'Password changed successfully'}, 
        status=status.HTTP_200_OK
    )
```

### Form Pattern
```python
# ✅ Preferred Django form pattern
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import Profile

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form with additional fields."""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Email address')
        })
    )
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('First name')
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def save(self, commit=True):
        """Save user with additional fields."""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    """Profile update form."""
    
    class Meta:
        model = Profile
        fields = ('bio', 'avatar')
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('Tell us about yourself...')
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
    
    def clean_avatar(self):
        """Validate avatar file size and type."""
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError(_('File size must be under 5MB'))
        return avatar
```

## Critical Rules - NEVER VIOLATE
- **NEVER use raw SQL queries** without proper parameterization to prevent SQL injection
- **NEVER store sensitive data in settings.py** - use environment variables
- **NEVER disable CSRF protection** unless absolutely necessary and with proper justification
- **NEVER use `User.objects.get()`** without exception handling - use `get_object_or_404()`
- **ALWAYS use Django's built-in authentication** and authorization systems
- **ALWAYS validate and sanitize user input** using Django forms or serializers
- **ALWAYS use proper URL namespacing** with app names in URL patterns
- **ALWAYS handle database migrations** properly and test them on staging
- **NEVER commit migration files** with sensitive data or credentials
- **ALWAYS use timezone-aware datetime** objects with Django's timezone utilities

## Django Best Practices

### Settings Configuration
```python
# ✅ Environment-based settings pattern
# config/settings/base.py
import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Security
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost', cast=lambda v: [s.strip() for s in v.split(',')])

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
    'django_extensions',
]

LOCAL_APPS = [
    'apps.core',
    'apps.accounts',
    'apps.api',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Custom user model
AUTH_USER_MODEL = 'accounts.User'
```

### URL Configuration
```python
# ✅ Proper URL namespacing pattern
# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('api/v1/', include('apps.api.v1.urls', namespace='api-v1')),
    path('', include('apps.core.urls', namespace='core')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# apps/accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileDetailView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile-edit'),
]
```

### Admin Configuration
```python
# ✅ Comprehensive admin configuration
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Profile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom user admin with additional fields."""
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_verified', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_verified', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        (_('Additional Info'), {'fields': ('is_verified',)}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (_('Additional Info'), {
            'fields': ('first_name', 'last_name', 'email', 'is_verified'),
        }),
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile admin configuration."""
    list_display = ('user', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('user')
```

## Common Commands
```bash
# Django management commands
python manage.py runserver 0.0.0.0:8000    # Development server
python manage.py runserver_plus              # Enhanced development server (django-extensions)
python manage.py shell                       # Django shell
python manage.py shell_plus                  # Enhanced shell (django-extensions)

# Database operations
python manage.py makemigrations              # Create migrations
python manage.py makemigrations accounts     # Create migrations for specific app
python manage.py migrate                     # Apply migrations
python manage.py migrate --plan              # Show migration plan
python manage.py showmigrations              # Show migration status
python manage.py sqlmigrate accounts 0001    # Show SQL for migration
python manage.py dbshell                     # Database shell

# User management
python manage.py createsuperuser             # Create superuser
python manage.py changepassword username     # Change user password

# Static files and media
python manage.py collectstatic               # Collect static files
python manage.py findstatic filename         # Find static file location
python manage.py compress                    # Compress static files (django-compressor)

# Data management
python manage.py dumpdata > fixtures/data.json              # Export data
python manage.py dumpdata accounts > fixtures/accounts.json # Export app data
python manage.py loaddata fixtures/data.json                # Import data
python manage.py flush                                       # Clear database

# Testing and quality
python manage.py test                        # Run all tests
python manage.py test apps.accounts          # Test specific app
python manage.py test --keepdb               # Keep test database
python manage.py test --parallel             # Parallel testing
coverage run --source='.' manage.py test     # Test with coverage
coverage report                              # Coverage report

# Internationalization
python manage.py makemessages -l es          # Create translation files
python manage.py compilemessages             # Compile translations

# Custom management commands
python manage.py send_notifications          # Custom command example
python manage.py cleanup_old_sessions        # Custom maintenance command
```

## Testing Strategy
- **Unit Tests**: Test models, forms, and utility functions
- **Integration Tests**: Test views and API endpoints
- **Model Tests**: Test model methods, properties, and validation
- **View Tests**: Test authentication, permissions, and response content
- **Form Tests**: Test form validation and save methods
- **API Tests**: Test serializers, permissions, and endpoint behavior

### Testing Patterns
```python
# ✅ Django test patterns
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from factory.django import DjangoModelFactory
import factory

User = get_user_model()

class UserFactory(DjangoModelFactory):
    """Factory for creating test users."""
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

class UserModelTest(TestCase):
    """Test User model."""
    
    def setUp(self):
        self.user = UserFactory()
    
    def test_string_representation(self):
        """Test __str__ method."""
        expected = f"{self.user.get_full_name()} ({self.user.email})"
        self.assertEqual(str(self.user), expected)
    
    def test_get_absolute_url(self):
        """Test get_absolute_url method."""
        expected_url = reverse('accounts:profile', kwargs={'pk': self.user.pk})
        self.assertEqual(self.user.get_absolute_url(), expected_url)

class UserViewTest(TestCase):
    """Test user views."""
    
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
    
    def test_profile_view_requires_login(self):
        """Test that profile view requires authentication."""
        url = reverse('accounts:profile')
        response = self.client.get(url)
        self.assertRedirects(response, f'/accounts/login/?next={url}')
    
    def test_profile_view_authenticated(self):
        """Test profile view with authenticated user."""
        self.client.force_login(self.user)
        url = reverse('accounts:profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.get_full_name())

class UserAPITest(APITestCase):
    """Test user API endpoints."""
    
    def setUp(self):
        self.user = UserFactory()
    
    def test_user_list_requires_authentication(self):
        """Test that user list requires authentication."""
        url = reverse('api-v1:user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_user_list_authenticated(self):
        """Test user list with authentication."""
        self.client.force_authenticate(user=self.user)
        url = reverse('api-v1:user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
```

## Environment Variables
```bash
# Django configuration
SECRET_KEY=your-secret-key-here
DEBUG=true
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DJANGO_SETTINGS_MODULE=config.settings.development

# Database configuration
DB_ENGINE=django.db.backends.postgresql
DB_NAME=django_project
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# Cache configuration (Redis)
CACHE_URL=redis://localhost:6379/1
SESSION_CACHE_ALIAS=default

# Email configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourproject.com

# Media and static files
MEDIA_URL=/media/
STATIC_URL=/static/
MEDIA_ROOT=./media
STATIC_ROOT=./staticfiles

# Security settings
SECURE_SSL_REDIRECT=false
SECURE_HSTS_SECONDS=0
SECURE_CONTENT_TYPE_NOSNIFF=true
SECURE_BROWSER_XSS_FILTER=true
X_FRAME_OPTIONS=DENY

# Third-party integrations
SENTRY_DSN=your-sentry-dsn-here
REDIS_URL=redis://localhost:6379/0

# API configuration
API_THROTTLE_ANON=100/hour
API_THROTTLE_USER=1000/hour
CORS_ALLOW_ALL_ORIGINS=false
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## Claude-Specific Instructions
- **Django Patterns**: Always follow Django conventions like MTV pattern, proper URL namespacing, and app organization
- **Security First**: Prioritize Django's security features (CSRF, authentication, permissions)
- **ORM Usage**: Leverage Django ORM efficiently with select_related, prefetch_related for performance
- **Forms and Validation**: Use Django forms for data validation and HTML generation
- **Admin Integration**: Configure Django admin for content management and debugging
- **Migration Handling**: Always create and review migrations carefully before applying
- **Testing**: Write comprehensive tests using Django's TestCase and factory_boy for test data
- **Internationalization**: Consider i18n/l10n from the beginning if multiple languages needed