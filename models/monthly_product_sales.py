from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class MonthlyProductSales(Base):
    __tablename__ = 'monthly_product_sales'

    analysis_id = Column(Integer,primary_key=True)
    analysis_date = Column(Date, nullable=False)
    product_id = Column(String, ForeignKey('products.product_id'), name="ID Référence produit", nullable=False)
    year_month = Column(String, nullable=False)
    quantity_sold = Column(Integer,nullable=False)
    total_amount = Column(Integer,nullable=False)

    products = relationship("Products", back_populates="monthly_sales")
