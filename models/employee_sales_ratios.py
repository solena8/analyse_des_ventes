from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class EmployeeSalesRatios(Base):
    __tablename__ = 'employee_sales_ratio'

    analysis_id = Column(Integer,primary_key=True)
    analysis_date = Column(Date, nullable=False)
    store_id = Column(Integer, ForeignKey('stores.store_id'), name="ID Magasin", nullable=False)
    employee_count = Column(Integer,nullable=False)
    total_sales = Column(Integer,nullable=False)
    sales_per_employee = Column(Integer,nullable=False)

    stores = relationship("Stores", back_populates="employee_ratios")

