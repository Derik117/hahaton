import aiohttp
import asyncio
import pandas as pd
from bs4 import BeautifulSoup
from hahaton.utils import activate_django_env
activate_django_env()
from data.models.quote import Quote
from data.models.catalog import Catalog


class Parser:
    def __init__(self):
        self.df = pd.DataFrame(columns=['book', 'text', 'cover', 'author', 'rating'])

    async def parse(self, i):
        print(f"{i} started")
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f'https://bookmix.ru/quotes/index.phtml?all=yes&begin={i}&num_point=200&num_points=200') as response:
                html = await response.text()
                soup = BeautifulSoup(html, features="html.parser")
                for card in soup.find_all('div', 'col-12'):
                    text = card.find('i')
                    if not text:
                        continue
                    text = text.text
                    book_desc = card.find('p', 'universal-blocks-description')
                    if not book_desc:
                        continue
                    book_desc = book_desc.find_all('a')
                    book = book_desc[0].text
                    pic = card.find('img')['src']
                    author = book_desc[1].text if len(book_desc) == 2 else None
                    rating = card.find('ul', 'universal-blocks-action').text.strip()
                    self.df = self.df.append({
                        'book': book,
                        'text': text,
                        'cover': pic,
                        'author': author,
                        'rating': rating
                    }, ignore_index=True)
            print(len(self.df))

    async def start(self):
        i = 0
        tasks = []
        while i < 131870:#131870:
            tasks.append(asyncio.ensure_future(self.parse(i)))
            i += 200
        print('starting')
        await asyncio.wait(tasks)


print('load books cache')
books = {b['title']: b['id'] for b in list(Catalog.objects.all().values('id', 'title'))}
print('starting pars')
pars = Parser()
async_loop = asyncio.get_event_loop()
async_loop.run_until_complete(pars.start())
pars.df['book_id'] = pars.df['book'].apply(lambda x: books.get(x))
quotes_objects = []
pars.df = pars.df.dropna()
for quote in pars.df.to_dict(orient='records'):
    quotes_objects.append(Quote(book_id=quote['book_id'], text=quote['text'], rating=quote['rating']))
Quote.objects.bulk_create(quotes_objects)

pars.df = pars.df.dropna()[['book_id', 'cover']].drop_duplicates()
books_objects = []
for num, book in enumerate(pars.df.to_dict(orient='records')):
    print(f"{num+1} / {len(pars.df)}")
    book_id = int(book['book_id'])
    catalog = Catalog.objects.get(id=book_id)
    catalog.cover_url = book['cover']
    books_objects.append(catalog)

Catalog.objects.bulk_update(books_objects, fields=['cover_url'])
