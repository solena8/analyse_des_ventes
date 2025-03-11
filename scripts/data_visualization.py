#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.products import Products
from models.stores import Stores
from models.product_sales_by_store import ProductSalesByStore
from models.monthly_product_sales import MonthlyProductSales
from models.employee_sales_ratios import EmployeeSalesRatios

DATAVIZ_PATH = os.environ.get('DATAVIZ_PATH')


def connect_to_db():
    db_path = os.environ.get('DB_PATH')
    engine = create_engine(f'sqlite:///{db_path}')
    Session = sessionmaker(bind=engine)
    return Session()


def generate_employee_sales_correlation(session, output_dir=f"{DATAVIZ_PATH}"):
    try:
        query = (
            session.query(
                Stores.city,
                EmployeeSalesRatios.employee_count,
                EmployeeSalesRatios.total_sales
            )
            .join(Stores, EmployeeSalesRatios.store_id == Stores.store_id)
            .order_by(Stores.city)
        )

        results = query.all()
        df = pd.DataFrame([(r.city, r.employee_count, r.total_sales) for r in results],
                          columns=['city', 'employee_count', 'total_sales'])

        # Create points
        plt.figure(figsize=(12, 8))
        plt.scatter(df['employee_count'], df['total_sales'], alpha=0.7, s=100)

        # Add labels to each point
        for i, txt in enumerate(df['city']):
            plt.annotate(txt, (df['employee_count'].iloc[i], df['total_sales'].iloc[i]),
                         xytext=(7, 3), textcoords='offset points')

        plt.xlabel('Number of Employees', fontsize=12)
        plt.ylabel('Total Sales', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Save chart
        filename = f"{output_dir}/employee_sales_correlation_dataviz.png"
        plt.savefig(filename, dpi=300)
        plt.close()

        print(f"Employee-sales correlation chart saved: {filename}")

    except Exception as e:
        print(f"Error generating employee-sales correlation chart: {str(e)}")
        raise


def generate_product_sales_by_store(session, output_dir=f"{DATAVIZ_PATH}"):
    try:
        query = (
            session.query(
                Products.name.label('product_name'),
                Stores.city.label('store_name'),
                ProductSalesByStore.quantity_sold
            )
            .join(Products, ProductSalesByStore.product_id == Products.product_id)
            .join(Stores, ProductSalesByStore.store_id == Stores.store_id)
            .order_by(Products.name, Stores.city)
        )

        results = query.all()
        df = pd.DataFrame([(r.product_name, r.store_name, r.quantity_sold) for r in results],
                          columns=['product_name', 'store_name', 'quantity_sold'])

        # Create a pivot table (product is the line name and store the column name and inside are the values)
        pivot_df = df.pivot(index='product_name', columns='store_name', values='quantity_sold')
        pivot_df = pivot_df.fillna(0)  # Replace NaN with 0 if some products are not sold in some cities

        total_sales_by_product = df.groupby('product_name')['quantity_sold'].sum()
        pivot_df = pivot_df.loc[total_sales_by_product]

        # Create bar chart
        pivot_df.plot(kind='bar', stacked=True, figsize=(14, 9))
        plt.title('Product Sales by Store', fontsize=16)
        plt.xlabel('Product', fontsize=12)
        plt.ylabel('Units Sold', fontsize=12)
        plt.legend(title='Store', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Save chart
        filename = f"{output_dir}/product_sales_by_store_dataviz.png"
        plt.savefig(filename, dpi=300)
        plt.close()

        print(f"Product sales by store chart saved: {filename}")

    except Exception as e:
        print(f"Error generating product sales by store chart: {str(e)}")
        raise


def generate_product_sales_by_month(session, output_dir=f"{DATAVIZ_PATH}"):
    try:
        query = (
            session.query(
                Products.name.label('product_name'),
                MonthlyProductSales.year_month,
                MonthlyProductSales.quantity_sold
            )
            .join(Products, MonthlyProductSales.product_id == Products.product_id)
            .order_by(Products.name, MonthlyProductSales.year_month)
        )

        results = query.all()
        df = pd.DataFrame([(r.product_name, r.year_month, r.quantity_sold) for r in results],
                          columns=['product_name', 'month', 'quantity_sold'])


        total_sales_by_product = df.groupby('product_name')['quantity_sold'].sum()
        df = df[df['product_name'].isin(total_sales_by_product)]

        # Create line chart
        plt.figure(figsize=(14, 8))

        # Each product is a separate line
        for product, data in df.groupby('product_name'):
            plt.plot(data['month'], data['quantity_sold'], marker='o', linewidth=2, label=product)

        plt.title('Monthly Sales by Product', fontsize=16)
        plt.xlabel('Month', fontsize=12)
        plt.ylabel('Units Sold', fontsize=12)
        plt.legend(title='Product', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save chart
        filename = f"{output_dir}/product_sales_by_month_dataviz.png"
        plt.savefig(filename, dpi=300)
        plt.close()

        print(f"Product sales by month chart saved: {filename}")

    except Exception as e:
        print(f"Error generating product sales by month chart: {str(e)}")
        raise


def run_visualizations():
    try:
        print("Starting visualization generation...")
        session = connect_to_db()

        generate_employee_sales_correlation(session)
        generate_product_sales_by_store(session)
        generate_product_sales_by_month(session)

        session.close()
        print("All dataviz successfully generated")

    except Exception as e:
        print(f"Error during visualization generation: {str(e)}")
        raise


if __name__ == "__main__":
    run_visualizations()
