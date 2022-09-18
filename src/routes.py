from fastapi import Query, Response
from proxy import ProxyUnsplash
from models import Photo


def set_routes(app):

    @app.get('/photos', response_model=list[Photo])
    async def photos(resp: Response,
                     limit : int = Query(0, ge=0), 
                     offset : int = Query(0, ge=0)):
        
        result = await ProxyUnsplash(limit, offset).get_photos()
        resp.headers["X-total"] = str(len(result))
        return result




