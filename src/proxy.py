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

    @classmethod
    async def get_photos(cls, limit, offset):

        per = int(cls.per)
        page_numbers = await get_page_numbers(limit, offset, per)
        await cls.get_pages(page_numbers)
        return await cls.get_items(limit, offset, per, page_numbers)

    @classmethod
    async def get_items(cls, limit, offset, per, page_numbers):

        items = []
        a = page_numbers[0]
        count = 0

        for i in page_numbers:
            page = cls.pages.get(i)
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

    @classmethod
    async def get_pages(cls, page_numbers: list):
        await asyncio.gather(
            *[cls.load_page(i) for i in page_numbers]
        )

    @classmethod
    async def load_page(cls, n):
        if cls.ttl \
                and n in cls.pages \
                and (datetime.now() - cls.pages[n][0]).seconds < cls.ttl:
            return cls.pages[n][1]

        params = {
            'order_by': 'popular',
            'page': n,
            'client_id': cls.token
        }

        data = await cls.query_url(params)
        if type(data) != list: return

        page = []
        for item in data:
            photo = {
                'id': item['id'],
                'description': item['description'] or '',
                'image': item['urls']['regular']
            }
            page.append(Photo(**photo))

        cls.pages.update({n: (datetime.now(), page)})

    @classmethod
    async def query_url(cls, params):
        if cls.debug:
            n = params['page']
            return [{'id': f'test_id_{n}_{i + 1}', 'description': 'test_desc', 'urls': {'regular': 'test_url'}} for i in
                    range(cls.per)]
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                async with session.get(cls.url, params=params) as resp:
                    data = await resp.json()
                    await cls.set_headers(resp.headers)
            return data
        except Exception as e:
            print('query_url:', e)

    @classmethod
    async def set_headers(cls, resp_header):
        cls.headers = dict(resp_header)
        cls.per = await cls.get_headers('X-Per-Page', cls.per)

    @classmethod
    async def get_headers(cls, key, default=''):
        return cls.headers.get(key, default)

    @classmethod
    async def get_total_cache(cls):
        return sum([len(cls.pages[i][1]) for i in cls.pages])


async def get_page_numbers(limit, offset, per):
    a = offset // per
    b = (offset + limit) // per
    b += (offset + limit) % per > 0
    return [i + 1 for i in range(a, b)]