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

- `GET /api/crews/` - List all accessible crews (public, invite-only, or member of)
- `GET /api/crews/{id}/` - Get crew details
- `POST /api/crews/{id}/join/` - Join a crew
- `POST /api/crews/{id}/leave/` - Leave a crew

- `GET /api/my-crews/` - List crews owned by current user
- `POST /api/my-crews/` - Create new crew
- `GET /api/my-crews/{id}/` - Get owned crew details
- `PUT /api/my-crews/{id}/` - Update owned crew
- `PATCH /api/my-crews/{id}/` - Partial update owned crew
- `DELETE /api/my-crews/{id}/` - Delete owned crew

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

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Contact

Yash - [GitHub](https://github.com/yash2974)

Project Link: [https://github.com/yash2974/backend-moto](https://github.com/yash2974/backend-moto)
