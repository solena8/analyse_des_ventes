from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from .base import Base


class Sales(Base):
    __tablename__ = 'sales'

    sale_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    quantity = Column(Integer, nullable=False)
    product_id = Column(String, ForeignKey('products.product_id'), nullable=False)
    store_id = Column(Integer, ForeignKey('stores.store_id'), nullable=False)

    products = relationship("Products", back_populates="sales")
    stores = relationship("Stores", back_populates="sales")

