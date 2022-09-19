# proxy-unsplash
Photos proxy api for unsplash.com


![](https://img.shields.io/badge/python-3.9.14-blue)


# Dependencies

* fastapi
* uvicorn
* aiohttp

# Environments

`.env`

- TTL_CASH=30 # in minutes
- URL_API=https://api.unsplash.com/photos
- PER_PAGE=10
- TOKEN_API=...

# Deployment

```
docker-compose up
```

# Diagram


![](https://drive.google.com/file/d/1_nTmBD1moQS76QQes5gHepTZCGyg27jC/view?usp=sharing)