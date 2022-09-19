from fastapi import Query, Response
from proxy import ProxyUnsplash
from models import Photo


def set_routes(app):

    @app.get('/photos', response_model=list[Photo])
    async def photos(resp: Response,
                     limit : int = Query(0, ge=0), 
                     offset : int = Query(0, ge=0)):
        
        proxy_unspalash = ProxyUnsplash(limit, offset)
        result = await proxy_unspalash.get_photos()
        resp.headers["X-Total"] = proxy_unspalash.headers('X-Total')
        return result




