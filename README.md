# API-for-social-networking-application
API for social networking application using Django Rest Framework with below functionalities.


# Django Social Network

A simple social networking application using Django and Docker.

## Setup

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/your-username/django-social-network.git
    cd django-social-network
    ```

2. Build and start the Docker containers:

    ```sh
    docker-compose up --build
    ```

3. Run database migrations:

    ```sh
    docker-compose exec web python manage.py migrate
    ```

4. Create a superuser:

    ```sh
    docker-compose exec web python manage.py createsuperuser
    ```

5. Access the application:

    Open your browser and go to `http://localhost:8000`.

## Usage

- Use the admin panel at `http://localhost:8000/admin` to manage users.
- Use the API endpoints as described in the Postman collection provided.

## Contributing

Feel free to submit pull requests and issues. Any contributions are welcome!
