# KidAI Backend

Django REST API backend for the KidAI application.

## Features

- User registration and authentication
- Parent and child management
- RESTful API endpoints
- CORS support for frontend integration

## API Endpoints

- `POST /api/register/` - Register a new parent and child
- `POST /api/login/` - Login with parent credentials
- `GET /admin/` - Django admin interface

## Local Development

1. Clone the repository
2. Navigate to the backend directory
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Copy `env.example` to `.env` and configure environment variables
6. Run migrations:
   ```bash
   python manage.py migrate
   ```
7. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```
8. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Environment Variables

Create a `.env` file with the following variables:

```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

## Deployment to Render

This backend is configured for deployment on Render.com.

### Automatic Deployment

1. Push this code to a GitHub repository
2. Connect your repository to Render
3. Render will automatically detect the `render.yaml` configuration
4. Set the following environment variables in Render:
   - `SECRET_KEY`: A secure Django secret key
   - `DEBUG`: Set to `False`
   - `ALLOWED_HOSTS`: Your Render domain
   - `CORS_ALLOWED_ORIGINS`: Your Vercel frontend URL
   - `DATABASE_URL`: Your database URL (optional, defaults to SQLite)

### Manual Deployment

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set the build command: `chmod +x build.sh && ./build.sh`
4. Set the start command: `gunicorn kidai_backend.wsgi:application --bind 0.0.0.0:$PORT`
5. Configure environment variables as listed above

## Database

The application uses SQLite by default for simplicity. For production, consider using PostgreSQL:

1. Add a PostgreSQL database service on Render
2. Set the `DATABASE_URL` environment variable to the PostgreSQL connection string
3. The application will automatically use PostgreSQL when `DATABASE_URL` is provided

## Frontend Integration

After deploying the backend, update your Vercel frontend environment variables:

1. Add `NEXT_PUBLIC_BACKEND_URL` with your Render backend URL
2. Update your frontend API calls to use the new backend URL

## Security

- Set `DEBUG=False` in production
- Use a strong `SECRET_KEY`
- Configure proper CORS settings
- Use HTTPS in production
- Consider adding rate limiting for production use

## Troubleshooting

- Check Render logs for deployment issues
- Verify environment variables are set correctly
- Ensure CORS settings allow your frontend domain
- Test API endpoints directly before frontend integration 