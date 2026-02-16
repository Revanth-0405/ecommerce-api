E-Commerce Inventory & Orders API


Project Overview

A production-style RESTful backend API that manages products, inventory, and orders for an e-commerce system.

This project demonstrates real backend engineering principles used in industry systems:
>Secure API key authentication
>Role-based access control
>Atomic multi-resource transactions
>Concurrency-safe inventory update
>Hybrid SQL + NoSQL architecture
>Request rate limiting
>Reporting analytics
>Automated testing
>Containerized deployment

This is designed to reflect real backend system architecture, not a tutorial project.
--------------------------------------------------------------------------------------------------------------------------------------------------
System Architecture

The application follows a layered architecture pattern:

Client Request
      ↓
Routes Layer
      ↓
Service Layer
      ↓
Database Models
      ↓
Storage Layer

Why this design?

>clean separation of concerns
>scalable code structure
>testable business logic
>maintainable modules
--------------------------------------------------------------------------------------------------------------------------------------------------
Technology Stack

Layer	            Technology
Backend Framework	Flask
ORM	                SQLAlchemy
Database	        SQLite
NoSQL Storage	    JSON File
Authentication	    API Keys + SHA256
Testing	            Pytest
Documentation	    OpenAPI / Swagger
Containerization	Docker
--------------------------------------------------------------------------------------------------------------------------------------------------
Repository Structure
app/
 ├── middleware/      # Auth, logging, rate limiting
 ├── models/          # Database schema
 ├── routes/          # API endpoints
 ├── services/        # Business logic
 ├── utils/           # Error handlers
 ├── config.py
 └── db.py

storage/
 └── orders.json      # Order storage (NoSQL)

tests/                # Automated test suite

postman_collection.json
run.py                # Application entrypoint
requirements.txt
swagger.yaml
Dockerfile
--------------------------------------------------------------------------------------------------------------------------------------------------
Authentication System

Protected endpoints require:

X-API-Key: <your-api-key>

Keys are:
securely hashed
role-restricted
revocable
rate limited
--------------------------------------------------------------------------------------------------------------------------------------------------
Feature Set

Authentication
Generate API keys
Role permissions (Admin / Viewer)

Product Management
Create products
Update products
Soft delete
Stock adjustment
Full-text search support

Order Processing
Create orders
Atomic stock deduction
Transaction safety
Cancel order (stock restoration)
Status workflow enforcement
pending → confirmed → shipped
Invalid transitions are automatically rejected.
--------------------------------------------------------------------------------------------------------------------------------------------------
Reporting APIs
Low stock report
Sales summary
Top selling products
-------------------------------------------------------------------------
Security Features
SHA256 key hashing
Role authorization
Rate limiting
Input validation
Transaction integrity
Thread-safe operations
--------------------------------------------------------------------------------------------------------------------------------------------------
Local Setup

Clone repository
git clone https://github.com/YOUR_USERNAME/ecommerce-api.git
cd ecommerce-api

Create virtual environment
python -m venv venv

Activate:

venv\Scripts\activate

Install dependencies
pip install -r requirements.txt

Run server
python run.py

Server runs at:
http://localhost:5000
--------------------------------------------------------------------------------------------------------------------------------------------------
Automated Tests

Run:
python -m pytest


Includes:
authentication tests
product tests
order flow tests
report tests
rate limiting tests
✔ 20+ test cases
✔ business logic coverage
✔ API validation
--------------------------------------------------------------------------------------------------------------------------------------------------
Docker Deployment

Build image:
docker build -t ecommerce-api .

Run container:
docker run -p 5000:5000 ecommerce-api
--------------------------------------------------------------------------------------------------------------------------------------------------
API Documentation

OpenAPI specification is provided:
swagger.yaml

Import into:
Swagger UI
Postman
Insomnia
--------------------------------------------------------------------------------------------------------------------------------------------------
Standard Error Format

All errors return consistent JSON:

{
  "error": "Message",
  "code": "ERROR_CODE"
}
--------------------------------------------------------------------------------------------------------------------------------------------------
Engineering Highlights

This project demonstrates ability to design and implement:
Scalable backend architecture
Transaction-safe operations
Concurrent request handling
Layered service design
Secure authentication systems
Automated testing strategy
--------------------------------------------------------------------------------------------------------------------------------------------------
Possible Enhancements

Future production improvements could include:
PostgreSQL database
Redis caching
JWT authentication
Async task workers
Monitoring dashboards
CI/CD pipeline