# Phase 2 - Authentication System

## Overview

This phase implements user authentication using JWT tokens with the following features:

- ✅ User registration with email validation
- ✅ User login with JWT token generation
- ✅ Protected routes using Bearer tokens
- ✅ Get current user information
- ✅ Password hashing with bcrypt
- ✅ Token verification and validation

## New Files

### Database Models
- **`app/models/user.py`** - User model with hashed password storage

### Services
- **`app/services/security.py`** - Password hashing and JWT token management
- **`app/services/user.py`** - User database operations and authentication logic

### Schemas (Validation)
- **`app/schemas/auth.py`** - Request/response schemas for authentication

### Routes
- **`app/routers/auth.py`** - Authentication endpoints (register, login, me)

### Updated
- **`app/main.py`** - Integrated auth router

## API Endpoints

### 1. Register User
**Endpoint:** `POST /api/auth/register`

**Request:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securePassword123"
}
```

**Response (201 Created):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "is_active": true,
    "created_at": "2026-06-10T20:43:36"
  }
}
```

**Error (400 Bad Request):**
```json
{
  "detail": "Username or email already registered"
}
```

### 2. Login User
**Endpoint:** `POST /api/auth/login`

**Request:**
```json
{
  "username": "john_doe",
  "password": "securePassword123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "is_active": true,
    "created_at": "2026-06-10T20:43:36"
  }
}
```

**Error (401 Unauthorized):**
```json
{
  "detail": "Invalid username/email or password"
}
```

### 3. Get Current User
**Endpoint:** `GET /api/auth/me`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2026-06-10T20:43:36"
}
```

**Error (401 Unauthorized):**
```json
{
  "detail": "Invalid or expired token"
}
```

## Testing with cURL

### Register
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securePassword123"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securePassword123"
  }'
```

### Get Current User (replace TOKEN with actual token)
```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer TOKEN"
```

## Testing with Swagger UI

1. Start the server: `python run.py`
2. Open: `http://localhost:8000/docs`
3. Click on each endpoint to test
4. For protected endpoints (GET /api/auth/me):
   - Click "Authorize" button in top-right
   - Enter: `Bearer <your_token>`
   - Click "Authorize"
   - Now you can test protected endpoints

## Architecture

### Security Flow
1. User provides credentials (username/email + password)
2. `UserService.authenticate_user()` verifies credentials
3. `TokenService.create_access_token()` generates JWT token
4. User receives token and stores it
5. For protected endpoints, token is verified via `get_current_user()` dependency

### Password Security
- Passwords are hashed using bcrypt (never stored in plain text)
- `PasswordService.hash_password()` hashes on registration
- `PasswordService.verify_password()` compares during login

### Token Security
- JWT tokens are signed with `SECRET_KEY` from config
- Default expiration: 30 minutes (configurable in `.env`)
- Tokens include user_id and username in payload
- Invalid/expired tokens are rejected

## Security Considerations

⚠️ **For Production:**
1. Change `SECRET_KEY` in `.env` to a strong random value
2. Update CORS `allow_origins` to specific domains (not "*")
3. Use HTTPS in production
4. Consider token refresh mechanisms
5. Add rate limiting on login/register endpoints
6. Add logging for authentication attempts
7. Add email verification for registration

## Database Schema

```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(120) UNIQUE NOT NULL,
  hashed_password VARCHAR(255) NOT NULL,
  is_active BOOLEAN DEFAULT TRUE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Next Steps

**Phase 3: Database Models**
- Create Pet model
- Create Activity model
- Create Friendship model
- Create Achievement model
- Create PetFocus model
- Link User to Pet relationships

## Useful Links

- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [JWT (JSON Web Tokens)](https://jwt.io/)
- [Passlib Documentation](https://passlib.readthedocs.io/)
- [Python-Jose (JWT Library)](https://github.com/mpdavis/python-jose)