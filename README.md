# proxy-unsplash
Photos proxy api for unsplash.com


![](https://img.shields.io/badge/python-3.9.14-blue)

# Speed test


```
/photos?limit=6&offset=0
x-time-query: 0:00:00.211996
/photos?limit=50&offset=75
x-time-query: 0:00:00.295535
```


# Dependencies

* fastapi
* uvicorn
* aiohttp

# Environments

`.env`

```
TTL_CASH=30 # in minutes
URL_API=https://api.unsplash.com/photos
PER_PAGE=10 # start per page
TOKEN_API=...
DEBUG=0 # if 1 then return fake data
```


# Deployment

```
docker-compose up
```