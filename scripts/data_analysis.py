#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import text

# using SQL here as requested in the brief (instead of the sql alchemy orm I set up)

def analyze_product_sales_by_store(session):
    try:
        current_date = datetime.now().date()

        session.execute(text("DELETE FROM product_sales_by_store"))
        session.commit()

        query = text("""
                   INSERT INTO product_sales_by_store (analysis_date, product_id, store_id, quantity_sold, revenue)
                   SELECT 
                       :analysis_date AS analysis_date,
                       s.product_id,
                       s.store_id,
                       SUM(s.quantity) AS quantity_sold,
                       SUM(s.quantity * p.price) AS revenue
                   FROM 
                       sales s
                       JOIN products p ON s.product_id = p.product_id
                   GROUP BY 
                       s.product_id, s.store_id
               """)

        session.execute(query, {"analysis_date": current_date})
        session.commit()

        print("Product sales by store analysis completed")

    except Exception as e:
        print(f"Error analyzing product sales by store: {str(e)}")
        session.rollback()
        raise


def analyze_monthly_product_sales(session):
    try:
        current_date = datetime.now().date()

        session.execute(text("DELETE FROM monthly_product_sales"))
        session.commit()

        query = text("""
                  INSERT INTO monthly_product_sales (analysis_date, product_id, year_month, quantity_sold, total_amount)
                  SELECT 
                      :analysis_date AS analysis_date,
                      s.product_id,
                      strftime('%Y-%m', s.date) AS year_month,
                      SUM(s.quantity) AS quantity_sold,
                      SUM(s.quantity * p.price) AS total_amount
                  FROM 
                      sales s
                      JOIN products p ON s.product_id = p.product_id
                  GROUP BY 
                      s.product_id, strftime('%Y-%m', s.date)
              """)

        session.execute(query, {"analysis_date": current_date})
        session.commit()

        print("Monthly product sales analysis completed")

    except Exception as e:
        print(f"Error analyzing monthly product sales: {str(e)}")
        session.rollback()
        raise


def analyze_employee_sales_ratio(session):
    try:
        current_date = datetime.now().date()

        session.execute(text("DELETE FROM employee_sales_ratio"))
        session.commit()

        query = text("""
                    INSERT INTO employee_sales_ratio (analysis_date, store_id, employee_count, total_sales, sales_per_employee)
                    SELECT 
                        :analysis_date AS analysis_date,
                        st.store_id,
                        st.employee_nb as employee_count,
                        SUM(sa.quantity) AS total_sales,
                        SUM(sa.quantity) / st.employee_nb AS sales_per_employee
                    FROM 
                        sales sa
                        JOIN stores st ON sa.store_id = st.store_id
                    GROUP BY 
                        st.store_id, st.employee_nb
                """)
        session.execute(query, {"analysis_date": current_date})
        session.commit()

    except Exception as e:
        print(f"Error analyzing employee sales ratio: {str(e)}")
        session.rollback()
        raise


def run_analyses(session):
    try:
        print("Starting sales analyses...")

        analyze_product_sales_by_store(session)

        analyze_monthly_product_sales(session)

        analyze_employee_sales_ratio(session)

        print("All analyses completed successfully")

    except Exception as e:
        print(f"Error during analyses: {str(e)}")
        raise
