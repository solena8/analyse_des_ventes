from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from .base import Base


class Stores(Base):
    __tablename__ = 'stores'

    store_id = Column(Integer, primary_key=True)
    city = Column(String, nullable=False, name="Ville")
    employee_nb = Column(Integer, nullable=False, name="Nombre de salariés")

    sales = relationship("Sales", back_populates="stores")
    product_sales = relationship("ProductSalesByStore", back_populates="stores")
    employee_ratios = relationship("EmployeeSalesRatios", back_populates="stores")
