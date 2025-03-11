from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class ProductSalesByStore(Base):
    __tablename__ = 'product_sales_by_store'

    analysis_id = Column(Integer,primary_key=True)
    analysis_date = Column(Date, nullable=False)
    product_id = Column(String, ForeignKey('products.product_id'), nullable=False)
    store_id = Column(Integer, ForeignKey('stores.store_id'), nullable=False)
    quantity_sold = Column(Integer,nullable=False)
    revenue = Column(Integer,nullable=False)

    products = relationship("Products", back_populates="product_sales")
    stores = relationship("Stores", back_populates="product_sales")
