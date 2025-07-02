# API Design

Design comprehensive RESTful APIs with OpenAPI specifications, documentation, and best practices implementation.

## Usage:
`/project:api-design [--style] [--specification]` or `/user:api-design [--style]`

## Process:
1. **Requirements Analysis**: Analyze business requirements and data models
2. **Resource Identification**: Identify API resources and their relationships
3. **Endpoint Design**: Design RESTful endpoints with proper HTTP methods
4. **Schema Definition**: Create data models and validation schemas
5. **Documentation Generation**: Generate comprehensive API documentation
6. **Security Implementation**: Add authentication, authorization, and rate limiting
7. **Versioning Strategy**: Implement API versioning and backward compatibility
8. **Testing Setup**: Create API tests and validation scenarios

## API Design Styles:
- **REST**: Resource-based, HTTP methods, stateless
- **GraphQL**: Query language, single endpoint, type system
- **RPC**: Remote procedure calls, action-based endpoints
- **WebSocket**: Real-time bidirectional communication
- **Webhook**: Event-driven, callback-based integration

## Framework-Specific Implementation:
- **FastAPI**: Pydantic models, automatic OpenAPI, dependency injection, async support
- **Django**: Django REST Framework, serializers, viewsets, permissions
- **Flask**: Flask-RESTful, Marshmallow schemas, blueprint organization
- **Data Science**: Model serving APIs, data processing endpoints, analytics interfaces

## Arguments:
- `--style`: API style (rest, graphql, rpc, websocket, webhook)
- `--specification`: Spec format (openapi, asyncapi, graphql-schema)
- `--auth`: Authentication method (jwt, oauth2, api-key, basic)
- `--versioning`: Versioning strategy (url, header, query, accept-header)

## Examples:
- `/project:api-design` - Design RESTful API with OpenAPI specification
- `/project:api-design --style graphql` - Design GraphQL API with schema
- `/project:api-design --auth oauth2 --versioning header` - OAuth2 with header versioning
- `/user:api-design --specification asyncapi` - Event-driven API design

## RESTful API Design Principles:

### Resource Naming:
```
Good Examples:
GET    /users              # Get all users
GET    /users/123          # Get specific user
POST   /users              # Create new user
PUT    /users/123          # Update user (full replacement)
PATCH  /users/123          # Update user (partial)
DELETE /users/123          # Delete user
GET    /users/123/posts    # Get user's posts

Avoid:
GET    /getUsers           # Non-RESTful naming
POST   /users/delete/123   # Wrong HTTP method
GET    /user-posts         # Unclear resource relationship
```

### HTTP Status Codes:
```
Success:
200 OK              # Successful GET, PUT, PATCH
201 Created         # Successful POST
204 No Content      # Successful DELETE

Client Errors:
400 Bad Request     # Invalid request format
401 Unauthorized    # Authentication required
403 Forbidden       # Access denied
404 Not Found       # Resource doesn't exist
409 Conflict        # Resource conflict
422 Unprocessable   # Validation errors

Server Errors:
500 Internal Error  # Server-side error
502 Bad Gateway     # Upstream service error
503 Unavailable     # Service temporarily down
```

## OpenAPI Specification Example:

### FastAPI Implementation:
```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="User Management API",
    description="Comprehensive user management system",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

class UserBase(BaseModel):
    """Base user model with common fields."""
    email: str = Field(..., example="user@example.com")
    full_name: str = Field(..., min_length=1, max_length=100)
    is_active: bool = Field(default=True)

class UserCreate(UserBase):
    """User creation model."""
    password: str = Field(..., min_length=8)

class UserResponse(UserBase):
    """User response model."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    """User update model."""
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

@app.post("/api/v1/users", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    """Create a new user account."""
    # Implementation here
    pass

@app.get("/api/v1/users", response_model=List[UserResponse])
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get list of users with pagination."""
    # Implementation here
    pass

@app.get("/api/v1/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Get user by ID."""
    # Implementation here
    pass
```

### Django REST Framework:
```python
from rest_framework import serializers, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    """User serializer with validation."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active']
        read_only_fields = ['id']
    
    def validate_email(self, value):
        """Validate email uniqueness."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

class UserViewSet(viewsets.ModelViewSet):
    """User management viewset."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        """Set user password."""
        user = self.get_object()
        password = request.data.get('password')
        if password:
            user.set_password(password)
            user.save()
            return Response({'status': 'password set'})
        return Response({'error': 'password required'}, status=400)
```

## API Security Implementation:

### Authentication & Authorization:
```python
# JWT Authentication
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Validate JWT token and return current user."""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        return await get_user_by_id(user_id)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

# Rate Limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/api/v1/public-data")
@limiter.limit("100/minute")
async def get_public_data(request: Request):
    """Public endpoint with rate limiting."""
    return {"data": "public information"}
```

## API Versioning Strategies:

### URL Versioning:
```
/api/v1/users
/api/v2/users
```

### Header Versioning:
```
GET /api/users
Accept: application/vnd.api+json;version=1
```

### Query Parameter Versioning:
```
/api/users?version=1
```

## Validation Checklist:
- [ ] All endpoints follow RESTful conventions
- [ ] Proper HTTP methods and status codes used
- [ ] Comprehensive input validation implemented
- [ ] Authentication and authorization configured
- [ ] Rate limiting and security headers in place
- [ ] API documentation complete and accurate
- [ ] Error handling provides meaningful messages
- [ ] Versioning strategy implemented consistently
- [ ] Integration tests cover all endpoints
- [ ] Performance considerations addressed

## Output:
- Complete OpenAPI/AsyncAPI specification
- Framework-specific API implementation code
- Comprehensive API documentation with examples
- Authentication and authorization setup
- Rate limiting and security configuration
- API testing suite with integration tests
- Versioning strategy implementation
- Monitoring and logging configuration
- Client SDK generation instructions

## Notes:
- Design APIs for your consumers, not your database
- Use consistent naming conventions across all endpoints
- Implement proper error handling with meaningful messages
- Consider backward compatibility when versioning
- Document all breaking changes and migration paths
- Implement proper logging for debugging and monitoring
- Use appropriate caching strategies for performance
- Regular API security audits and penetration testing