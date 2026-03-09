# Kickstand Backend API

A Django REST Framework backend for a motorcycle/vehicle management and social platform. Track your vehicles, manage expenses, and connect with other riders through crews.

## Features

- **Vehicle Management** - Track your motorcycles and vehicles with specs, service history, and images
- **Expense Tracking** - Monitor fuel, maintenance, repairs, insurance, and other vehicle expenses
- **Social Crews** - Create and join riding crews with different privacy levels
- **Authentication** - JWT-based user authentication and authorization
- **Service Reminders** - Track service intervals and last service dates

## Tech Stack

- **Framework:** Django 6.0.1
- **API:** Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** JWT (djangorestframework-simplejwt)
- **Python:** 3.13

## Data Models

### BaseModel (Abstract)

All models inherit from BaseModel which provides:

- `created_at` - Timestamp when record was created
- `updated_at` - Timestamp when record was last updated

### Vehicle

Track motorcycles and vehicles with detailed information.

**Fields:**

- `owner` - Foreign key to User
- `make` - Vehicle manufacturer (e.g., Honda, Harley-Davidson)
- `model` - Vehicle model name
- `year` - Manufacturing year
- `license_plate` - Unique license plate (optional, indexed)
- `image_url` - URL to vehicle image
- `last_service_date` - Date of last service
- `service_interval` - Service interval in kilometers
- `specs` - JSON field for flexible vehicle specifications

**Relationships:**

- One vehicle belongs to one user (owner)
- One vehicle can have many expenses

### Expense

Track all vehicle-related expenses.

**Fields:**

- `owner` - Foreign key to User
- `vehicle` - Foreign key to Vehicle
- `amount` - Expense amount (decimal)
- `date` - Date and time of expense
- `category` - One of: Fuel, Maintenance, Repair, Insurance, Other
- `description` - Optional notes about the expense

**Relationships:**

- One expense belongs to one user
- One expense is associated with one vehicle

### Crew

Social groups for riders to connect and organize rides.

**Fields:**

- `name` - Unique crew name
- `description` - Crew description
- `type` - One of: Sports, Adventure, Cruising, Offroad
- `logo_url` - URL to crew logo
- `owner` - Foreign key to User (crew creator)
- `members` - Many-to-many relationship with User
- `country` - Location (optional)
- `city` - City (optional)
- `is_private` - One of: Public, Private, Invite Only

**Relationships:**

- One crew has one owner
- One crew can have many members (users)
- One user can be in many crews

## API Endpoints

### Authentication

- `POST /api/users/register/` - Register new user
- `POST /api/users/login/` - Login and get JWT tokens
- `GET /api/users/me/` - Get current user details
- `PUT /api/users/me/update/` - Update user profile

### Vehicles

- `GET /api/vehicles/` - List all user's vehicles
- `POST /api/vehicles/` - Create new vehicle
- `GET /api/vehicles/{id}/` - Get vehicle details
- `PUT /api/vehicles/{id}/` - Update vehicle
- `PATCH /api/vehicles/{id}/` - Partial update vehicle
- `DELETE /api/vehicles/{id}/` - Delete vehicle

### Expenses

- `GET /api/expenses/` - List all user's expenses
- `POST /api/expenses/` - Create new expense
- `GET /api/expenses/{id}/` - Get expense details
- `PUT /api/expenses/{id}/` - Update expense
- `PATCH /api/expenses/{id}/` - Partial update expense
- `DELETE /api/expenses/{id}/` - Delete expense

### Crews

**Public Crews:**

- `GET /api/crews/` - List all accessible crews (public, invite-only, or member of)
- `GET /api/crews/{id}/` - Get crew details
- `POST /api/crews/{id}/join/` - Join a crew (immediate for public, creates request for invite-only)
- `POST /api/crews/{id}/leave/` - Leave a crew

**Owned Crews:**

- `GET /api/my-crews/` - List crews owned by current user
- `POST /api/my-crews/` - Create new crew
- `GET /api/my-crews/{id}/` - Get owned crew details
- `PUT /api/my-crews/{id}/` - Update owned crew
- `PATCH /api/my-crews/{id}/` - Partial update owned crew
- `DELETE /api/my-crews/{id}/` - Delete owned crew

**Request Management (Owner Only):**

- `GET /api/my-crews/{id}/requests/` - Get pending join requests for a crew
- `POST /api/my-crews/{id}/requests/{request_id}/approve/` - Approve a join request
- `POST /api/my-crews/{id}/requests/{request_id}/reject/` - Reject a join request

## Installation & Setup

### Prerequisites

- Python 3.13+
- PostgreSQL
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/yash2974/backend-moto.git
cd backend-moto
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=backend
DB_USER=postgres
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=5432
```

See `.env.example` for a template.

### 5. Database Setup

```bash
# Create PostgreSQL database
createdb backend

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

### 7. Access Admin Panel

Visit `http://localhost:8000/admin/` and login with your superuser credentials.

## Usage Examples

### Register a New User

```bash
POST /api/users/register/
Content-Type: application/json

{
  "username": "rider123",
  "email": "rider@example.com",
  "password": "securepassword"
}
```

### Create a Vehicle

```bash
POST /api/vehicles/
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
  "make": "Honda",
  "model": "CBR600RR",
  "year": 2023,
  "license_plate": "ABC123",
  "image_url": "https://example.com/bike.jpg",
  "specs": {
    "engine": "599cc",
    "power": "120hp",
    "weight": "196kg"
  }
}
```

### Track an Expense

```bash
POST /api/expenses/
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
  "vehicle": 1,
  "amount": 45.50,
  "category": "Fuel",
  "description": "Fill up at Shell station"
}
```

### Create a Crew

```bash
POST /api/my-crews/
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
  "name": "Speed Demons",
  "description": "For riders who love adrenaline",
  "type": "Sports",
  "country": "USA",
  "city": "Los Angeles",
  "is_private": "Public"
}
```

## Project Structure

```
kickstanddrfbackend/
├── crews/              # Crew management app
├── expenses/           # Expense tracking app
├── vehicles/           # Vehicle management app
├── users/              # User authentication app
├── kickstanddrfbackend/# Main project settings
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
```

## Security Features

- JWT token-based authentication
- Environment variable configuration for secrets
- Password validation
- CSRF protection
- User-scoped data access (users can only access their own data)

## Testing

The project includes comprehensive test coverage for all key features. Tests are organized by app and cover models, API endpoints, permissions, and edge cases.

### Running Tests

Run all tests:

```bash
python manage.py test
```

Run tests for a specific app:

```bash
python manage.py test crews
python manage.py test vehicles
python manage.py test expenses
python manage.py test users
```

Run a specific test class:

```bash
python manage.py test crews.tests.CrewJoinAPITestCase
```

Run with verbose output:

```bash
python manage.py test --verbosity=2
```

### Crew Tests

**Test Coverage: 23 tests**

#### Model Tests (2 tests)

- `test_create_crew` - Verify crew model creation
- `test_crew_string_representation` - Test **str** method

#### Crew Creation Tests (5 tests)

- `test_create_public_crew` - Create a public crew with all fields
- `test_create_invite_only_crew` - Create an invite-only crew
- `test_create_crew_without_auth` - Verify authentication is required
- `test_create_crew_duplicate_name` - Test unique name constraint
- Owner is automatically added as a member upon creation

#### Join Crew Tests (5 tests)

- `test_join_public_crew` - Join a public crew (immediate membership)
- `test_join_invite_only_crew` - Join invite-only crew (creates pending request)
- `test_join_already_member` - Prevent duplicate memberships
- `test_join_as_owner` - Owner cannot join their own crew
- `test_join_request_duplicate` - Prevent duplicate join requests

#### Leave Crew Tests (3 tests)

- `test_leave_crew` - Successfully leave a crew
- `test_owner_cannot_leave` - Owner cannot leave their own crew
- `test_leave_when_not_member` - Cannot leave if not a member

#### Request Management Tests (6 tests)

- `test_get_pending_requests` - List all pending join requests
- `test_approve_request` - Approve a join request (adds member to crew)
- `test_reject_request` - Reject a join request
- `test_process_already_processed_request` - Cannot process twice
- `test_process_nonexistent_request` - Handle invalid request IDs
- `test_non_owner_cannot_process_request` - Only owners can manage requests

#### Crew Listing Tests (3 tests)

- `test_list_crews_authenticated` - List visible crews based on privacy
- `test_list_my_crews` - List only crews owned by user
- `test_list_crews_unauthenticated` - Require authentication

### Test Database

Tests use a separate test database that is automatically created and destroyed:

- Database: `test_<your_database_name>`
- All migrations are applied automatically
- Test data is isolated from production/development data

### Writing New Tests

When adding new features, follow these testing patterns:

1. **Create test file** in the app's `tests.py`
2. **Import required modules:**
   ```python
   from rest_framework.test import APITestCase, APIClient
   from rest_framework import status
   from django.contrib.auth.models import User
   ```
3. **Use `setUp()` method** to create test data
4. **Test positive and negative cases**
5. **Verify database state changes** after operations
6. **Check response status codes and messages**

Example test structure:

```python
class MyFeatureTestCase(APITestCase):
    def setUp(self):
        # Create test users and data
        self.user = User.objects.create_user(username='test', password='pass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_feature_success(self):
        # Test successful operation
        response = self.client.post('/api/endpoint/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_feature_validation_error(self):
        # Test validation errors
        response = self.client.post('/api/endpoint/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
```

### Continuous Integration

Tests should pass before merging any pull request. Run tests locally before pushing:

```bash
# Run all tests
python manage.py test

# Check for any errors
echo $?  # Should output 0 if all tests pass
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. **Write tests for your changes**
4. **Ensure all tests pass** (`python manage.py test`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Contact

Yash - [GitHub](https://github.com/yash2974)

Project Link: [https://github.com/yash2974/backend-moto](https://github.com/yash2974/backend-moto)
