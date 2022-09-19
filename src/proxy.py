from models import Photo
import os
from datetime import datetime
import aiohttp

class ProxyUnsplash:

    _cash = {} # index: (date_load, Photo)
    _ttl = int(os.getenv('TTL_CASH')) * 60 # seconds
    _url = os.getenv('URL_API') # template with page number (paginator) API
    _per = int(os.getenv('PER_PAGE'))# count photos per page
    _token = os.getenv('TOKEN_API')
    
    
    
    def __init__(self, limit, offset):
        self._limit = limit
        self._offset = offset
        self._headers = {}
        
        
        
    async def get_photos(self): 
        return [i async for i in self]



    def __aiter__(self):
        self.__count = -1
        return self



    async def __anext__(self):
        self.__count += 1
        if self.__count < self._limit:
            return await self.get_photo(self._offset + self.__count)
        else:
            raise StopAsyncIteration
         

         
    async def get_photo(self, index):

        if index not in self._cash:
            await self.call_api(index)
        
        if index not in self._cash: 
            raise StopAsyncIteration
            
        if (datetime.now() - self._cash[index][0]).seconds >= self._ttl:
            await self.call_api(index)    
        
            
        return self._cash[index][1]
        
    
    
    async def call_api(self, index):
        # which page index
        page = index // self._per + 1
        params = {
            'order_by': 'popular',
            'page': page,
            'client_id': self._token
        }
        
        # get json data from url
        data = await self.query_url(params)
        if type(data) != list:
            print('API unsplash return', data)
            raise StopAsyncIteration
            
        per = len(data)
        
        # set cash photos
        try:
            for i, item in enumerate(data):
                j = (page - 1)*per + i
                photo = {
                    'id': item['id'],
                    'description': item['description'] or '',
                    'image': item['urls']['regular']
                }
                self._cash.update({j: (datetime.now(), Photo(**photo)) })
        except Exception as e:
            print('call_api', e)
         

         
    async def query_url(self, params):
        #data = [{'id': f'test_id_{i}', 'description': 'test_desc', 'urls': {'regular': 'test_url'}} for i in range(self._per-1)]
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                async with session.get(self._url, params=params) as resp:
                    data = await resp.json()
                    self._headers = dict(resp.headers)
                    self._per = int(self.headers('X-Per-Page', self._per))
            return data
        except Exception as e:
            print('query_url:', e)



    def headers(self, key, default=''):
        return self._headers.get(key, default)