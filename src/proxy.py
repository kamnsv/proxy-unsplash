from .models import Photo, Settings
from datetime import datetime
import aiohttp
import asyncio


class ProxyPage:
    cfg = Settings()
    pages = {}  # index_page: (datetime, page)
    headers = {}  # header data from unsplash
    per = cfg.per  # per_page
    token = cfg.token
    ttl = int(cfg.ttl) * 60
    debug = cfg.debug
    url = cfg.url
    
    async def get_photos(self, limit, offset):

        per = self.per
        page_numbers = await get_page_numbers(limit, offset, per)
        await self.get_pages(page_numbers)
        return await self.get_items(limit, offset, per, page_numbers)

    async def get_items(self, limit, offset, per, page_numbers):

        items = []
        a = page_numbers[0]
        count = 0
        
        for i in page_numbers:
            page = self.pages.get(i)
            if not page: continue
            for j, item in enumerate(page[1]):
                
                # first page
                if (a == i and offset % per > j): 
                        continue
                        
                items.append(item)
                
                count += 1
                if count == limit:
                    break
                    
        return items

    async def get_pages(self, page_numbers: list):
        await asyncio.gather(
            *[self.load_page(i) for i in page_numbers]
        )

    async def load_page(self, n):
        if self.ttl \
                and n in self.pages \
                and (datetime.now() - self.pages[n][0]).seconds < self.ttl:
            return self.pages[n][1]

        params = {
            'order_by': 'popular',
            'page': n,
            'client_id': self.token
        }

        data = await self.query_url(params)
        if type(data) != list: return

        page = []
        for item in data:
            photo = {
                'id': item['id'],
                'description': item['description'] or '',
                'image': item['urls']['regular']
            }
            page.append(Photo(**photo))

        self.pages.update({n: (datetime.now(), page)})

    async def query_url(self, params):
        if self.debug:
            n = params['page']
            return [{'id': f'test_id_{n}_{i+1}', 'description': 'test_desc', 'urls': {'regular': 'test_url'}} for i in
                    range(self.per)]
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                async with session.get(self.url, params=params) as resp:
                    data = await resp.json()
                    await self.set_headers(resp.headers)
            return data
        except Exception as e:
            print('query_url:', e)

    async def set_headers(self, resp_header):
        self.headers = dict(resp_header)
        self.per = await self.get_headers('X-Per-Page', self.per)

    async def get_headers(self, key, default=''):
        return self.headers.get(key, default)

    async def get_total_cache(self):
        return sum([len(self.pages[i][1]) for i in self.pages])

async def get_page_numbers(limit, offset, per):
    a = offset // per
    b = (offset + limit) // per
    b += (offset + limit) % per > 0
    return [i+1 for i in range(a, b)]