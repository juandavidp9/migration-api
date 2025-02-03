# DB Migration API

This is a FastAPI application designed for database migration. It provides endpoints for uploading historical data from CSV files into a PostgreSQL database. The application supports batch transactions, allowing the insertion of up to 1000 rows with a single request.

## Features

- FastAPI for building APIs
- PostgreSQL for database
- Docker for containerization
- pgAdmin for database management
- Batch transactions for efficient data insertion

## Prerequisites

- Docker
- Docker Compose

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/juandavidp9/migration-api.git
cd migration-api

2. Create a .env File
Create a .env file in the root directory with the following content:
```bash
DATABASE_URL=postgresql://postgres:juan@db:5432/migration_db

3. Build and Run the Docker Containers
```bash
docker-compose up --build

This command will build and start the Docker containers for the FastAPI application, PostgreSQL database, and pgAdmin.

4. Access the Application
FastAPI: Open your browser and navigate to http://localhost:8000
API Documentation: Navigate to http://localhost:8000/docs
pgAdmin: Open your browser and navigate to http://localhost:5050


5. Add Server in pgAdmin
Open pgAdmin at http://localhost:5050
Log in with the following credentials:
Email: admin@gmail.com
Password: admin
Right-click on "Servers" in the left-hand menu and select "Create" > "Server..."
In the "Create - Server" dialog, enter the following details:

General Tab:
Name: local
Connection Tab:
Host name/address: db
Port: 5432
Username: postgres
Password: juan
Click "Save" to add the server.

Files por testing the endpoints are availble under the folder Files. 
To test the FstAPI endpoints go to:
http://localhost:8000/docs

Endpoints
Upload Employees
URL: /api/v1/upload/employees
Method: POST
Description: Endpoint to upload employees from a CSV file.
Request:
File: CSV file containing employee data.

Upload Departments
URL: /api/v1/upload/departments
Method: POST
Description: Endpoint to upload departments from a CSV file.
Request:
File: CSV file containing department data.

Upload Jobs
URL: /api/v1/upload/jobs
Method: POST
Description: Endpoint to upload jobs from a CSV file.
Request:
File: CSV file containing job data.

Get Hires by Quarter
URL: /api/v1/reports/hires-by-quarter
Method: GET
Description: Endpoint to get the number of hires by quarter for each department and job.

Get Departments Above Mean
URL: /api/v1/reports/departments-above-mean
Method: GET
Description: Endpoint to get departments with hire counts above the mean.

Running Tests
To run tests, use the following command:
```bash
docker-compose run test

License
This project is licensed under the MIT License.

