#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import io
import os
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from datetime import datetime
from models import Products, Stores, Sales

BASE_PATH = os.environ.get('DATA_PATH')
PRODUCTS_PATH = f"{BASE_PATH}/données_brief_data_engineer_produits.csv"
STORES_PATH =  f"{BASE_PATH}/donnees_brief_data_engineer_magasins.csv"
SALES_PATH =  f"{BASE_PATH}/données_brief_data_engineer_ventes.csv"


def fetch_data(path):
    # reads and returns data from csv
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
    except IOError as e:
        print(f"Error reading file {path}: {str(e)}")
        raise


def import_products(session, csv_content):
    try:
        csv_reader = csv.reader(io.StringIO(csv_content), delimiter=',')
        headers = next(csv_reader)
        # checks if product already exists in db
        for row in csv_reader:
            nom, product_id, price, stock = row
            stmt = select(Products).where(Products.product_id == product_id)
            existing_product = session.execute(stmt).first()
            if not existing_product:
                product = Products(
                    product_id=product_id,
                    name=nom,
                    price=float(price),
                    stock=int(stock)
                )
                session.add(product)
        session.commit()
        print("Products imported successfully")

    except (SQLAlchemyError, csv.Error) as e:
        print(f"Error importing products: {str(e)}")
        session.rollback()
        raise


def import_stores(session, csv_content):
    try:
        csv_reader = csv.reader(io.StringIO(csv_content), delimiter=',')
        headers = next(csv_reader)
        for row in csv_reader:
            store_id, city, employee_nb = row
            stmt = select(Stores).where(Stores.store_id == int(store_id))
            existing_store = session.execute(stmt).first()
            if not existing_store:
                store = Stores(
                    store_id=int(store_id),
                    city=city,
                    employee_nb=int(employee_nb)
                )
                session.add(store)
        session.commit()
        print("Stores imported successfully")

    except (SQLAlchemyError, csv.Error) as e:
        print(f"Error importing stores: {str(e)}")
        session.rollback()
        raise


def import_sales(session, csv_content):
    try:

        csv_reader = csv.reader(io.StringIO(csv_content), delimiter=',')
        headers = next(csv_reader)
        for row in csv_reader:
            date_str, product_id, quantity, store_id = row

            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            # converts str date into Date format

            stmt = select(Sales).where(
                (Sales.date == date_obj) &
                (Sales.product_id == product_id) &
                (Sales.store_id == int(store_id)) &
                (Sales.quantity == int(quantity))
            )
            existing_sale = session.execute(stmt).first()
            if not existing_sale:
                sale = Sales(
                    date=date_obj,
                    product_id=product_id,
                    store_id=int(store_id),
                    quantity=int(quantity)
                )
                session.add(sale)
        session.commit()
        print("Sales imported successfully")

    except (SQLAlchemyError, csv.Error) as e:
        print(f"Error importing sales: {str(e)}")
        session.rollback()
        raise


def import_data(session):
    """Main function that orchestrates the import of all data"""
    try:
        print("Starting data import")

        print(f"Importing products from {PRODUCTS_PATH}")
        produits_data = fetch_data(PRODUCTS_PATH)
        import_products(session, produits_data)

        print(f"Importing stores from {STORES_PATH}")
        magasins_data = fetch_data(STORES_PATH)
        import_stores(session, magasins_data)

        print(f"Importing sales from {SALES_PATH}")
        ventes_data = fetch_data(SALES_PATH)
        import_sales(session, ventes_data)

        print("Data import completed successfully")

    except Exception as e:
        print(f"Error during data import: {str(e)}")
        raise