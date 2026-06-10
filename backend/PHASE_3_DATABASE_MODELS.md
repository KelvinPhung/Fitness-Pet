# Phase 3 - Database Models

## Overview

This phase implements all core database models with proper relationships and constraints. The models form the backbone of the application's data structure.

## Database Schema

### Users Table
```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(120) UNIQUE NOT NULL,
  hashed_password VARCHAR(255) NOT NULL,
  is_active BOOLEAN DEFAULT TRUE,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL
);
```

### Pets Table
```sql
CREATE TABLE pets (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL FOREIGN KEY,
  name VARCHAR(100) NOT NULL,
  species VARCHAR(50) NOT NULL,
  level INTEGER DEFAULT 1,
  experience INTEGER DEFAULT 0,
  evolution_stage INTEGER DEFAULT 1,
  strength_xp INTEGER DEFAULT 0,
  endurance_xp INTEGER DEFAULT 0,
  speed_xp INTEGER DEFAULT 0,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL
);
```

### Pet Focus Table
```sql
CREATE TABLE pet_focus (
  id INTEGER PRIMARY KEY,
  pet_id INTEGER NOT NULL UNIQUE FOREIGN KEY,
  strength_focus INTEGER DEFAULT 50,
  endurance_focus INTEGER DEFAULT 30,
  speed_focus INTEGER DEFAULT 20,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL
);
```

### Activities Table
```sql
CREATE TABLE activities (
  id INTEGER PRIMARY KEY,
  pet_id INTEGER NOT NULL FOREIGN KEY,
  user_id INTEGER NOT NULL FOREIGN KEY,
  activity_type VARCHAR(50) NOT NULL,
  distance FLOAT DEFAULT 0,
  duration INTEGER NOT NULL,
  intensity VARCHAR(50) DEFAULT 'moderate',
  strength_xp INTEGER DEFAULT 0,
  endurance_xp INTEGER DEFAULT 0,
  speed_xp INTEGER DEFAULT 0,
  total_xp INTEGER DEFAULT 0,
  notes TEXT,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL
);
```

### Achievements Table
```sql
CREATE TABLE achievement_definitions (
  id INTEGER PRIMARY KEY,
  slug VARCHAR(100) UNIQUE NOT NULL,
  name VARCHAR(200) NOT NULL,
  description TEXT NOT NULL,
  icon VARCHAR(255)
);

CREATE TABLE achievements (
  id INTEGER PRIMARY KEY,
  pet_id INTEGER NOT NULL FOREIGN KEY,
  achievement_def_id INTEGER NOT NULL FOREIGN KEY,
  unlocked_at DATETIME NOT NULL
);
```

### Friendships Table
```sql
CREATE TABLE friendships (
  id INTEGER PRIMARY KEY,
  requester_id INTEGER NOT NULL FOREIGN KEY,
  receiver_id INTEGER NOT NULL FOREIGN KEY,
  status VARCHAR(50) DEFAULT 'pending',
  requested_at DATETIME NOT NULL,
  responded_at DATETIME,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL
);
```

## Models Overview

### 1. User (app/models/user.py)
Core user model for authentication and account management.

**Key Fields:**
- `id` - Unique identifier
- `username` - Unique username
- `email` - Unique email address
- `hashed_password` - Bcrypt hashed password
- `is_active` - Account status
- `created_at`, `updated_at` - Timestamps

**Relationships:**
- `pets` - One-to-many with Pet model
- `friend_requests_sent` - One-to-many with Friendship (as requester)
- `friend_requests_received` - One-to-many with Friendship (as receiver)
- `activities` - One-to-many with Activity

### 2. Pet (app/models/pet.py)
Virtual pet model that evolves based on user's fitness activities.

**Key Fields:**
- `id` - Unique identifier
- `user_id` - Owner (FK to User)
- `name` - Pet's name
- `species` - Type (dog, cat, rabbit, bird, dragon)
- `level` - Current level (1+)
- `experience` - Current XP (0+)
- `evolution_stage` - Visual stage (1-5)
- `strength_xp`, `endurance_xp`, `speed_xp` - Stat XP totals

**Enums:**
- `PetSpecies`: dog, cat, rabbit, bird, dragon

**Relationships:**
- `user` - Many-to-one with User
- `pet_focus` - One-to-one with PetFocus
- `activities` - One-to-many with Activity
- `achievements` - One-to-many with Achievement
- `unlocked_achievements` - One-to-many with Achievement

### 3. PetFocus (app/models/pet_focus.py)
Tracks the user's priorities for stat distribution.

**Key Fields:**
- `id` - Unique identifier
- `pet_id` - Pet owner (FK to Pet, unique)
- `strength_focus` - Strength priority (0-100%)
- `endurance_focus` - Endurance priority (0-100%)
- `speed_focus` - Speed priority (0-100%)

**Constraints:**
- Sum of focus values must equal 100%
- One-to-one with Pet (only one focus per pet)

**Methods:**
- `validate_focus()` - Ensures totals equal 100

**Example:**
```python
# User focuses on strength training and endurance
pet_focus = PetFocus(
    pet_id=1,
    strength_focus=50,
    endurance_focus=40,
    speed_focus=10
)
```

### 4. Activity (app/models/activity.py)
Logs individual fitness activities and XP rewards.

**Key Fields:**
- `id` - Unique identifier
- `pet_id` - Which pet gets XP (FK to Pet)
- `user_id` - Who did the activity (FK to User)
- `activity_type` - Type of activity
- `distance` - Distance in kilometers
- `duration` - Duration in minutes
- `intensity` - Low/moderate/high
- `strength_xp`, `endurance_xp`, `speed_xp` - XP distributed
- `total_xp` - Total XP awarded
- `notes` - Optional user notes

**Enums:**
- `ActivityType`: running, walking, cycling, swimming, strength_training, yoga, sports, hiit, cardio, other

**Relationships:**
- `pet` - Many-to-one with Pet
- `user` - Many-to-one with User

**Example:**
```python
# User runs 10km in 60 minutes
activity = Activity(
    pet_id=1,
    user_id=1,
    activity_type="running",
    distance=10.0,
    duration=60,
    intensity="high",
    strength_xp=50,
    endurance_xp=100,
    speed_xp=50,
    total_xp=200
)
```

### 5. Achievement (app/models/achievement.py)
Tracks unlocked achievements/badges.

**Models:**

#### AchievementDefinition
Template for achievements. Pre-populated with standard achievements.

**Key Fields:**
- `id` - Unique identifier
- `slug` - Unique identifier (first_activity, 10km_walked, etc.)
- `name` - Display name
- `description` - Description
- `icon` - Asset path or URL

**Example Achievements:**
- `first_activity` - "First Steps" - Complete your first activity
- `10km_walked` - "Walking Distance" - Walk 10km total
- `100km_total` - "Adventurer" - Complete 100km in activities
- `first_evolution` - "Evolution!" - Reach stage 2
- `7_day_streak` - "Consistency" - Log activity 7 days in a row
- `reach_level_10` - "Level Master" - Reach level 10
- `all_activities` - "Versatile" - Complete all activity types

#### Achievement
Instance of unlocked achievement for a specific pet.

**Key Fields:**
- `id` - Unique identifier
- `pet_id` - Which pet unlocked it (FK to Pet)
- `achievement_def_id` - Which achievement (FK to AchievementDefinition)
- `unlocked_at` - When it was unlocked

**Relationships:**
- `pet` - Many-to-one with Pet
- `definition` - Many-to-one with AchievementDefinition

### 6. Friendship (app/models/friendship.py)
Manages connections between users for comparing pet progress.

**Key Fields:**
- `id` - Unique identifier
- `requester_id` - User sending request (FK to User)
- `receiver_id` - User receiving request (FK to User)
- `status` - pending/accepted/blocked
- `requested_at` - When request was sent
- `responded_at` - When it was accepted/rejected
- `created_at`, `updated_at` - Timestamps

**Enums:**
- `FriendshipStatus`: pending, accepted, blocked

**Relationships:**
- `requester` - Many-to-one with User
- `receiver` - Many-to-one with User

**Example Flow:**
```
1. User A sends friend request to User B
   Friendship(requester_id=1, receiver_id=2, status="pending")

2. User B accepts request
   Friendship.status = "accepted"
   Friendship.responded_at = now()

3. Users can now see each other's pet progress
```

## Relationships Diagram

```
User (1) ──────── (M) Pet
                    │
                    ├── (1) PetFocus
                    ├── (M) Activity
                    └── (M) Achievement

User (M) ────── (M) Friendship (M) ──── User

Activity (M) ──── (1) User
Activity (M) ──── (1) Pet

Achievement (M) ──── (1) AchievementDefinition
Achievement (M) ──── (1) Pet
```

## Key Design Decisions

### 1. Pet Focus as Separate Model
- Simplifies queries for user priorities
- Easy to update without affecting Pet
- Allows historical tracking if needed in future

### 2. Activity Logs Both Pet and User
- Enables user activity history
- Enables pet activity history
- Supports multiple pets per user

### 3. Achievement Definitions Separate from Unlocked
- Allows defining achievements without unlocking
- Easy to add new achievements
- Supports achievement rarity/difficulty levels in future

### 4. Friendship Cascading Deletes
- When user is deleted, all friendships deleted
- Maintains data integrity
- No orphaned friendship records

## Model Validation

### Pet Focus Validation
```python
def validate_focus(self) -> bool:
    total = self.strength_focus + self.endurance_focus + self.speed_focus
    return total == 100
```

### Database Constraints
- Username and Email are UNIQUE
- Foreign keys cascade on DELETE
- Required fields are NOT NULL
- Timestamps auto-update

## Next Steps

**Phase 4: Pet Creation System**
- Create endpoint `POST /api/pets/create`
- Initialize pet with default values
- Create default PetFocus (50/30/20)
- Auto-create database tables

**Phase 5: Focus System**
- Create endpoint `POST /api/pets/{id}/focus`
- Update PetFocus values
- Validate focus percentages

**Phase 6: XP Engine**
- Implement XP calculation service
- Map activities to stat rewards
- Handle focus distribution

## Files Created

1. `app/models/user.py` - User model (from Phase 2)
2. `app/models/pet.py` - Pet model with species enum
3. `app/models/pet_focus.py` - Pet focus distribution model
4. `app/models/activity.py` - Activity logging model
5. `app/models/achievement.py` - Achievement models
6. `app/models/friendship.py` - Friendship model
7. `app/models/__init__.py` - Models package exports

## Testing Models

```python
from app.models import Pet, PetSpecies, PetFocus, Activity, ActivityType

# Create a pet
pet = Pet(
    user_id=1,
    name="Buddy",
    species=PetSpecies.DOG,
    level=1,
    experience=0,
    evolution_stage=1
)

# Create focus
focus = PetFocus(
    pet_id=1,
    strength_focus=50,
    endurance_focus=30,
    speed_focus=20
)

# Log activity
activity = Activity(
    pet_id=1,
    user_id=1,
    activity_type=ActivityType.RUNNING,
    distance=5.0,
    duration=30,
    intensity="moderate",
    total_xp=150
)
```
