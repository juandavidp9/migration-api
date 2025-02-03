# DB Migration API

A FastAPI application for database migration, designed to upload historical data from CSV files into a PostgreSQL database. The application supports batch transactions, enabling efficient insertion of up to 1000 rows per request.

## Features

- **FastAPI** for building APIs
- **PostgreSQL** for database storage
- **Docker** for containerization
- **pgAdmin** for database management
- **Batch transactions** for efficient data insertion

## Prerequisites

Ensure you have the following installed:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/juandavidp9/migration-api.git
cd migration-api
```

### 2. Create a `.env` File

Create a `.env` file in the root directory and add the following content:

```bash
DATABASE_URL=postgresql://postgres:juan@db:5432/migration_db
```

### 3. Build and Run the Docker Containers

```bash
docker-compose up --build
```

This command builds and starts the Docker containers for:
- FastAPI application
- PostgreSQL database
- pgAdmin

### 4. Access the Application

- **FastAPI**: [http://localhost:8000](http://localhost:8000)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **pgAdmin**: [http://localhost:5050](http://localhost:5050)

### 5. Configure pgAdmin

1. Open pgAdmin at [http://localhost:5050](http://localhost:5050)
2. Log in with the following credentials:
   - **Email**: admin@gmail.com
   - **Password**: admin
3. Add a new server:
   - Right-click on "Servers" in the left-hand menu and select **Create** > **Server**
   - In the **General** tab:
     - **Name**: local
   - In the **Connection** tab:
     - **Host name/address**: db
     - **Port**: 5432
     - **Username**: postgres
     - **Password**: juan
   - Click **Save** to add the server.

## API Endpoints

### Upload Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/upload/employees` | POST | Upload employees from a CSV file |
| `/api/v1/upload/departments` | POST | Upload departments from a CSV file |
| `/api/v1/upload/jobs` | POST | Upload jobs from a CSV file |

**Request Format**: Multipart form-data with a CSV file.

### Reports Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/reports/hires-by-quarter` | GET | Get the number of hires by quarter for each department and job |
| `/api/v1/reports/departments-above-mean` | GET | Get departments with hire counts above the mean |

## Running Tests

To run tests, use the following command:

```bash
docker-compose run test
```

## License

This project is licensed under the **GPL-3.0 License**.

