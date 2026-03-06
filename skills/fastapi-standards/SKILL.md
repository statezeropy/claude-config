---
name: fastapi-standards
description: Enforce FastAPI design standards, RESTful principles, and project structure. Use when creating new endpoints, designing API architecture, or reviewing FastAPI code.
allowed-tools: Read, Grep, Glob
---

# FastAPI Design Standards

**IMPORTANT:** Always respond in Korean to the user.

## When to use
- **New Endpoint Creation:** When adding new API routes or handlers.
- **API Architecture Design:** When structuring routers, services, and schemas.
- **Code Review:** When checking for RESTful compliance or anti-patterns.
- **Authentication Setup:** When implementing OAuth2, JWT, or API key auth.

## Instructions

### 1. API Design Principles
1.1. **Methods:** Use correct HTTP methods (GET, POST, PUT, DELETE, PATCH).
1.2. **URL Structure:**
   - **Prefix:** All endpoints must start with `/api/v1`.
   - **Rule 1. Nouns (No Verbs):** Use resource names. Actions are handled by HTTP methods.
      - Good: `POST /api/v1/chats`
      - Bad: `POST /api/v1/createChat`
      - *Exception:* For AI processing jobs, use action-nouns (e.g., `/summarizations`).
   - **Rule 2. Plurals:** Always use plural nouns to represent collections.
      - Good: `/api/v1/users`, `/api/v1/summaries`
      - Bad: `/api/v1/user`
   - **Rule 3. Kebab-case:** Use lowercase letters and hyphens `-`. No camelCase or snake\_case in URLs.
      - Good: `/api/v1/user-profiles`
      - Bad: `/api/v1/userProfiles`, `/api/v1/user_profiles`
   - **Rule 4. Hierarchy:** Use URL paths to show parent/child relationships (max 3 levels).
      - Example: `/api/v1/users/{id}/chats` (Chats belonging to a specific user).
   - **Rule 5. Query Params for Filtering:** Do not use paths for filtering or sorting.
      - Good: `/api/v1/chats?sort=desc&limit=10`
      - Bad: `/api/v1/chats/recent/10`

1.3. **Responses:**
   - Always use Pydantic models.
   - Use `HTTPException`, never return `{"error": ...}` with 200 OK.

1.4. **Project Structure:**
   - `app/main.py`: Entry point.
   - `app/api/`: Routers.
   - `app/schemas/`: Pydantic models.
   - `app/services/`: Business logic.

1.5. **Dependency Injection:** Use `Depends()` explicitly. Avoid global state.

### 2. Authentication & Authorization
2.1. **OAuth2 with JWT:**
   - Use `OAuth2PasswordBearer` for token-based auth.
   - Store secrets in environment variables (use `pydantic-settings`).
   - Set reasonable token expiration times.

2.2. **Password Handling:**
   - **NEVER** store plain passwords. Use `passlib` with bcrypt.
   - Example: `pwd_context = CryptContext(schemes=["bcrypt"])`

2.3. **Authorization:**
   - Use dependency injection for role/permission checks.
   - Create reusable dependencies: `get_current_user`, `get_current_active_user`.

### 3. Error Handling
3.1. **Exception Handlers:**
   - Register global exception handlers in `main.py`.
   - Return consistent error response format.

3.2. **Error Response Schema:**
   ```python
   class ErrorResponse(BaseModel):
       detail: str
       error_code: str | None = None
   ```

3.3. **Custom Exceptions:**
   - Create domain-specific exceptions inheriting from `Exception`.
   - Map them to HTTP status codes via exception handlers.

### 4. Database Patterns (SQLAlchemy Async)
4.1. **Session Management:**
   - Use `async_sessionmaker` with `AsyncSession`.
   - Inject session via `Depends(get_db)`.

4.2. **Repository Pattern:**
   - Separate DB operations into repository classes.
   - Keep routes thin, business logic in services.

### 5. Testing
5.1. **Test Structure:**
   - `tests/`: Test directory at project root.
   - `tests/conftest.py`: Shared fixtures.
   - `tests/api/`: API endpoint tests.

5.2. **Test Client:**
   - Use `TestClient` for sync tests, `httpx.AsyncClient` for async.
   - Override dependencies for testing (mock DB, auth).

5.3. **Fixture Pattern:**
   ```python
   @pytest.fixture
   def client(app: FastAPI) -> TestClient:
       return TestClient(app)
   ```

### Checklist
Before finishing, verify:
- [ ] Endpoints start with /api/v1 and follow naming rules (Plural, Kebab-case).
- [ ] Endpoints follow RESTful principles (Methods/Status Codes).
- [ ] Pydantic models used for requests/responses.
- [ ] Project structure follows `app/` convention.
- [ ] Passwords hashed with bcrypt (never plain text).
- [ ] Secrets loaded from environment variables.
- [ ] Exception handlers return consistent error format.

## Examples

### Example Endpoint

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Router prefix should be set in main.py or router include, e.g., /api/v1
router = APIRouter(prefix="/items", tags=["items"]) 

class Item(BaseModel):
    name: str
    price: float

# Final URL: POST /api/v1/items
@router.post("", response_model=Item, status_code=201)
def create_item(item: Item):
    if item.price < 0:
        raise HTTPException(status_code=400, detail="Price cannot be negative")
    return item
```

### Authentication Dependency

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    user = await decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
```

### Global Exception Handler

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

class DomainException(Exception):
    def __init__(self, detail: str, error_code: str):
        self.detail = detail
        self.error_code = error_code

@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.detail, "error_code": exc.error_code},
    )
```

### Async Test Example

```python
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_create_item():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Testing against the versioned API path
        response = await client.post("/api/v1/items", json={"name": "Test", "price": 10.0})
        assert response.status_code == 201
```
