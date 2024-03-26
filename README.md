# Youtube-Data-Harvesting
Project on Youtube Data Harvesting and Warehousing with SQL, Pandas and Streamlit
Description
YouTube Data Harvesting and Warehousing is a project aimed at collecting YouTube data using the YouTube Data API, storing it in a SQL database, and creating an interactive dashboard using Streamlit for data visualization and analysis. This project allows users to gather insights from YouTube channels and videos efficiently.

Features
Harvest YouTube data (channel information, video details, etc.) using the YouTube Data API.
Store collected data in a SQL database for efficient data management.
Create an interactive dashboard using Streamlit for visualizing and analyzing YouTube data.
Support for querying and filtering data based on various criteria.
User-friendly interface for easy navigation and exploration of YouTube data.
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/your_username/BreadcrumbsYouTube-Data-Harvesting-and-Warehousing.git
Install dependencies:

bash
Copy code
cd BreadcrumbsYouTube-Data-Harvesting-and-Warehousing
pip install -r requirements.txt
Obtain API keys:

Obtain a YouTube Data API key from the Google Developer Console.
Update the config.py file with your API key.
Set up the SQL database:

Create a new SQL database (e.g., MySQL) to store the harvested YouTube data.
Update the database connection details in the config.py file.
Usage
Run the Streamlit app:

arduino
Copy code
streamlit run app.py
Access the Streamlit dashboard in your web browser at http://localhost:8501.

Use the dashboard to interact with the YouTube data, explore insights, and perform analysis.

Credits
Google Developers - Documentation for the YouTube Data API.
Streamlit - Framework for building interactive web applications in Python.
MySQL - Relational database management system for storing harvested data.
License
This project is licensed under the MIT License - see the LICENSE file for details
