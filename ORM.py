import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json
from HW_6 import create_tables, Publisher, Book, Stock, Shop, Sale

DSN = "postgresql://postgres:13245342@localhost:5432/postgres"

engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind = engine)
session = Session()

with open("D:\Python\SQL\HomeWorks_6\Tests_data.json", 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()


publisher_name = input('Введите имя издателя: ')
print()
publisher = session.query(Publisher).filter_by(name=publisher_name).first()

facts = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)\
    .join(Publisher, Book.publisher)\
    .join(Stock, Book.stock)\
    .join(Shop, Stock.stock_shop)\
    .join(Sale, Stock.stock_sale)\
    .filter(Publisher.name == publisher_name)\
    .all()


for fact in facts:
    print(f"{fact[0]} | {fact[1]} | {fact[2]} | {fact[3]}")
print()
print(fact)
session.close()