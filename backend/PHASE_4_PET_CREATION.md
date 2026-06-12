# Phase 4 - Pet Creation System

## Overview

This phase implements the complete pet management system, allowing users to create, read, update, and delete pets. Each pet automatically gets default stat focus settings.

## API Endpoints

### 1. Create Pet
**Endpoint:** `POST /api/pets/create`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request:**
```json
{
  "name": "Buddy",
  "species": "dog"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "user_id": 1,
  "name": "Buddy",
  "species": "dog",
  "level": 1,
  "experience": 0,
  "evolution_stage": 1,
  "strength_xp": 0,
  "endurance_xp": 0,
  "speed_xp": 0,
  "created_at": "2026-06-12T02:30:00",
  "updated_at": "2026-06-12T02:30:00",
  "pet_focus": {
    "id": 1,
    "pet_id": 1,
    "strength_focus": 50,
    "endurance_focus": 30,
    "speed_focus": 20
  }
}
```

**Errors:**
- `400`: Invalid species
- `401`: Invalid or missing token

**Valid Species:**
- `dog`
- `cat`
- `rabbit`
- `bird`
- `dragon`

### 2. Get All Pets
**Endpoint:** `GET /api/pets`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "pets": [
    {
      "id": 1,
      "user_id": 1,
      "name": "Buddy",
      "species": "dog",
      "level": 1,
      "experience": 0,
      "evolution_stage": 1,
      "strength_xp": 0,
      "endurance_xp": 0,
      "speed_xp": 0,
      "created_at": "2026-06-12T02:30:00",
      "updated_at": "2026-06-12T02:30:00",
      "pet_focus": {
        "id": 1,
        "pet_id": 1,
        "strength_focus": 50,
        "endurance_focus": 30,
        "speed_focus": 20
      }
    }
  ],
  "total": 1
}
```

**Errors:**
- `401`: Invalid or missing token

### 3. Get Single Pet
**Endpoint:** `GET /api/pets/{pet_id}`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `pet_id`: ID of the pet to retrieve

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": 1,
  "name": "Buddy",
  "species": "dog",
  "level": 1,
  "experience": 0,
  "evolution_stage": 1,
  "strength_xp": 0,
  "endurance_xp": 0,
  "speed_xp": 0,
  "created_at": "2026-06-12T02:30:00",
  "updated_at": "2026-06-12T02:30:00",
  "pet_focus": {
    "id": 1,
    "pet_id": 1,
    "strength_focus": 50,
    "endurance_focus": 30,
    "speed_focus": 20
  }
}
```

**Errors:**
- `401`: Invalid or missing token
- `403`: Pet belongs to another user
- `404`: Pet not found

### 4. Update Pet Name
**Endpoint:** `PUT /api/pets/{pet_id}`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `pet_id`: ID of the pet to update

**Request:**
```json
{
  "name": "BuddyNew"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": 1,
  "name": "BuddyNew",
  "species": "dog",
  "level": 1,
  "experience": 0,
  "evolution_stage": 1,
  "strength_xp": 0,
  "endurance_xp": 0,
  "speed_xp": 0,
  "created_at": "2026-06-12T02:30:00",
  "updated_at": "2026-06-12T02:35:00",
  "pet_focus": null
}
```

**Errors:**
- `401`: Invalid or missing token
- `403`: Pet belongs to another user
- `404`: Pet not found

### 5. Delete Pet
**Endpoint:** `DELETE /api/pets/{pet_id}`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `pet_id`: ID of the pet to delete

**Response (204 No Content):**
```
(empty response)
```

**Errors:**
- `401`: Invalid or missing token
- `403`: Pet belongs to another user
- `404`: Pet not found

---

## Testing with cURL

### Create Pet
```bash
# First, login to get token
TOKEN=$(curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"test_user","password":"TestPass123"}' \
  | jq -r '.access_token')

# Create pet
curl -X POST "http://localhost:8000/api/pets/create" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Buddy","species":"dog"}'
```

### Get All Pets
```bash
curl -X GET "http://localhost:8000/api/pets" \
  -H "Authorization: Bearer $TOKEN"
```

### Get Single Pet
```bash
curl -X GET "http://localhost:8000/api/pets/1" \
  -H "Authorization: Bearer $TOKEN"
```

### Update Pet
```bash
curl -X PUT "http://localhost:8000/api/pets/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"BuddyRenamed"}'
```

### Delete Pet
```bash
curl -X DELETE "http://localhost:8000/api/pets/1" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Testing with Swagger UI

1. Start the server: `python run.py`
2. Open: `http://localhost:8000/docs`
3. Click "Authorize" button in top-right
4. Enter: `Bearer <your_token>`
5. Click "Authorize"
6. Test each endpoint in the "pets" section

---

## Files Created

1. **`app/services/pet.py`** - PetService with CRUD operations
2. **`app/schemas/pet.py`** - Pet request/response schemas
3. **`app/routers/pets.py`** - Pet management endpoints
4. **`app/main.py`** - Updated to include pet routes

---

## Default Pet Focus

When a pet is created, it automatically gets the following focus distribution:
- **Strength:** 50% - Primary focus on strength building
- **Endurance:** 30% - Secondary focus on endurance
- **Speed:** 20% - Tertiary focus on speed

Users can modify this focus later in Phase 5.

---

## Pet Lifecycle

```
1. User creates pet
   ├── Pet created with level=1, exp=0, stage=1
   ├── PetFocus created with 50/30/20 distribution
   └── All XP values start at 0

2. User logs activities
   ├── Activity XP is distributed based on focus
   ├── Pet gains experience
   └── Checks for level up / evolution

3. User updates focus (Phase 5)
   ├── Change focus percentages
   └── Future activities use new distribution

4. User manages pets
   ├── Rename pet (Phase 4 ✓)
   ├── Delete pet (Phase 4 ✓)
   └── View pet details (Phase 4 ✓)
```

---

## Security Features

✅ **Ownership Verification** - Users can only access their own pets
✅ **Token Authentication** - All endpoints require valid JWT token
✅ **Data Validation** - Pet names and species are validated
✅ **Cascading Deletes** - Deleting pet cascades to activities/achievements

---

## Next Steps

**Phase 5: Focus System**
- Update endpoint `PUT /api/pets/{id}/focus`
- Validate focus percentages sum to 100
- Handle focus updates

**Phase 6: Activity System**
- Log fitness activities
- Calculate XP rewards based on focus
- Update pet stats

---

## Summary

✅ Pet creation with automatic default focus
✅ Full CRUD operations for pets
✅ Ownership verification for security
✅ Integration with authentication system
✅ Type-safe schemas and enums