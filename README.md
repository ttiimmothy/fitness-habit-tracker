# Fitness & Habit Tracker

A full-stack application for tracking fitness habits and building healthy routines. Built with Astro, React, FastAPI, and PostgreSQL.

## Features

- 🏃 **Habit Management**: Create and manage daily/weekly fitness habits
- 📊 **Progress Tracking**: Visualize your progress with interactive charts
- 🔥 **Streak Counter**: Track current and longest streaks for motivation
- 🏆 **Achievement Badges**: Unlock badges for milestones and consistency
- 📈 **Analytics Dashboard**: View detailed statistics and progress over time
- 🌙 **Dark Mode**: Toggle between light and dark themes
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile
- 🔐 **Secure Authentication**: JWT-based authentication with password hashing + Google OAuth
- ⚡ **Real-time Updates**: Fast and responsive user interface

## Tech Stack

### Frontend
- **Astro 5** with TypeScript
- **React 18** for interactive components
- **Tailwind CSS** for styling
- **Zustand** for state management
- **React Query** for data fetching and caching
- **Recharts** for data visualization
- **React Hook Form** with Zod validation
- **Lucide React** for icons
- **Day.js** for date manipulation

### Backend
- **FastAPI** with Python 3.11
- **SQLAlchemy 2.0** with Alembic for database management
- **PostgreSQL** database
- **Redis** for rate limiting and caching
- **JWT** authentication with python-jose
- **Pydantic** for data validation and settings
- **uv** for dependency management
- **Pytest** for testing

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Node.js 18+
- uv (Python package manager)
- Git

### 1. Clone the repository
```bash
git clone https://github.com/your-username/fitness_habit_tracker
cd fitness_habit_tracker
```

### 2. For development

#### 1. Start the database and services
```bash
docker compose up --build
```

#### 2. Set up the backend
```bash
cd backend
cp .env.example .env
# Edit .env with your database URL and JWT secret
uv sync
uv run alembic revision --autogenerate -m "init schema"
uv run alembic upgrade head
uv run python seed.py
```

#### 3. Set up the frontend
```bash
cd client
cp .env.example .env
# Edit .env with your API URL
npm install
npm run dev
```

#### 4. Access the application
- Frontend: http://localhost:4321
- Backend API: http://localhost:8000
- Database: localhost:5432
- Redis: localhost:6379

## Demo Credentials

The application comes with seeded demo data. You can log in with:
- **Email**: demo@example.com
- **Password**: Demo123!

## Project Structure

```
fitness_habit_tracker/
├── client/                     # Astro frontend application
│   ├── src/
│   │   ├── components/         # Astro and React components
│   │   │   ├── Avatar.tsx
│   │   │   ├── Footer.astro
│   │   │   └── Header.astro
│   │   ├── config/             # Configuration files
│   │   │   └── oauth.ts
│   │   ├── hooks/              # Custom React hooks
│   │   │   ├── useAuth.ts
│   │   │   ├── useBadges.ts
│   │   │   ├── useHabitLog.ts
│   │   │   ├── useHabits.ts
│   │   │   └── useStats.ts
│   │   ├── islands/            # React interactive components
│   │   │   ├── react/          # React components
│   │   │   ├── AccountActionIsland.tsx
│   │   │   ├── BadgesIsland.tsx
│   │   │   ├── CalendarIsland.tsx
│   │   │   ├── GoogleLoginButtonIsland.tsx
│   │   │   ├── HabitCardIsland.tsx
│   │   │   ├── IndividualHabitChartIsland.tsx
│   │   │   ├── LoginFormIsland.tsx
│   │   │   ├── ProgressChartIsland.tsx
│   │   │   ├── RegisterFormIsland.tsx
│   │   │   ├── StreakCounterIsland.tsx
│   │   │   ├── UserMenuIsland.tsx
│   │   │   └── UserProfileIsland.tsx
│   │   ├── lib/                # API client and utilities
│   │   │   ├── api.ts
│   │   │   ├── avatar.ts
│   │   │   ├── dayjs.ts
│   │   │   ├── getQueryClient.ts
│   │   │   └── googleAuth.ts
│   │   ├── pages/              # Astro pages
│   │   │   ├── auth/
│   │   │   │   └── google/
│   │   │   │       └── callback.astro
│   │   │   ├── badge-intro.astro
│   │   │   ├── badge.astro
│   │   │   ├── habit/
│   │   │   │   └── [id].astro
│   │   │   ├── index.astro
│   │   │   ├── login.astro
│   │   │   ├── register.astro
│   │   │   ├── setup-password.astro
│   │   │   └── user.astro
│   │   ├── providers/          # React context providers
│   │   │   ├── AuthGuard.tsx
│   │   │   ├── AuthProvider.tsx
│   │   │   ├── GoogleLoginProvider.tsx
│   │   │   └── QueryProvider.tsx
│   │   ├── schemas/            # Zod validation schemas
│   │   │   ├── authSchemas.ts
│   │   │   ├── badgeSchemas.ts
│   │   │   └── habitSchemas.ts
│   │   ├── store/              # Zustand stores
│   │   │   ├── authStore.ts
│   │   │   └── habitStore.ts
│   │   ├── styles/             # Global CSS
│   │   │   └── global.css
│   │   └── layouts/
│   │       └── Layout.astro
│   ├── public/                 # Static assets
│   │   ├── default-avatar-dark.svg
│   │   ├── default-avatar.svg
│   │   └── favicon.svg
│   ├── astro.config.mjs
│   ├── package.json
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── vercel.json
│   └── Dockerfile
├── backend/                    # FastAPI backend application
│   ├── app/
│   │   ├── api/                # API dependencies
│   │   │   └── middleware/
│   │   │       └── get_current_user.py
│   │   ├── core/               # Core configuration
│   │   │   ├── config.py
│   │   │   ├── rate_limit.py
│   │   │   └── security.py
│   │   ├── db/                 # Database configuration
│   │   │   ├── base.py
│   │   │   ├── base_model_imports.py
│   │   │   └── session.py
│   │   ├── lib/                # Utility libraries
│   │   │   └── get_or_create_user.py
│   │   ├── models/             # SQLAlchemy models
│   │   │   ├── badge.py
│   │   │   ├── habit.py
│   │   │   ├── habit_log.py
│   │   │   └── user.py
│   │   ├── routers/            # API route handlers
│   │   │   ├── auth.py
│   │   │   ├── badges.py
│   │   │   ├── habits.py
│   │   │   ├── logs.py
│   │   │   └── stats.py
│   │   ├── schemas/            # Pydantic schemas
│   │   │   ├── auth.py
│   │   │   ├── badge.py
│   │   │   ├── habit.py
│   │   │   ├── habit_log.py
│   │   │   ├── stats.py
│   │   │   └── user.py
│   │   ├── services/           # Business logic
│   │   │   └── setup_initial_habits.py
│   │   ├── main.py             # FastAPI app
│   │   └── problem_details.py
│   ├── alembic/                # Database migrations
│   │   ├── migrations/
│   │   │   └── versions/       # Migration files
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── alembic.ini
│   ├── tests/                  # Backend tests
│   │   ├── routers/            # API route tests
│   │   │   ├── test_auth.py
│   │   │   ├── test_badges.py
│   │   │   ├── test_habits.py
│   │   │   ├── test_logs.py
│   │   │   └── test_stats.py
│   │   ├── conftest.py
│   │   └── test_models.py
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── uv.lock
│   ├── seed.py                 # Demo data seeding
│   ├── seed_badges.py          # Badge seeding
│   ├── Dockerfile
│   └── Makefile
├── .github/
│   └── workflows/              # GitHub Actions CI/CD
│       ├── backend_ci.yml
│       └── client_ci.yml
├── docker-compose.yml          # Development services
├── LICENSE
└── README.md
```

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user
- `POST /auth/register` - User registration (if implemented)

### Habits
- `GET /habits` - Get user's habits
- `POST /habits` - Create new habit
- `GET /habits/{id}` - Get habit details
- `PUT /habits/{id}` - Update habit
- `DELETE /habits/{id}` - Delete habit

### Habit Logs
- `POST /habits/{id}/log` - Log habit completion
- `GET /habits/{id}/logs` - Get habit logs
- `GET /habits/logs/today` - Get today's logs

### Statistics
- `GET /stats/overview` - Get overview statistics
- `GET /stats/{habit_id}/streak` - Get habit streak data
- `GET /stats/{habit_id}/daily-progress` - Get daily progress data

## Development

### Running Tests
```bash
# Backend tests
cd backend
uv run pytest

# Frontend tests
cd client
npm test

# All tests
docker compose exec backend uv run pytest
```

### Linting and Formatting
```bash
# Backend linting and formatting
cd backend
uv run ruff check .
uv run black .

# Frontend linting
cd client
npm run lint
```

### Database Management
```bash
# Create migration
cd backend
uv run alembic revision --autogenerate -m "description"

# Apply migrations
uv run alembic upgrade head

# Reset database
uv run alembic downgrade base
uv run alembic upgrade head

# Seed database
uv run python seed.py
```

## Docker Deployment

### Build and run with Docker Compose
```bash
# Build all services
docker compose build

# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

### Individual Docker builds
```bash
# Backend
cd backend
docker build -t fitness-tracker-backend .

# Frontend
cd client
docker build -t fitness-tracker-frontend .
```

## Environment Variables

### Backend (.env)
```env
ENV=dev
PORT=8000
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/fitness
JWT_SECRET=your-super-secret-jwt-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=60
REDIS_URL=redis://redis:6379/0

# Google OAuth (optional)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=http://localhost:4321/auth/google/callback
```

### Frontend (.env)
```env
PUBLIC_API_URL=http://localhost:8000
PUBLIC_GOOGLE_CLIENT_ID=your_google_client_id
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with modern web technologies
- Inspired by popular habit tracking apps
- Designed for simplicity and ease of use
- Focus on building sustainable fitness habits