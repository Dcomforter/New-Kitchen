# [Dcomforters' Kitchen](https://dcomforter.pythonanywhere.com)

![Dcomforters' Kitchen Logo](newapp/static/img/DK_logo.png)

Dcomforters' Kitchen is a dynamic web application built with Django, offering a platform for managing, exploring, and reserving a table at an African Restaurant serving a variety of delightful intercontinental menus. Whether you are a Full Stack, BackEnd or FrontEnd Developer, this project provides an opportunity to see how all these are put together to design this dynamic application.

## Features

- **Menu Management:** Create, edit, and delete your menus with ease.
- **User Management:** Create, edit, delete and add users to groups.
- **Menu Exploration:** Discover a variety of menus served by the restaurant.
- **Table Reservation:** Reserve a table for you and your family, and enjoy special offers.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Dcomforter/Dcomforters-Kitchen.git
    ```

2. Navigate to the project directory:

    ```bash
    cd 'Dcomforters Kitchen'/secondproject
    ```

3. Install dependencies in the following order.

    ```bash
    pip install django
    ```

     ```bash
    pip install django-countries
    ```

     ```bash
    pip install whitenoise
    ```

4. Apply database migrations:

    ```bash
    python manage.py makemigration
    ```

    ```bash
    python manage.py migrate
    ```

5. Start the development server:

    ```bash
    python manage.py runserver
    ```

6. Visit `http://127.0.0.1:8000/` in your browser to access Dcomforters' Kitchen.

## Admin Usage

- **Create Admin User:** Create an admin user at the console, 
    ```bash
    python manage.py createsupersuser
    ```
    visit the link below to log in to the admin page with the credentials created above.
    ```bash
    http://127.0.0.1:8000/admin
    ```
- **Add Users and Groups:** Create groups, add roles to groups, create users and add users to groups.
- **Create and Manage Reservations:** Create or manage existing resersations as an admin user.

## Technologies Used For Fronted and Backend

- **Django:** A high-level web framework for Python.
- **SQLite:** Lightweight and easy-to-use database for development.
- **Bootstrap:** Front-end framework for responsive and modern design.
- **Pipenv:** Dependency management tool for Python projects.
- **JavaScript:** For interactive and dynamic front-end functionality.
- **HTML:** For creating the structure and layout of web pages.
- **CSS:** For styling and visual design of the web interface.

## Technologies Used For Deployment to Production
- **Jenkins:** Used to create a CI/CD pipeline. The pipeline tested the application, built a Docker image, and deployed it to a Docker Registry. Automates the integration and deployment process.
- **Docker:** Packaged the application and its dependencies into a containerized image, making it portable and consistent across different environments.
- **Kubernetes:** Orchestrated and managed the deployment of the Dockerized application. Pulled the image from the Docker Registry and deployed it to production environments on AWS using Elastic Kubernetes Service (EKS) and on GCP using Google Kubernetes Engine (GKE).
- **Terraform:** Implemented Infrastructure as Code (IaC) to provision production-ready Kubernetes clusters on AWS and GCP, ensuring an automated and consistent cloud environment setup.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
