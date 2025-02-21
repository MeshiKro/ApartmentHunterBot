'''
MongoDB --> List of dicts --> SQL Model Objects --> PostgreSQL Table

Pseudocode (with ETL stages)
1. Connect to MongoDB and fetch data.       # Extract - Retrieve data from MongoDB and store it as a list of dictionaries.

2. Process the fetched data into SQL Model objects.  # Transform - Filter and convert each dictionary into an SQL Model object.

3. Connect to PostgreSQL and create a table. # Load - Connect to PostgreSQL and create a table based on the SQL Model.

4. Insert processed data into PostgreSQL.    # Load - Insert all SQL Model objects into the PostgreSQL table.

'''
from datetime import time
import logging, time, os, sys
from dotenv import load_dotenv
import pandas as pd
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from sqlalchemy.dialects.postgresql import insert

# Load the .env file
load_dotenv()

# Add the path to the project directory
sys.path.append(os.getcwd())

from utils.regex_extractor import extract_rental_info
from ETL.models.Post import Post


def extract_data(limit=20):
    """Extract data from MongoDB and return a list of dictionaries."""
    # Connect to MongoDB
    client = MongoClient(os.environ.get("MONGO_URL"))
    db = client["posts"]
    collection = db["collection"]

    # Fetch data (limit to 20 records by default)
    data = list(collection.find().limit(limit))
    # data = list(collection.find())
    return data


def transform_data(data: list) -> list:
    """Transform - Filter, extract values using Regex, and convert to SQLModel objects."""
    df = pd.DataFrame(data)  # Convert to DataFrame for easier processing

    # Use Regex functions to extract values from the 'content' field
    df[['price', 'rooms', 'size']] = df['content'].apply(lambda x: pd.Series(extract_rental_info(x)))

    # Filter only the columns relevant to the Post model
    df = df[['content', 'rooms', 'size', 'price']]

    # Convert each row into a SQLModel object
    """Transform - Filter, clean, and convert MongoDB documents into SQLModel objects."""
    processed_data = []

    for i, row in df.iterrows():
        row_data = row.to_dict()
        row_data["mongo_id"] = str(data[i]["_id"])  # <-- Store MongoDB _id in mongo_id field

        row_data["rooms"] = None if pd.isna(row_data.get("rooms")) else row_data.get("rooms")
        row_data["size"] = None if pd.isna(row_data.get("size")) else row_data.get("size")
        row_data["price"] = None if pd.isna(row_data.get("price")) else row_data.get("price")

        processed_data.append(Post(**row_data))

    return processed_data
    

def connect_to_postgres():
    """Connect to PostgreSQL using SQLAlchemy and return the engine."""
    # Get the connection string
    DATABASE_URL = os.getenv("POSTGRES_URL")
    
    engine = create_engine(DATABASE_URL)
    return engine


def insert_data(engine, data: list):
    """Load - Insert processed SQLModel objects into PostgreSQL using ON CONFLICT DO NOTHING."""
    create_table()  # Ensure the table exists

    with Session(engine) as session:
        # Prepare bulk insert using SQLAlchemy insert
        stmt = insert(data[0].__class__).values([obj.model_dump() for obj in data])  # Use the class of the first object
        stmt = stmt.on_conflict_do_nothing(index_elements=["mongo_id"])  # Avoid duplicate mongo_id

        # Execute the statement
        session.execute(stmt)
        session.commit()
        print(f"{len(data)} records inserted successfully!")

def create_table():
    """Create tables based on SQLModel definitions"""
    SQLModel.metadata.create_all(engine)
    print("Table created successfully!")



if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    start_time = time.time()  # Measure total execution time
    
    logging.info("ETL process started.")
    
    try:
        # raise RuntimeError("Simulated general error")
        
        # Extract - Connect to MongoDB and fetch data
        logging.info("Starting data extraction from MongoDB.")
        data = extract_data()
        logging.info(f"Extraction completed. Retrieved {len(data)} documents.")

        # Transform - Process the fetched data into SQL Model objects
        logging.info("Starting data transformation.")
        transformed_data = transform_data(data)
        logging.info(f"Transformation completed. Processed {len(transformed_data)} records.")

        # Load - Connect to PostgreSQL and insert data
        logging.info("Connecting to PostgreSQL.")
        engine = connect_to_postgres()
        
        logging.info("Starting data insertion into PostgreSQL.")
        insert_data(engine, transformed_data)
        logging.info("Data insertion completed successfully.")

    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")

    finally:
        logging.info(f"ETL process finished in {time.time() - start_time:.2f} seconds.")
    

    
    
    
    
    