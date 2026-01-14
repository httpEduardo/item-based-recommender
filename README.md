# RecoFoundry

RecoFoundry is a local recommender that uses item-item cosine similarity over implicit feedback.

## Quick start

```bash
python -m app.server --port 5173
```

Open http://localhost:5173

## API

- GET `/api/users`
- GET `/api/items`
- GET `/api/recommend?user_id=`
- POST `/api/seed`

