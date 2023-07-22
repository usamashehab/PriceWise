# PriceWise: A Price Comparison Website

Welcome to PriceWise, a powerful and user-friendly price comparison website developed by a team of skilled professionals. This project showcases the collaboration between talented backend engineers, web scrapers, and frontend developers, resulting in a dynamic and feature-rich platform.

## Installation

To experience the full potential of PriceWise, follow these installation steps:

1. Clone the repository:

```bash
$ git clone https://github.com/usamashehab/PriceWise.git
```

2. Change into the project directory:

```bash
$ cd PriceWise
```

3. Install the required dependencies:

```bash
$ pip install -r requirements.txt
```

4. Create a PostgreSQL database named `pricewise` and add the `pg_trgm` extension for full-text search support:

   - First, ensure that you have PostgreSQL installed and running on your system.
   - Open a terminal or command prompt and log in as the `postgres` user:

     **For Linux:**

     ```bash
     sudo -u postgres psql
     CREATE DATABASE pricewise;
     \c pricewise;
     CREATE EXTENSION pg_trgm;
     ```

     **For Windows:**

     ```bash
     psql -U postgres
     ```

     Enter your credentials and then:

     ```bash
     CREATE DATABASE pricewise;
     \c pricewise;
     CREATE EXTENSION pg_trgm;
     ```

5. Migrate the database:

```bash
$ python manage.py migrate
```

6. Start the development server:

```bash
$ python manage.py runserver
```

7. Open a web browser and navigate to `http://localhost:8000/redoc/` to access the comprehensive API documentation.

## Key Features

PriceWise offers a variety of cutting-edge features that enhance your shopping experience:

1. **Seamless Search Experience:** Our expert scraping team, led by Mohamed Mohsen and Ziad Ahmed, diligently gathered product data from various vendors, ensuring an extensive and up-to-date catalog.

2. **Advanced Filtering:** Working closely with our talented frontend team, led by Mohamed Samir and Ahmed Radwan, we implemented a dynamic filtering system that optimizes search results based on user-selected attributes, providing a personalized and efficient shopping experience.

3. **Real-time Price Comparison:** Leveraging our web scraping expertise, we retrieve real-time pricing data from multiple vendors, enabling users to make informed purchasing decisions with accurate and up-to-date information.

4. **User-Friendly APIs:** Collaborating with our backend and frontend teams, we utilized Django REST Framework (DRF) to create robust and secure APIs, ensuring seamless integration with other platforms and facilitating third-party integrations.

5. **Enhanced User Management:** Working closely with our scrapping and frontend teams, we implemented user authentication and authorization using Djoser and JWT tokens, allowing secure access to user-specific features such as saved favorites and personalized alerts.

6. **Price History Tracking:** In collaboration with our scrapping team, we developed a feature to track the price history of products, providing users with historical price trends and empowering them to make informed decisions based on past fluctuations.

7. **Price Drop Alerts:** Collaborating with our frontend team, we implemented a functionality that allows users to set price drop alerts for their favorite products. Users receive notifications when the price of a tracked product reaches their desired price threshold, ensuring they never miss out on great deals.

8. **Performance Optimization:** In collaboration with our backend and caching experts, we leveraged PostgreSQL for efficient data storage and retrieval, while Redis caching significantly improved the performance of dynamic filtering, reducing database load and enhancing user experience.

## Video Overview

Check out our video, "Building a Price Comparison Website with Django, DRF, PostgreSQL, and Redis: A Technical Journey," for an in-depth look at the development process, tech stack, and key features of PriceWise. Learn how our team of dedicated backend engineers, web scrapers, and frontend developers collaborated to create a powerful and user-friendly price comparison platform.

[![PriceWise Video](demo.mp4)](demo.mp4)

## Frontend Repository
Frontend were done by @ahmedRadwan10 and @mohamedsamirr9 but unfortunately they prefer to keep they repo private


> Note: As this is a personal project to showcase my backend engineering skills, the video and frontend repository are for demonstration purposes only and may not be functional or actively maintained.
