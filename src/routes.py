from fastapi import Query, Response
from .models import Photo
from .proxy import ProxyPage
from datetime import datetime


def set_routes(app):

    @app.get('/photos', response_model=list[Photo])
    async def photos(resp: Response,
                     limit: int = Query(0, ge=0),
                     offset: int = Query(0, ge=0)):

        proxy_page = ProxyPage()

        start = datetime.now()
        result = await proxy_page.get_photos(limit, offset)
        resp.headers["X-Time-Query"] = str(datetime.now() - start)

        total = await proxy_page.get_headers('X-Total')
        if total:
            resp.headers["X-Total"] = total

        resp.headers["X-Total-Cache"] = str(await proxy_page.get_total_cache())

        return result
