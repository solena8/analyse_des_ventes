from models import Base

def setup_database(engine):
    try:
        Base.metadata.create_all(engine)
        print("Tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {str(e)}")
        raise