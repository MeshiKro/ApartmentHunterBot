![Architecture](https://raw.githubusercontent.com/Daniel1Maymon/ApartmentHunterBot/main/Scraper-project-Digram.png)


# Facebook Rental Listings – Data Pipeline

This project implements a full data pipeline that extracts Facebook rental listings, processes them into structured format, and stores the results for analysis and visualization.

## Features

- Automated scraping using Playwright (Python)
- Raw data stored in MongoDB
- ETL process managed by Apache Airflow
  - Extract: Load only unprocessed posts from MongoDB
  - Transform: Clean and structure the data using pandas
  - Load: Insert into PostgreSQL with conflict handling
- Dashboard (planned): Will display insights such as average prices per area

## Architecture

The pipeline consists of the following components:

1. **Scraper** – Python script that collects new posts every 20 minutes and stores them in MongoDB.
2. **MongoDB** – Stores raw unprocessed posts.
3. **Airflow DAG** – Manages ETL execution:
   - Extracts unprocessed posts
   - Processes them with pandas
   - Loads them into PostgreSQL
4. **PostgreSQL** – Stores structured and cleaned data.
5. **Dashboard (coming soon)** – Will be built on top of PostgreSQL for data exploration.

### Diagram

See the full architecture diagram here:

```markdown

