                                             🎬 Movies Dashboard 2024

A Streamlit-powered interactive dashboard for exploring and analyzing movie data with natural language query capabilities.
![Image](https://github.com/user-attachments/assets/bed2a010-98f4-4a0c-926d-30464bd69134)

## 🚀 Features

- **Interactive Visualizations**: Beautiful charts and graphs to explore movie data
- **Natural Language Query**: Ask questions in plain English like "Show top 5 highest rated movies"
- **Custom SQL Query**: Write your own SQL queries for advanced analysis
- **Smart Filters**: Filter by genre, rating, votes, and duration
- **Responsive Design**: Works on desktop and mobile devices
- **Sample Data**: Auto-generates sample data if no database exists

🛠️ Requirements:

Python 3.8+
Streamlit
Pandas
SQLite3
Plotly Express
Matplotlib
Seaborn
🏃‍♂️ Running the App:
streamlit run app.py

🗃️ Database Structure:
The app uses SQLite with the following sample schema:

Column |	Type |	Description
Title |	TEXT | Movie title
genre	 |TEXT |	Movie genre
Rating |	REAL |	Rating (0-10)
Votes |	INTEGER |	Number of votes
Duration |	TEXT |	Duration in "2h 15m" format
Duration_Minutes |	INTEGER |	Duration in minutes

💡 Usage Examples:
Natural Language Queries
"Show all action movies"
"Give me the top 5 highest rated movies"
"Show movies with rating above 8"

Custom SQL Queries:

-- Get all movies sorted by duration (descending)
SELECT * FROM movies ORDER BY Duration DESC

-- Get top 10 highest rated movies
SELECT * FROM movies ORDER BY Rating DESC LIMIT 10

-- Get horror movies with rating above 7
SELECT * FROM movies WHERE genre = 'horror' AND Rating > 7


🎨 UI Features:
Dark Mode: Sleek dark theme for comfortable viewing
Animated Elements: Smooth transitions and loading animations
Responsive Layout: Adapts to different screen sizes
Interactive Charts: Hover for details, click to filter.

📊 Available Visualizations:

Top Rated Movies Bar Chart
Genre Distribution Pie Chart
Rating vs Votes Scatter Plot
Rating vs Duration Line Chart
Rating Distribution by Genre (Box Plot)
Average Duration by Genre
Violin Plot of Ratings
Correlation Between Ratings & Votes

📧 Contact
Your Name - sibi.sjce26@gmail.com









 
