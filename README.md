# Item Based Recommender

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)

Item Based Recommender is a local recommender that uses item-item cosine similarity over implicit feedback.

## Quick start

```bash
python -m item_based_recommender.server --port 5173
```

Open http://localhost:5173

## API

- GET `/api/users`
- GET `/api/items`
- GET `/api/recommend?user_id=`
- POST `/api/seed`

