#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import io
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from datetime import datetime
from analyse_des_ventes.models import Products, Stores, Sales

PRODUITS_PATH = "/app/analyse_des_ventes/data/données_brief_data_engineer_produits.csv"
MAGASINS_PATH = "/app/analyse_des_ventes/data/donnees_brief_data_engineer_magasins.csv"
VENTES_PATH = "/app/analyse_des_ventes/data/données_brief_data_engineer_ventes.csv"


def fetch_data(path):
    # reads and returns data from csv
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
    except IOError as e:
        print(f"Erreur lors de la lecture du fichier {path}: {str(e)}")
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
        print("Produits importés avec succès")

    except (SQLAlchemyError, csv.Error) as e:
        print(f"Erreur lors de l'import des produits : {str(e)}")
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
        print("Magasins importés avec succès")

    except (SQLAlchemyError, csv.Error) as e:
        print(f"Erreur lors de l'import des magasins : {str(e)}")
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
        print("Ventes importées avec succès")

    except (SQLAlchemyError, csv.Error) as e:
        print(f"Erreur lors de l'import des ventes : {str(e)}")
        session.rollback()
        raise


def import_data(session):
    """Fonction principale qui orchestre l'importation de toutes les données"""
    try:
        print("Début de l'import des données")

        print(f"Import des produits depuis {PRODUITS_PATH}")
        produits_data = fetch_data(PRODUITS_PATH)
        import_products(session, produits_data)

        print(f"Import des magasins depuis {MAGASINS_PATH}")
        magasins_data = fetch_data(MAGASINS_PATH)
        import_stores(session, magasins_data)

        print(f"Import des ventes depuis {VENTES_PATH}")
        ventes_data = fetch_data(VENTES_PATH)
        import_sales(session, ventes_data)

        print("Import des données terminé avec succès")

    except Exception as e:
        print(f"Erreur lors de l'import des données : {str(e)}")
        raise
