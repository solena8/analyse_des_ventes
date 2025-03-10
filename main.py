#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from scripts.database import setup_database
from scripts.data_import import import_data


def main():
    try:
        # Configuration de la base de données
        db_path = os.environ.get('DB_PATH', '/app/analyse_des_ventes/data/sale-analysis.db')
        print(f"Using database: {db_path}")

        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        engine = create_engine(f'sqlite:///{db_path}')

        # Création des tables
        setup_database(engine)

        # Création de la session
        Session = sessionmaker(bind=engine)
        session = Session()

        # Import des données
        import_data(session)

        # Fermeture de la session
        session.close()
        print("Processing completed successfully")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    print("Starting sales analysis script")
    main()