
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from saleappv2.eapp import db, app


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class Category(BaseModel):
    name = Column(String(50), nullable=False, unique=True)

    products = relationship(
        'Product',
        backref='category',
        lazy=True
    )


class Product(BaseModel):
    name = Column(String(50), nullable=False)
    description = Column(Text)
    price = Column(Float, default=0)
    image = Column(String(255))
    active = Column(String(100))
    category_id = Column(
        Integer,
        ForeignKey(Category.id),
        nullable=False
    )


if __name__ == '__main__':

    products = [
        {
            "name": "iPhone 7 Plus",
            "description": "Apple, 32GB, RAM: 3GB, iOS13",
            "price": 17000000,
            "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg",
            "category_id": 1
        },
        {
            "name": "iPad Pro 2020",
            "description": "Apple, 128GB, RAM: 6GB",
            "price": 37000000,
            "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729533/zuur9gzztcekmyfenkfr.jpg",
            "category_id": 2
        },
        {
            "name": "Galaxy Note 10 Plus",
            "description": "Samsung, 64GB, RAM: 6GB",
            "price": 24000000,
            "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg",
            "category_id": 3
        }
    ]

    with app.app_context():

        # Tạo bảng
        db.create_all()

        try:
            # Thêm danh mục nếu chưa có
            if Category.query.count() == 0:
                categories = [
                    Category(name='Mobile'),
                    Category(name='Tablet'),
                    Category(name='Desktop'),
                    Category(name='Laptop')
                ]

                db.session.add_all(categories)
                db.session.commit()

            # Thêm sản phẩm nếu chưa có
            if Product.query.count() == 0:

                for x in products:
                    p = Product(
                        name=x['name'],
                        description=x['description'],
                        price=x['price'],
                        image=x['image'],
                        category_id=x['category_id']
                    )

                    db.session.add(p)

                db.session.commit()

            print("Them du lieu thanh cong!")

        except Exception as e:
            db.session.rollback()
            print("Loi:", e)
