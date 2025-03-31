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

---

## Pipeline Design

### Overview
This ETL pipeline collects rental posts from Facebook every 20 minutes using a Playwright-based Python scraper. The pipeline extracts unprocessed posts from MongoDB, processes them using pandas, and loads structured results into a PostgreSQL table for future dashboarding.

The process is managed by Apache Airflow, which orchestrates three separate tasks: extract, transform, and load.

### Database Structure

**MongoDB (Database: `posts`)**
- `raw_posts`: Contains all scraped posts. Each document has a `processed` field (boolean) and other raw data.
- `posts_to_process_ids`: Temporary collection that stores a list of post `_id`s selected for processing in the current DAG run.
- `transformed_posts`: Temporary collection that stores the cleaned, structured output of the transform step.

**PostgreSQL**
- Table: `posts`
- Stores structured fields extracted from raw posts: `mongo_id`, `price`, `rooms`, `size`, `area`, etc.

### DAG Tasks

| Task           | Description                                                   | Input                            | Output                              | Notes |
|----------------|---------------------------------------------------------------|----------------------------------|--------------------------------------|-------|
| `run_extract`  | Selects unprocessed posts from `raw_posts` and saves their `_id`s to `posts_to_process_ids` | `raw_posts` (MongoDB)           | `posts_to_process_ids`              | Skips if a batch is already in progress |
| `run_transform`| Loads posts by `_id`, extracts structured fields using `pandas`, stores result in `transformed_posts` | `raw_posts`, `posts_to_process_ids` | `transformed_posts`               | Stateless; doesn't modify source data |
| `run_load`     | Inserts transformed posts into PostgreSQL and marks original posts as processed | `transformed_posts` (MongoDB)    | `posts` (PostgreSQL); updates to `raw_posts` | Cleans up temp collections on success |

### Failure Strategy
- The extract task checks if `posts_to_process_ids` is empty before running. If not, the DAG skips to prevent overlap.
- The transform step does not mutate any state and can be retried independently.
- Only if the load to PostgreSQL is successful, the original documents in `raw_posts` are marked `processed=true`.
- Temp collections `posts_to_process_ids` and `transformed_posts` are only cleared after a successful load.

### Design Choices & Rationale

**Why no XCom?**
- Avoids Airflow's limitations on XCom size.
- Enables larger data volumes and separation between tasks.

**Why save only post IDs during extract?**
- Avoids data duplication in MongoDB.
- Enables efficient lookup during transform.

**Why store transformed data before loading?**
- Allows clean separation of responsibilities.
- Makes debugging and partial reruns easier.

### Future Improvements
- Replace temp collections with status flags inside `raw_posts` for higher scalability.
- Add unit tests for transform logic.
- Store timestamps for ETL runs to support incremental reporting.
- Build dashboard (e.g., Streamlit) with filtering and aggregated stats.

---

_Last updated: 2025-03-31_
