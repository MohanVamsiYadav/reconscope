# ReconScope - Deployable Version

This version serves the frontend and Flask API from the same Render web service.
That avoids the localhost API problem after deployment.

## Local test

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

Open:
http://127.0.0.1:5000

Health:
http://127.0.0.1:5000/api/health

## Render deployment

Push this project to GitHub.

In Render:
- New -> Web Service
- Connect the GitHub repository
- Root Directory: `backend`
- Runtime: Python 3
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
- Instance: Free (if available for your account)

Render provides an `onrender.com` URL and HTTPS for the deployed service.

Only use reconnaissance functions against systems you own or are explicitly authorized to assess.
