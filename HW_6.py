import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"
    id = sq.Column(sq.Integer, primary_key = True)
    name = sq.Column(sq.String(length=48), unique = True)

    book = relationship("Book", back_populates="publisher")

    def __str__(self):
        return f'Publisher {self.id}: {self.name}'

class Book(Base):
    __tablename__ = "book"
    id = sq.Column(sq.Integer, primary_key = True)
    title = sq.Column(sq.String(length=124), unique = True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable = False)

    publisher = relationship("Publisher", back_populates="book")
    stock = relationship("Stock", back_populates="stock_book")

    def __str__(self):
        return f'Book {self.id}: {self.title}'

class Stock(Base):
    __tablename__ = "stock" #акции
    id = sq.Column(sq.Integer, primary_key = True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable = False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable = False)
    count = sq.Column(sq.Integer, nullable = False)

    stock_book = relationship("Book", back_populates="stock")
    stock_sale = relationship("Sale", back_populates="sale")
    stock_shop = relationship("Shop", back_populates="shop_stock")

    def __str__(self):
        return f'Stock {self.id}: {self.count}'

class Shop(Base):
    __tablename__ = "shop"
    id = sq.Column(sq.Integer, primary_key = True)
    name = sq.Column(sq.String(length=48), unique = True)

    shop_stock = relationship("Stock", back_populates="stock_shop")

    def __str__(self):
        return f'Shop {self.id}: {self.name}'

class Sale(Base):
    __tablename__ = "sale"
    id = sq.Column(sq.Integer, primary_key = True)
    price = sq.Column(sq.Text, nullable = False)
    date_sale = sq.Column(sq.Text, nullable = False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable = False)
    count = sq.Column(sq.Integer, nullable = False)

    sale = relationship("Stock", back_populates="stock_sale")

    def __str__(self):
        return f'Sale {self.id}: {self.price}, {self.date_sale}, {self.count}'
    

def create_tables(engine):          # Функция для создания таблиц. принимает параметр engine - наш движок
    Base.metadata.drop_all(engine)          # удалить существующие таблицы из нашей БД!
    Base.metadata.create_all(engine)        # умный метод create_all создаст таблицы, если они уже есть, не будет ошибки.