# Django Backend Deployment Guide

This guide explains how to deploy the Django backend separately from the Vercel frontend.

## Deployment Options

### Option 1: Railway (Recommended)
1. Create a Railway account at https://railway.app
2. Connect your GitHub repository
3. Select the `backend` folder as the source
4. Add environment variables:
   - `SECRET_KEY`: Generate a secure Django secret key
   - `DEBUG`: Set to `False` for production
   - `ALLOWED_HOSTS`: Add your Railway domain
   - `CORS_ALLOWED_ORIGINS`: Add your Vercel frontend URL
5. Deploy

### Option 2: Heroku
1. Create a Heroku account
2. Install Heroku CLI
3. Create a new Heroku app
4. Add PostgreSQL addon
5. Update `settings.py` to use PostgreSQL
6. Deploy using Git

### Option 3: DigitalOcean App Platform
1. Create a DigitalOcean account
2. Create a new App
3. Connect your GitHub repository
4. Select the `backend` folder
5. Configure environment variables
6. Deploy

## Environment Variables

Set these environment variables in your deployment platform:

```bash
SECRET_KEY=your-secure-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
CORS_ALLOWED_ORIGINS=https://your-vercel-app.vercel.app
```

## Database Setup

For production, consider using:
- PostgreSQL (recommended)
- MySQL
- SQLite (for simple deployments)

## Frontend Configuration

After deploying the backend, update your Vercel environment variables:

1. Go to your Vercel project settings
2. Add environment variable:
   - `NEXT_PUBLIC_BACKEND_URL`: Your deployed backend URL (e.g., `https://your-app.railway.app`)

## CORS Configuration

Make sure your backend allows requests from your Vercel frontend domain:

```python
CORS_ALLOWED_ORIGINS = [
    "https://your-vercel-app.vercel.app",
    "http://localhost:3000",  # For local development
]
```

## Security Considerations

1. Use HTTPS in production
2. Set `DEBUG=False` in production
3. Use a strong `SECRET_KEY`
4. Configure proper CORS settings
5. Consider adding rate limiting
6. Use environment variables for sensitive data

## Testing the Deployment

1. Deploy the backend first
2. Test the API endpoints directly
3. Update frontend environment variables
4. Deploy the frontend to Vercel
5. Test the complete flow

## Troubleshooting

### Common Issues:
1. **CORS errors**: Check `CORS_ALLOWED_ORIGINS` configuration
2. **Database errors**: Ensure database is properly configured
3. **Environment variables**: Verify all required variables are set
4. **Static files**: Configure static file serving if needed

### Debug Mode:
For debugging, temporarily set `DEBUG=True` and check the logs in your deployment platform. 