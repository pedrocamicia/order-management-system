# Order Management System

This project is a backend Order Management System built using Domain-Driven Design principles.

It allows clients to:

Create orders

Add and modify products in a cart

Confirm orders

Manage stock consistently

The system includes a fully functional REST API, persistence using PostgreSQL, and unit/integration tests.

## Architecture

The project follows a layered architecture:

Domain Layer
Contains business logic, entities, aggregates, and validation rules.

Service Layer
Orchestrates use cases and coordinates domain and repositories.

Infrastructure Layer
Handles persistence with PostgreSQL repositories.

API Layer (FastAPI)
Exposes REST endpoints and maps domain objects to DTOs.

This separation ensures clean boundaries between business logic and infrastructure concerns.

## Core Domain Concepts

### Aggregates

**Pedido (Order)**– Aggregate Root
Manages order state, items, and business validations.

**Producto (Product)** – Independent Aggregate
Manages availability and stock.

**Cliente (Client)** – Independent Aggregate

### Order States:

Carrito (Cart)

Confirmado (Confirmed)

Orders can only be modified while in Carrito state.

## Features

### Orders

Create order

Modify product quantity in order

Remove product from order

Confirm order (with stock validation and deduction)

Retrieve order details

### Products

Create product

Retrieve signle product

List products with pagination and dynamic filters

### Clients

Create client

Retrieve client

List products with pagination and dynamic filters

## Business Rules

An order cant be confirmed if empty.

An order cant be modified if is confirmed.

Stock and product state is validated before confirmation or modification.

Stock is deducted only upon confirmation.

Product quantity cannot be negative.

If quantity becomes zero, the item is removed from the order.

## API Endpoints

### Clients

POST /clientes

GET /clientes/{id}

GET /clientes

- Pagination (limit/page)
 
- Dynamic filters (nombre) 

### Products

POST /productos

GET /productos/{id}

GET /productos

- Pagination (limit/page)

- Dynamic filters (estado, min_price, max_price) 


### Orders

POST /pedidos

GET /pedidos/{id}

PATCH /pedidos/{pedido_id}/items

PATCH /pedidos/{pedido_id}/confirmar

## Technologies Used

Python

FastAPI

PostgreSQL

psycopg2

Pytest

## How to Run

Configure environment variables for database connection, in file ".env.example".

Run the application:

uvicorn main:app --reload

Access API docs at:

http://localhost:8000/docs

## Tests

### Run tests using:

'pytest'

The project includes:

Unit tests for domain logic

Integration tests for services and persistence