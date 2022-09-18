from models import Photo
import os
from datetime import datetime

class ProxyUnsplash:

    __cash = {} # index: (date_load, Photo)
    __ttl = int(os.getenv('TTL_CASH')) * 60 # seconds
    __url = os.getenv('URL_API') # template with page number (paginator) API
    __per = int(os.getenv('PER_PAGE'))# count photos per page
    
    def __init__(self, limit, offset):
        self.__limit = limit
        self.__offset = offset
        
    async def get_photos(self): 
        return [i async for i in self]

    def __aiter__(self):
        self.__count = -1
        return self

    async def __anext__(self):
        self.__count += 1
        if self.__count < self.__limit:
            return await self.get_photo(self.__offset + self.__count)
        else:
            raise StopAsyncIteration
            
    async def get_photo(self, index):

        if index not in self.__cash:
            await self.call_api(index)
        
        if index not in self.__cash: 
            raise StopAsyncIteration
            
        if (datetime.now() - self.__cash[index][0]).seconds >= self.__ttl:
            await self.call_api(index)    
        
            
        return self.__cash[index][1]
        
    
    async def call_api(self, index):
        # which page index
        page = index // self.__per + 1
        url = self.__url % page
        
        # get json data from url
        data = await self.query_url(url)
        per = len(data)
        
        # set cash photos
        for i, item in enumerate(data):
            j = (page - 1)*per + i
            photo = {
                'id': item['id'],
                'description': item['description'],
                'image': item['urls']['regular']
            }
            self.__cash.update({j: (datetime.now(), Photo(**photo)) })

        
    async def query_url(self, url):
        data = [{'id': f'test_id_{i}', 'description': 'test_desc', 'urls': {'regular': 'test_url'}} for i in range(self.__per-1)]
        return data
    