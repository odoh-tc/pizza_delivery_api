# Pizza Delivery API

## Table of Contents

- [Pizza Delivery API](#pizza-delivery-api)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Endpoints](#endpoints)
    - [Authentication](#authentication)
    - [Order Management](#order-management)
    - [User Management](#user-management)
    - [Staff Functionality](#staff-functionality)
  - [Technologies Used](#technologies-used)
  - [Getting Started](#getting-started)
    - [Local Development](#local-development)
  - [Environment Variables](#environment-variables)
  - [Contributing](#contributing)
  - [License](#license)

## Introduction

The Pizza Delivery API is a RESTful web service built with FastAPI and PostgreSQL, allowing users to place orders for pizza delivery and manage them through various endpoints. It includes user authentication, order management, and additional functionalities for staff.

## Features

- User authentication and authorization
- Order placement and management
- Staff functionality for order administration

## Endpoints

### Authentication

- **Signup**: Register a new user account.
- **Login**: Authenticate a user and generate an access token.
- **Token**: Use the access token for subsequent requests that require authentication.

### Order Management

- **Place Order**: Create a new order with details such as quantity and pizza size.
- **View Orders**: Retrieve all orders or view orders specific to the authenticated user.
- **Update Order**: Update the details or status of an existing order.
- **Delete Order**: Delete an existing order.

### User Management

- **Update User**: Modify user details such as username, email, first name, and last name.
- **Delete User**: Remove the user account from the system.

### Staff Functionality

- **View Orders**: Staff members can view all orders placed by users.
- **Update Order Status**: Staff members can update the status of orders (e.g., pending, processing, shipped).
- **Delete Order**: Staff members can delete orders.

## Technologies Used

This project is built with:

- **FastAPI**: For building the API.
- **PostgreSQL**: As the database.
- **Docker and Docker Compose**: For containerization and deployment.
- **Python 3.9+**: Programming language.
- Other dependencies from `requirements.txt`:
  - **aiofiles**
  - **bcrypt**
  - **Jinja2**
  - **SQLAlchemy**
  - **uvicorn**
  - (and more...)

## Getting Started

To set up the project, follow the instructions for local development or deploying with Docker.

### Local Development

To run the project locally, follow these steps:

1. Clone the repository and navigate to it:

   ```python
   git clone https://github.com/your-username/repo.git
   cd repo
   ```

2. Create a virtual environment and activate it:

   ```python
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:

   ```python
   pip install -r requirements.txt

   ```

4. Start the FastAPI server:

      ```python
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Deploying with Docker

To deploy the project with Docker, follow these steps:

1. Ensure Docker and Docker Compose are installed on your system.

2. Clone the repository:

    ```python
   git clone https://github.com/your-username/repo.git
   cd repo
   ```

3. Build and start the Docker containers in detached mode:

   ```python
   docker-compose up --build -d
   ```

## Environment Variables

The following environment variables are used in this project:

- **SECRET**: The secret key used for token generation and authentication.
- **POSTGRES_USER**: The username for PostgreSQL.
- **POSTGRES_PASSWORD**: The password for PostgreSQL.
- **POSTGRES_DB**: The name of the PostgreSQL database.
- **POSTGRES_HOST**: The host for PostgreSQL.

## Contributing

We welcome contributions to the project. If you'd like to contribute, please follow these guidelines:

1. Fork the repository and create your own branch for new changes.
2. Submit a pull request with a clear description of the changes.
3. Ensure your code follows our coding standards and passes all tests.
4. Review any feedback and make necessary changes before merging.

For more information, check the [CONTRIBUTING](CONTRIBUTING.md) file for detailed guidelines.

## License

This project is licensed under the **MIT License**. See the LICENSE file for more details.
