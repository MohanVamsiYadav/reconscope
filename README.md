# ReconScope v2

This version fixes common causes of empty results:
- Accepts domain, IP, http:// and https:// input.
- DNS module returns per-record errors instead of silently hiding failures.
- HTTP module tries HTTPS and then HTTP.
- RDAP supports both domain and IP objects.
- Dashboard checks backend health before scanning.
- Backend exposes `/api/health`.

## Start backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

## Start frontend

Open another Terminal:

```bash
cd frontend
python3 -m http.server 8000
```

Open:

http://127.0.0.1:8000

## Test the API directly

```bash
curl http://127.0.0.1:5000/api/health
```

Then:

```bash
curl -X POST http://127.0.0.1:5000/api/recon \
  -H "Content-Type: application/json" \
  -d '{"target":"example.com"}'
```

The application is intended for authorized educational reconnaissance.
