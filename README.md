# Sales Analysis System

This project implements a sales analysis system for a small to medium-sized business. It processes sales data to provide insights into product performance, store efficiency, and sales trends.

## Architecture

The system is built using a two-service architecture:

### Script Execution Service (Python)
This service is responsible for:
- Importing data from CSV files
- Processing and analyzing sales data
- Storing analysis results in the database

The service is built from a custom Docker image using Python 3.12 on a slim Debian base. It contains modules for:
- Database setup and connection management
- Data import from CSV files
- Data analysis and reporting

![architecture.svg](docs/architecture.svg)

### Database Service (SQLite)
This service provides:
- Persistent storage for sales data
- Storage for analysis results
- Data retrieval capabilities

The service uses the `keinos/sqlite3:latest` image, which is an Alpine-based implementation of SQLite3 with support for both AMD and ARM architectures.

## Database Schema

The database consists of the following tables:
- **Products**: Stores product information
- **Stores**: Contains store details and location data
- **Sales**: Records all sales transactions
- **Analysis tables**: Multiple tables for storing analysis results

Each analysis table is designed for a specific type of analysis:
- **product_sales_by_store**: Tracks product sales performance by store
- **monthly_product_sales**: Monitors product sales trends by month
- **employee_sales_ratio**: Analyzes the relationship between employee count and sales

![sale_analysis_db_schema.png](docs/sale_analysis_db_schema.png)

## Setup and Installation

### Prerequisites
- Docker and Docker Compose
- Access to product, store, and sales data files

### Running the System
1. Clone this repository
2. Place your CSV data files in the `data/` directory
3. Build and start the services:
   ```bash
   docker-compose up --build
   docker-compose up --build -d (to detach)

   ```

## Data Analysis Results

### Visualizations

*[TODO: Add visualizations and their explanations here]*

## Development

### Project Structure
```
project/
├── data/                     # Data files
├── scripts/                  # Python scripts
│   ├── database.py           # Database setup
│   ├── data_import.py        # Data import functions
│   └── data_analysis.py      # Data analysis functions
├── models/                   # Database models
│   ├── base.py               # Base SQLAlchemy model
│   ├── products.py           # Products model
│   ├── stores.py             # Stores model
│   ├── sales.py              # Sales model
│   └── ...                   # Analysis models
├── main.py                   # Main entry point script
├── Dockerfile                # Docker image definition
├── docker-compose.yml        # Service configuration
└── requirements.txt          # Python dependencies
```

### Adding New Analyses
To add a new analysis:
1. Create a new model in the `models/` directory
2. Add the model to `models/__init__.py`
3. Implement the analysis logic in `scripts/data_analysis.py`
4. Update the main script to include the new analysis