import unittest
from src.proxy import get_page_numbers


class TestProxyPage(unittest.IsolatedAsyncioTestCase):
        
    async def test_get_page_numbers(self):
        result = await get_page_numbers(offset=0, limit=5, per=10)
        self.assertEqual([1], result)

        result = await get_page_numbers(offset=0, limit=50, per=10)
        self.assertEqual([1, 2, 3, 4, 5], result)

        result = await get_page_numbers(offset=10, limit=50, per=10)
        self.assertEqual([2, 3, 4, 5, 6], result)

        result = await get_page_numbers(offset=75, limit=50, per=10)
        self.assertEqual([8, 9, 10, 11, 12, 13], result)

        result = await get_page_numbers(offset=72, limit=48, per=10)
        self.assertEqual([8, 9, 10, 11, 12], result)


if __name__ == '__main__':
    unittest.main()