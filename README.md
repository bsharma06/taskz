# Taskz - Modern Task Management Application

A full-stack task management application built with FastAPI (backend) and Next.js (frontend), featuring role-based access control, modern UI with dark theme, and comprehensive task management capabilities.

## 🚀 Features

### Backend Features

- **User Authentication**: JWT-based authentication with secure password hashing
- **Role-Based Access Control (RBAC)**: Admin and normal user roles with different permissions
- **User Management**: Create, read, update, and delete users with email validation
- **Task Management**: Full CRUD operations for tasks with status tracking
- **Email Normalization**: Automatic lowercase conversion for email addresses
- **CORS Support**: Configured for frontend communication

### Frontend Features

- **Modern UI**: Built with shadcn UI components and Tailwind CSS
- **Dark Theme**: Default dark mode with consistent design system
- **Responsive Design**: Mobile-first approach with collapsible sidebar
- **Dashboard**: Task statistics and comprehensive task table
- **Task Details Modal**: View full task information in a modal dialog
- **Authentication Pages**: Sign in and sign up with error handling

## 📋 Tech Stack

### Backend

- **Framework**: FastAPI 0.127.0
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens) with python-jose
- **Password Hashing**: bcrypt via passlib
- **Validation**: Pydantic for data validation
- **Testing**: pytest
- **Server**: Uvicorn ASGI server

### Frontend

- **Framework**: Next.js 14.2.5 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS 3.4.7
- **UI Components**: shadcn UI (Radix UI primitives)
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **State Management**: React Hooks

## 🛠️ Prerequisites

- **Python**: 3.13+ (or 3.8+)
- **Node.js**: 18+ and npm
- **PostgreSQL**: 12+ (for production) or SQLite (for development)
- **Git**: For version control

## 📦 Installation & Setup

### Backend Setup

1. **Navigate to backend directory**:

```bash
cd backend
```

1. **Create virtual environment** (recommended):

```bash
python -m venv venv
```

1. **Activate virtual environment**:
   - **Windows**:

   ```bash
   venv\Scripts\activate
   ```

   - **Linux/Mac**:

   ```bash
   source venv/bin/activate
   ```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

   Or install manually:

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic pydantic-settings python-jose[cryptography] passlib[bcrypt] python-multipart email-validator
```

1. **Create `.env` file** in the `backend` directory:

```env
DATABASE_URL=postgresql://postgres:password123@localhost:5432/taskz
JWT_SECRET=your-secret-key-here-change-in-production
```

1. **Initialize database**:

```bash
python -m app.db.init_db
```

### Frontend Setup

1. **Navigate to frontend directory**:

```bash
cd frontend
```

1. **Install dependencies**:

```bash
npm install
```

1. **Create `.env.local` file** in the `frontend` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🗄️ Database Configuration

### PostgreSQL Setup

**Connection Details**:

```
Server Name       = dev
Host Name/Address = localhost
Port              = 5432
Database          = postgres/taskz
User              = postgres
Password          = password123
```

**Start PostgreSQL Server** (Windows):

```bash
pg_ctl -D ../data -l ../logfile start
```

**Stop PostgreSQL Server**:

```bash
pg_ctl -D ../data stop
```

**Create Database**:

```sql
CREATE DATABASE taskz;
```

## 🚀 Running the Application

### Start Backend Server

```bash
cd backend
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

API Documentation (Swagger UI): `http://localhost:8000/docs`
Alternative API Docs (ReDoc): `http://localhost:8000/redoc`

### Start Frontend Server

```bash
cd frontend
npm run dev
```

The frontend will be available at: `http://localhost:3000`

## 📡 API Endpoints

### Authentication (`/auth`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/login` | User login (returns JWT token) | No |
| GET | `/auth/me` | Get current user information | Yes |

**Login Request**:

```bash
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com
password=yourpassword
```

**Response**:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Users (`/users`)

| Method | Endpoint | Description | Auth Required | Role Required |
|--------|----------|-------------|---------------|---------------|
| GET | `/users/` | List users | Yes | Admin: all users, Normal: self only |
| POST | `/users/` | Create new user | Optional* | - |
| GET | `/users/{user_id}` | Get user by ID | Yes | Admin: any user, Normal: self only |
| PUT | `/users/{user_id}` | Update user | Yes | Self only |
| DELETE | `/users/{user_id}` | Delete user | Yes | Self only |

*User creation without auth is allowed for new users. If user exists, auth is required.

**Create User Request**:

```json
POST /users/
{
  "user_email": "user@example.com",
  "user_name": "John Doe",
  "pwd": "password123",
  "role": "normal"
}
```

### Tasks (`/tasks`)

| Method | Endpoint | Description | Auth Required | Role Required |
|--------|----------|-------------|---------------|---------------|
| GET | `/tasks/` | List tasks | Yes | Admin: all tasks, Normal: own tasks |
| POST | `/tasks/` | Create new task | Yes | - |
| GET | `/tasks/{task_id}` | Get task by ID | Yes | Admin: any task, Normal: own tasks |
| PUT | `/tasks/{task_id}` | Update task | Yes | Admin: any task, Normal: own tasks |
| DELETE | `/tasks/{task_id}` | Delete task | Yes | Admin: any task, Normal: own tasks |

**Create Task Request**:

```json
POST /tasks/
{
  "title": "Complete project",
  "description": "Finish the task management app",
  "start_date": "2024-01-01T00:00:00Z",
  "due_date": "2024-01-15T00:00:00Z",
  "priority": "high",
  "status": "pending",
  "created_by": "user@example.com",
  "assigned_to": "user@example.com"
}
```

**Task Status Values**: `pending`, `in_progress`, `completed`

**Task Priority Values**: `low`, `medium`, `high`

## 🔐 Authentication

All protected endpoints require a Bearer token in the Authorization header:

```bash
Authorization: Bearer <your-jwt-token>
```

## 🎨 Frontend Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── dashboard/         # Dashboard page with tasks
│   ├── signin/            # Sign in page
│   ├── signup/            # Sign up page
│   ├── layout.tsx         # Root layout with dark theme
│   └── globals.css        # Global styles and theme
├── components/            # React components
│   ├── ui/                # shadcn UI components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── dialog.tsx
│   │   ├── table.tsx
│   │   └── badge.tsx
│   ├── Sidebar.tsx        # Collapsible navigation sidebar
│   ├── MobileMenu.tsx     # Mobile navigation menu
│   ├── StatsCards.tsx     # Statistics cards component
│   ├── TaskTable.tsx       # Task table component
│   └── TaskDetailModal.tsx # Task detail modal
├── lib/                   # Utility functions
│   ├── api.ts             # API client and interfaces
│   ├── auth.ts            # Authentication utilities
│   └── utils.ts           # Helper functions
└── package.json           # Dependencies
```

## 🏗️ Backend Structure

```
backend/
├── app/
│   ├── api/
│   │   └── routes/        # API route handlers
│   │       ├── auth.py    # Authentication routes
│   │       ├── users.py   # User management routes
│   │       └── tasks.py   # Task management routes
│   ├── core/              # Core functionality
│   │   ├── config.py      # Application configuration
│   │   └── security.py    # Security utilities (JWT, password hashing)
│   ├── db/                # Database configuration
│   │   ├── session.py     # Database session
│   │   └── init_db.py     # Database initialization
│   ├── models/            # SQLAlchemy models
│   │   ├── user.py        # User model
│   │   └── task.py        # Task model
│   ├── schemas/           # Pydantic schemas
│   │   ├── user_schema.py # User request/response schemas
│   │   └── task_schema.py # Task request/response schemas
│   └── main.py            # FastAPI application entry point
├── tests/                 # Test files
│   ├── conftest.py        # Pytest configuration
│   ├── test_auth.py       # Authentication tests
│   ├── test_users.py      # User management tests
│   └── test_tasks.py      # Task management tests
└── requirements.txt       # Python dependencies
```

## 🧪 Testing

### Backend Tests

Run all tests:

```bash
cd backend
pytest
```

Run with verbose output:

```bash
pytest -v
```

Run specific test file:

```bash
pytest tests/test_users.py
```

### Frontend Tests

Currently, frontend tests are not set up. To add testing:

```bash
npm install --save-dev @testing-library/react @testing-library/jest-dom jest
```

## 🔒 Security Features

- **Password Hashing**: Bcrypt with salt rounds
- **JWT Tokens**: Secure token-based authentication
- **Email Normalization**: Automatic lowercase conversion
- **Role-Based Access**: Admin and normal user permissions
- **CORS Protection**: Configured for specific origins
- **Input Validation**: Pydantic schema validation

## 📝 Environment Variables

### Backend (`.env`)

```env
DATABASE_URL=postgresql://user:password@localhost:5432/taskz
JWT_SECRET=your-secret-key-change-in-production
```

### Frontend (`.env.local`)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🎯 Role-Based Access Control

### Admin Role

- Can view all users
- Can view all tasks
- Can manage any task
- Full system access

### Normal User Role

- Can only view own user profile
- Can only view tasks created by or assigned to them
- Can only manage own tasks
- Limited access scope

## 🐛 Troubleshooting

### Backend Issues

**Database Connection Error**:

- Verify PostgreSQL is running
- Check DATABASE_URL in `.env` file
- Ensure database exists: `CREATE DATABASE taskz;`

**Import Errors**:

- Activate virtual environment
- Install all dependencies: `pip install -r requirements.txt`

**CORS Errors**:

- Verify CORS middleware is configured in `main.py`
- Check frontend URL matches allowed origins

### Frontend Issues

**API Connection Error**:

- Verify backend server is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Verify CORS is configured in backend

**Build Errors**:

- Delete `node_modules` and `package-lock.json`
- Run `npm install` again
- Clear Next.js cache: `rm -rf .next`

**Type Errors**:

- Run `npm run build` to check for TypeScript errors
- Ensure all dependencies are installed

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [shadcn UI Components](https://ui.shadcn.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a pull request



## 👥 Developer

Developed for task management and productivity tracking.
_Bhoopesh Sharma_

---

**Note**: Remember to change the JWT_SECRET and database credentials in production environments!
