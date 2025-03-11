#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from scripts.data_analysis import run_analyses
from scripts.data_visualization import run_visualizations
from scripts.database import setup_database
from scripts.data_import import import_data


def main():
    try:
        # Setting up the database
        db_path = os.environ.get('DB_PATH')
        print(f"Using database: {db_path}")

        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        engine = create_engine(f'sqlite:///{db_path}')

        # Creating tables
        setup_database(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        import_data(session)

        run_analyses(session)

        run_visualizations()

        session.close()
        print("Processing completed successfully")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    print("Starting sales analysis script")
    main()