# YouTube Data Harvesting and Warehousing using SQL and Streamlit


**Description**

YouTube Data Harvesting and Warehousing is a project aimed at collecting YouTube data using the YouTube Data API, storing it in a SQL database, and creating an interactive dashboard using Streamlit for data visualization and analysis. This project allows users to gather insights from YouTube channels and videos efficiently.

**Features**

Harvest YouTube data (channel information, video details, etc.) using the YouTube Data API.
Store collected data in a SQL database for efficient data management.
Create an interactive dashboard using Streamlit for visualizing and analyzing YouTube data.
Support for querying and filtering data based on various criteria.
User-friendly interface for easy navigation and exploration of YouTube data.

**Installation**
1. Clone the repository:

git clone https://github.com/your_username/YouTube-Data-Harvesting-and-Warehousing.git

2. Install dependencies

cd YouTube-Data-Harvesting-and-Warehousing
pip install -r requirements.txt

3. Obtain API keys:

Obtain a YouTube Data API key from the Google Developer Console.
Update the config.py file with your API key.

4. Set up the SQL database:

Create a new SQL database (e.g., MySQL) to store the harvested YouTube data.
Update the database connection details in the config.py file.

**Usage**
1. Run the Streamlit app:

streamlit run app.py

2. Access the Streamlit dashboard in your web browser at http://localhost:8501.

3. Use the dashboard to interact with the YouTube data, explore insights, and perform analysis.

Credits
Google Developers - Documentation for the YouTube Data API.
Streamlit - Framework for building interactive web applications in Python.
MySQL - Relational database management system for storing harvested data.

License
This project is licensed under the MIT License - see the LICENSE file for details
