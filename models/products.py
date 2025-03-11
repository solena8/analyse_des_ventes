from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.orm import relationship
from .base import Base


class Products(Base):
    __tablename__ = 'products'

    product_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)

    sales = relationship("Sales", back_populates="products")
    product_sales = relationship("ProductSalesByStore", back_populates="products")
    monthly_sales = relationship("MonthlyProductSales", back_populates="products")

