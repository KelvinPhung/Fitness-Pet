# Phase 3 - Database Models

## Overview

This phase implements all core database models with proper relationships and constraints. The models form the backbone of the application's data structure.

## Models Created

### 1. Pet Model
Virtual pet that evolves based on user's fitness activities.

**Key Fields:**
- `id` - Unique identifier
- `user_id` - Owner (FK to User)
- `name` - Pet's name
- `species` - Type (dog, cat, rabbit, bird, dragon)
- `level` - Current level (1+)
- `experience` - Current XP (0+)
- `evolution_stage` - Visual stage (1-5)
- `strength_xp`, `endurance_xp`, `speed_xp` - Stat XP totals

**Relationships:**
- One-to-one with PetFocus
- One-to-many with Activity
- One-to-many with Achievement

### 2. PetFocus Model
Tracks the user's priorities for stat distribution.

**Key Fields:**
- `pet_id` - Pet owner (FK to Pet, unique)
- `strength_focus` - Strength priority (0-100%)
- `endurance_focus` - Endurance priority (0-100%)
- `speed_focus` - Speed priority (0-100%)

**Constraint:** Sum of focus values must equal 100%

**Example:**
```python
pet_focus = PetFocus(
    pet_id=1,
    strength_focus=50,
    endurance_focus=40,
    speed_focus=10
)
```

### 3. Activity Model
Logs individual fitness activities and XP rewards.

**Key Fields:**
- `pet_id` - Which pet gets XP (FK to Pet)
- `user_id` - Who did the activity (FK to User)
- `activity_type` - Type of activity (running, cycling, etc.)
- `distance` - Distance in kilometers
- `duration` - Duration in minutes
- `intensity` - Low/moderate/high
- `strength_xp`, `endurance_xp`, `speed_xp` - XP distributed
- `total_xp` - Total XP awarded

**Activity Types:**
- running, walking, cycling, swimming, strength_training, yoga, sports, hiit, cardio, other

### 4. Achievement Model
Tracks unlocked achievements/badges.

**Two Tables:**

**AchievementDefinition** - Template for achievements
- `slug` - Unique identifier (first_activity, 10km_walked, etc.)
- `name` - Display name
- `description` - Description
- `icon` - Asset path or URL

**Achievement** - Instance of unlocked achievement
- `pet_id` - Which pet unlocked it (FK to Pet)
- `achievement_def_id` - Which achievement (FK to AchievementDefinition)
- `unlocked_at` - When it was unlocked

### 5. Friendship Model
Manages connections between users for comparing pet progress.

**Key Fields:**
- `requester_id` - User sending request (FK to User)
- `receiver_id` - User receiving request (FK to User)
- `status` - pending/accepted/blocked
- `requested_at` - When request was sent
- `responded_at` - When it was accepted/rejected

**Status Options:**
- `pending` - Awaiting response
- `accepted` - Friends
- `blocked` - User blocked another

## Database Schema

```
USERS (1) ──── (M) PETS
              ├── (1) PET_FOCUS
              ├── (M) ACTIVITIES
              └── (M) ACHIEVEMENTS

USERS (M) ──── (M) FRIENDSHIPS (M) ──── USERS

ACTIVITIES (M) ──── (1) USERS
ACTIVITIES (M) ──── (1) PETS

ACHIEVEMENTS (M) ──── (1) ACHIEVEMENT_DEFINITIONS
ACHIEVEMENTS (M) ──── (1) PETS
```

## Key Features

✅ **Cascading Deletes** - When user/pet deleted, related records cleaned up
✅ **Unique Constraints** - Username, email, pet_focus per pet
✅ **Timestamps** - All models track created_at and updated_at
✅ **Relationships** - Proper foreign keys and backlinks
✅ **Enums** - Type-safe activity types, pet species, friendship status
✅ **Validation** - PetFocus validates focus percentages

## Files Created

1. `app/models/pet.py` - Pet model with species enum
2. `app/models/pet_focus.py` - Pet focus distribution model
3. `app/models/activity.py` - Activity logging model
4. `app/models/achievement.py` - Achievement models
5. `app/models/friendship.py` - Friendship model
6. `app/models/__init__.py` - Models package exports

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

## All Models Are Now Integrated

The application database is fully structured and ready for:
- Pet management
- Activity tracking
- Achievement system
- Friend connections
- User progression
