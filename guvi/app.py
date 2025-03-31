import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os
import matplotlib.pyplot as plt
import seaborn as sns
import time
import re

# Set page configuration
st.set_page_config(
    page_title="Movies Dashboard 2024",
    page_icon="🎬",
    layout="wide"
)

# Title and description
st.title("Movies Dashboard 2024")
# Custom CSS for a better UI experience
st.markdown("""
    <style>
    /* Background and Fonts */
    body {
        font-family: 'Arial', sans-serif;
        background-color: #121212;
        color: white;
    }

    /* Streamlit Titles */
    .stTitle {
        font-size: 42px !important;
        font-weight: bold !important;
        background: -webkit-linear-gradient(45deg, #ff7eb3, #ff758c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        animation: fadeIn 1.5s ease-in-out;
    }

    /* Custom Header */
    .stMarkdown h1 {
        font-size: 36px;
        color: #ff758c;
        text-align: center;
        font-weight: bold;
    }

    /* Sidebar Customization */
    .stSidebar {
        background-color: #1f1f1f !important;
        border-radius: 15px;
        padding: 20px;
        color: white;
    }
    
    /* Sidebar Inputs */
    .stSidebar select, .stSidebar input {
        background: #262626 !important;
        color: white !important;
        border: 1px solid #ff758c !important;
        border-radius: 5px;
    }

    /* Expander & Dataframe */
    .stExpander {
        background: #1e1e1e !important;
        color: white !important;
    }
    
    /* Button Customization */
    .stButton>button {
        background: linear-gradient(45deg, #ff758c, #ff7eb3);
        color: white !important;
        border: none;
        font-size: 16px;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 25px;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background: linear-gradient(45deg, #ff7eb3, #ff758c);
        transform: scale(1.05);
    }

    /* Metric Box Enhancements */
    .stMetric {
        background: #262626;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0px 5px 15px rgba(255, 117, 140, 0.3);
        text-align: center;
    }

    /* Animations */
    @keyframes fadeIn {
        0% {opacity: 0;}
        100% {opacity: 1;}
    }
    
    </style>
""", unsafe_allow_html=True)

# Check if the database exists
db_path = "movies_2024.db"
db_exists = os.path.exists(db_path)

# Create sample data if database doesn't exist
if not db_exists:
    st.info("Creating sample movie database since it doesn't exist...")
    
    # Sample movie data
    sample_data = {
        'Title': [
            'The Last Adventure', 'Eternal Sunshine', 'Midnight Express',
            'Golden Hour', 'The Silent Echo', 'Parallel Lives',
            'Forgotten Dreams', 'The Lost City', 'Beyond the Stars', 'Winter\'s Tale',
            'The Dark Knight', 'Pulp Fiction', 'The Godfather',
            'Inception', 'The Matrix', 'Interstellar',
            'Fight Club', 'Forrest Gump', 'The Shawshank Redemption', 'Star Wars'
        ],
        'genre': [
            'action', 'romance', 'thriller',
            'drama', 'horror', 'sci-fi',
            'comedy', 'adventure', 'sci-fi', 'drama',
            'action', 'crime', 'crime', 
            'sci-fi', 'sci-fi', 'sci-fi',
            'drama', 'drama', 'drama', 'sci-fi'
        ],
        'Rating': [8.2, 9.1, 7.8, 8.5, 6.9, 7.5, 8.0, 7.2, 9.3, 6.8, 9.0, 8.9, 9.2, 8.8, 8.7, 8.6, 8.8, 8.8, 9.3, 8.6],
        'Votes': [2450, 3200, 1890, 2100, 980, 1500, 2300, 1750, 2800, 1200, 5000, 4800, 4900, 3800, 4200, 3900, 3600, 3700, 4500, 4100],
        'Duration': [
            '2h 15m', '1h 52m', '1h 48m',
            '2h 05m', '1h 37m', '2h 22m',
            '1h 45m', '2h 10m', '2h 30m', '1h 58m',
            '2h 32m', '2h 34m', '2h 55m',
            '2h 28m', '2h 16m', '2h 49m',
            '2h 19m', '2h 22m', '2h 22m', '2h 1m'
        ]
    }
    
    # Create DataFrame
    sample_df = pd.DataFrame(sample_data)
    
    # Create SQLite database and save data
    conn = sqlite3.connect(db_path)
    sample_df.to_sql("movies", conn, index=False, if_exists="replace")
    conn.close()
    
    st.success("Sample movie database created successfully!")

# Function to convert duration to minutes
def convert_to_minutes(duration):
    try:
        hours = 0
        minutes = 0
        if 'h' in duration:
            hours = int(duration.split('h')[0].strip())
        if 'm' in duration:
            minutes = int(duration.split('h')[-1].replace('m', '').strip()) if 'h' in duration else int(duration.replace('m', '').strip())
        return hours * 60 + minutes
    except:
        return None  # Return None for invalid formats

# Function to load data from database with custom SQL query option
@st.cache_data
def load_data(custom_query=None):
    try:
        conn = sqlite3.connect(db_path)
        
        # First, check what tables exist in the database
        table_query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = pd.read_sql(table_query, conn)
        
        if 'movies' not in tables['name'].values:
            st.error("The 'movies' table does not exist in the database.")
            conn.close()
            return pd.DataFrame()
        
        # If movies table exists, read it with either default or custom query
        if custom_query:
            df = pd.read_sql(custom_query, conn)
        else:
            df = pd.read_sql("SELECT * FROM movies", conn)
        
        conn.close()
        
        # Convert data types
        if 'Rating' in df.columns:
            df["Rating"] = pd.to_numeric(df["Rating"], errors='coerce')
        if 'Votes' in df.columns:
            df["Votes"] = pd.to_numeric(df["Votes"], errors='coerce')
        df = df.fillna(0)
        
        return df
    
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Function to generate SQL query from natural language
def generate_sql_query(user_query):
    user_query = user_query.lower()
    
    # Dictionary of common query patterns and corresponding SQL
    query_patterns = {
        # Duration-related queries
        r"duration.*(asc|ascending|shortest|short)": "SELECT * FROM movies ORDER BY Duration_Minutes ASC",
        r"duration.*(desc|descending|longest|long)": "SELECT * FROM movies ORDER BY Duration_Minutes DESC",
        
        # Rating-related queries
        r"highest.*(rating|rated)": "SELECT * FROM movies ORDER BY Rating DESC",
        r"lowest.*(rating|rated)": "SELECT * FROM movies ORDER BY Rating ASC",
        r"rating.*above (\d+\.?\d*)": lambda match: f"SELECT * FROM movies WHERE Rating > {match.group(1)}",
        r"rating.*between (\d+\.?\d*) and (\d+\.?\d*)": lambda match: f"SELECT * FROM movies WHERE Rating BETWEEN {match.group(1)} AND {match.group(2)}",
        
        # Vote-related queries
        r"(most popular|highest vote|most votes)": "SELECT * FROM movies ORDER BY Votes DESC",
        r"(least popular|lowest vote|fewest votes)": "SELECT * FROM movies ORDER BY Votes ASC",
        r"votes?.*above (\d+)": lambda match: f"SELECT * FROM movies WHERE Votes > {match.group(1)}",
        
        # Genre-related queries
        r"(all|show|list) (\w+) movies": lambda match: f"SELECT * FROM movies WHERE genre = '{match.group(2)}'",
        r"(\w+) movies.*(rating|rated).*above (\d+\.?\d*)": lambda match: f"SELECT * FROM movies WHERE genre = '{match.group(1)}' AND Rating > {match.group(3)}",
        
        # Title-related queries
        r"title.*(contain|including|with) (.+)": lambda match: f"SELECT * FROM movies WHERE Title LIKE '%{match.group(2)}%'",
        
        # Top N queries
        r"top (\d+).*rating": lambda match: f"SELECT * FROM movies ORDER BY Rating DESC LIMIT {match.group(1)}",
        r"top (\d+).*votes": lambda match: f"SELECT * FROM movies ORDER BY Votes DESC LIMIT {match.group(1)}",
        r"top (\d+) (\w+) movies": lambda match: f"SELECT * FROM movies WHERE genre = '{match.group(2)}' ORDER BY Rating DESC LIMIT {match.group(1)}",
        
        # Average queries
        r"average.*rating.*genre": "SELECT genre, AVG(Rating) as avg_rating FROM movies GROUP BY genre ORDER BY avg_rating DESC",
        r"average.*duration.*genre": "SELECT genre, AVG(Duration_Minutes) as avg_duration FROM movies GROUP BY genre ORDER BY avg_duration DESC",
        
        # Count queries
        r"(count|number of|how many).*(\w+) movies": lambda match: f"SELECT COUNT(*) as movie_count FROM movies WHERE genre = '{match.group(2)}'",
        r"(count|number of|how many).*(genre|movies)": "SELECT genre, COUNT(*) as movie_count FROM movies GROUP BY genre ORDER BY movie_count DESC",
        
        # Above/below average
        r"above.*(average|avg).*rating": "SELECT * FROM movies WHERE Rating > (SELECT AVG(Rating) FROM movies)",
        r"below.*(average|avg).*rating": "SELECT * FROM movies WHERE Rating < (SELECT AVG(Rating) FROM movies)",
        
        # Best/worst in genre
        r"(best|highest).* (\w+)": lambda match: f"SELECT * FROM movies WHERE genre = '{match.group(2)}' ORDER BY Rating DESC LIMIT 1",
        r"(worst|lowest).* (\w+)": lambda match: f"SELECT * FROM movies WHERE genre = '{match.group(2)}' ORDER BY Rating ASC LIMIT 1",
        
        # Runtime queries
        r"(shorter|less) than (\d+).*minutes": lambda match: f"SELECT * FROM movies WHERE Duration_Minutes < {match.group(2)}",
        r"(longer|more) than (\d+).*minutes": lambda match: f"SELECT * FROM movies WHERE Duration_Minutes > {match.group(2)}",
        
        # Default query if no pattern matches
        "default": "SELECT * FROM movies"
    }
    
    # Try to match the user query with patterns and get corresponding SQL
    for pattern, sql in query_patterns.items():
        match = re.search(pattern, user_query)
        if match:
            if callable(sql):
                return sql(match)
            return sql
    
    # If no pattern matches, return the default query
    return query_patterns["default"]

# Sidebar for navigation and query options
st.sidebar.header("Movies Dashboard Navigation")

# Navigation options
nav_option = st.sidebar.radio(
    "Choose Mode",
    ["Standard Dashboard", "Natural Language Query", "Custom SQL Query"]
)

# If Natural Language Query is selected
if nav_option == "Natural Language Query":
    st.sidebar.subheader("Ask in Plain English")
    
    # Example queries to help users
    st.sidebar.markdown("**Example Queries:**")
    example_queries = [
        "Show all action movies",
        "Give me the top 5 highest rated movies",
        "Show movies with rating above 8",
        "List all horror movies with rating above 7",
        "What is the average rating by genre?",
        "Show movies sorted by duration in ascending order",
        "Show the longest sci-fi movie",
        "Count the number of movies by genre"
    ]
    
    for example in example_queries:
        if st.sidebar.button(example):
            user_nl_query = example
            st.session_state.user_nl_query = user_nl_query
    
    # Text input for user query
    user_nl_query = st.sidebar.text_area(
        "Enter your query in natural language",
        value=st.session_state.get('user_nl_query', ''),
        height=100
    )
    
    if user_nl_query:
        # Generate SQL query from natural language input
        generated_sql = generate_sql_query(user_nl_query)
        
        # Show the generated SQL
        with st.sidebar.expander("Generated SQL Query"):
            st.code(generated_sql, language="sql")
        
        # Load data with the generated query
        movies_df = load_data(generated_sql)
        
        # Add Duration_Minutes if not in the result
        if 'Duration' in movies_df.columns and 'Duration_Minutes' not in movies_df.columns:
            movies_df["Duration_Minutes"] = movies_df["Duration"].apply(convert_to_minutes)

# If Custom SQL Query is selected
elif nav_option == "Custom SQL Query":
    st.sidebar.subheader("Write Your Own SQL Query")
    
    # SQL query input
    sql_query = st.sidebar.text_area(
        "Enter SQL Query",
        "SELECT * FROM movies ORDER BY Rating DESC",
        height=150
    )
    
    # Add a SQL query help expander
    with st.sidebar.expander("SQL Query Examples"):
        st.markdown("""
        **Examples:**
        ```sql
        -- Get all movies sorted by duration (descending)
        SELECT * FROM movies ORDER BY Duration DESC
        
        -- Get top 10 highest rated movies
        SELECT * FROM movies ORDER BY Rating DESC LIMIT 10
        
        -- Get horror movies with rating above 7
        SELECT * FROM movies WHERE genre = 'horror' AND Rating > 7
        
        -- Get average rating by genre
        SELECT genre, AVG(Rating) as avg_rating FROM movies GROUP BY genre ORDER BY avg_rating DESC
        ```
        """)
    
    # Load data with custom query
    movies_df = load_data(sql_query)
    
    # Add Duration_Minutes if not in the result
    if 'Duration' in movies_df.columns and 'Duration_Minutes' not in movies_df.columns:
        movies_df["Duration_Minutes"] = movies_df["Duration"].apply(convert_to_minutes)

# Standard Dashboard with filters
else:  # Standard Dashboard
    # Load all movie data with default query
    movies_df = load_data()
    
    # Convert Duration to Minutes for all rows
    movies_df["Duration_Minutes"] = movies_df["Duration"].apply(convert_to_minutes)
    
    # Drop rows with invalid durations
    movies_df = movies_df.dropna(subset=["Duration_Minutes"])

    # Standard filtering options
    st.sidebar.subheader("Filters & Sorting")
    
    # Genre filter
    genres = ["All"] + sorted(movies_df["genre"].unique().tolist())
    selected_genre = st.sidebar.selectbox("Select Genre", genres, key="genre_select")
    
    # Rating filter
    min_rating, max_rating = st.sidebar.slider(
        "Rating Range", 0.0, 10.0, (0.0, 10.0), key="rating_slider"
    )
    
    # Votes filter
    min_votes, max_votes = st.sidebar.slider(
        "Votes Range", 
        int(movies_df["Votes"].min()), 
        int(movies_df["Votes"].max()), 
        (int(movies_df["Votes"].min()), int(movies_df["Votes"].max())), 
        key="votes_slider"
    )
    
    # Duration filter
    min_duration, max_duration = st.sidebar.slider(
        "Duration (Minutes)", 
        int(movies_df["Duration_Minutes"].min()), 
        int(movies_df["Duration_Minutes"].max()), 
        (int(movies_df["Duration_Minutes"].min()), int(movies_df["Duration_Minutes"].max())), 
        key="duration_slider"
    )
    
    # Sorting options
    sort_by = st.sidebar.selectbox(
        "Sort By",
        ["Rating (High to Low)", "Votes (High to Low)", "Duration (Long to Short)", "Duration (Short to Long)"],
        index=0
    )
    
    # Apply filters
    filtered_data = movies_df.copy()
    
    if selected_genre != "All":
        filtered_data = filtered_data[filtered_data["genre"] == selected_genre]
    
    filtered_data = filtered_data[
        (filtered_data["Rating"] >= min_rating) & 
        (filtered_data["Rating"] <= max_rating) &
        (filtered_data["Votes"] >= min_votes) & 
        (filtered_data["Votes"] <= max_votes) &
        (filtered_data["Duration_Minutes"] >= min_duration) & 
        (filtered_data["Duration_Minutes"] <= max_duration)
    ]
    
    # Apply sorting
    if sort_by == "Rating (High to Low)":
        filtered_data = filtered_data.sort_values("Rating", ascending=False)
    elif sort_by == "Votes (High to Low)":
        filtered_data = filtered_data.sort_values("Votes", ascending=False)
    elif sort_by == "Duration (Long to Short)":
        filtered_data = filtered_data.sort_values("Duration_Minutes", ascending=False)
    else:  # Duration (Short to Long)
        filtered_data = filtered_data.sort_values("Duration_Minutes", ascending=True)
    
    # Update movies_df to use the filtered data for visualizations
    movies_df = filtered_data

# Main dashboard display
if not movies_df.empty:
    # Show a loading animation
    progress_bar = st.progress(0)
    for percent in range(100):
        time.sleep(0.005)  # Faster loading for better UX
        progress_bar.progress(percent + 1)
    
    # Display query result info
    st.subheader("Query Results")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Movies", len(movies_df))
    
    # Only show these metrics if the columns exist in the result
    if 'Rating' in movies_df.columns:
        col2.metric("Average Rating", f"{movies_df['Rating'].mean():.1f}/10")
    if 'genre' in movies_df.columns:
        col3.metric("Genres", len(movies_df['genre'].unique()) if 'genre' in movies_df.columns else "N/A")
    
    # Display result data
    with st.expander("View Data"):
        st.dataframe(movies_df)
    
    # Only create visualizations if we have the necessary columns
    has_rating = 'Rating' in movies_df.columns
    has_genre = 'genre' in movies_df.columns
    has_votes = 'Votes' in movies_df.columns
    has_duration = 'Duration_Minutes' in movies_df.columns
    has_title = 'Title' in movies_df.columns
    
    # Create visualizations based on available columns
    if has_rating and has_title:
        # Create columns for visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            # Top movies chart
            st.subheader("Top Rated Movies")
            top_movies = movies_df.sort_values("Rating", ascending=False).head(10)
            
            fig = px.bar(
                top_movies,
                x="Rating",
                y="Title",
                orientation="h",
                color="Rating",
                color_continuous_scale="Viridis",
                title=f"Top 10 Movies (Based on Rating)",
                text="Rating"
            )
            fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
    
        if has_genre:
            with col2:
                # Genre distribution
                st.subheader("Genre Distribution")
                genre_counts = movies_df["genre"].value_counts().reset_index()
                genre_counts.columns = ["genre", "count"]
                
                fig = px.pie(
                    genre_counts, 
                    values="count", 
                    names="genre",
                    title="Movies by Genre",
                    hole=0.3
                )
                st.plotly_chart(fig, use_container_width=True)
    
    if has_rating and has_votes and has_genre and has_title:
        # Rating vs Votes
        st.subheader("Rating vs Votes")
        fig = px.scatter(
            movies_df,
            x="Votes",
            y="Rating",
            size="Votes",
            color="genre",
            hover_name="Title",
            title="Movie Ratings vs Popularity"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    if has_rating and has_duration:
        # Rating vs. Duration
        st.subheader("Rating vs. Duration")
        # Sort by duration for line chart
        movies_sorted = movies_df.sort_values("Duration_Minutes")
        
        fig_line = px.line(
            movies_sorted,
            x="Duration_Minutes",
            y="Rating",
            markers=True,
            title="Movie Rating Trend Over Duration",
            labels={"Duration_Minutes": "Duration (Minutes)", "Rating": "Rating"},
            line_shape="linear"
        )
        st.plotly_chart(fig_line, use_container_width=True)
    
    if has_rating and has_genre:
        # Box Plot: Rating Distribution by Genre
        st.subheader("Rating Distribution by Genre")
        fig_box = px.box(
            movies_df,
            x="genre",
            y="Rating",
            title="Box Plot of Movie Ratings by Genre",
            labels={"genre": "Genre", "Rating": "Rating"},
            color="genre",
            boxmode="group"
        )
        st.plotly_chart(fig_box, use_container_width=True)
    
    if has_duration and has_genre:
        st.subheader("⏳ Average Movie Duration by Genre")
        if len(movies_df) > 0:
            avg_duration = movies_df.groupby("genre")["Duration_Minutes"].mean().reset_index()
            
            fig_duration = px.bar(
                avg_duration,
                x="genre",
                y="Duration_Minutes",
                title="Average Movie Duration by Genre",
                color="Duration_Minutes",
                color_continuous_scale="Blues"
            )
            st.plotly_chart(fig_duration, use_container_width=True)
    
    if has_votes and has_genre:
        st.subheader("📊 Genres with Highest Average Votes")
        if len(movies_df) > 0:
            avg_votes = movies_df.groupby("genre")["Votes"].mean().reset_index()
            
            fig_votes = px.bar(
                avg_votes,
                x="genre",
                y="Votes",
                title="Genres with Highest Average Votes",
                color="Votes",
                color_continuous_scale="Reds"
            )
            st.plotly_chart(fig_votes, use_container_width=True)
    
    if has_rating:
        st.subheader("📈 Rating Distribution Across Movies")
        fig_box = px.box(
            movies_df, 
            y="Rating", 
            title="Movie Rating Distribution",
            points="all",
            color_discrete_sequence=["green"]
        )
        st.plotly_chart(fig_box, use_container_width=True)
    
    if has_rating and has_genre and len(movies_df["genre"].unique()) > 1:
        st.subheader("🎻 Violin Plot of Movie Ratings by Genre")
        fig_violin = px.violin(
            movies_df,
            x="genre",
            y="Rating",
            title="Violin Plot of Ratings by Genre",
            color="genre",
            box=True,
            points="all"
        )
        st.plotly_chart(fig_violin, use_container_width=True)
    
    if has_rating and has_genre:
        st.subheader("⭐ Average Ratings by Genre")
        if len(movies_df) > 0:
            avg_ratings = movies_df.groupby("genre")["Rating"].mean().reset_index()
            
            fig_genre_ratings = px.bar(
                avg_ratings,
                x="genre",
                y="Rating",
                title="Average Ratings by Genre",
                color="Rating",
                color_continuous_scale="Cividis"
            )
            st.plotly_chart(fig_genre_ratings, use_container_width=True)
    
    if has_rating:
        # Rating Distribution Histogram
        fig_rating_dist = px.histogram(
            movies_df, 
            x="Rating", 
            nbins=20, 
            title="📈 Rating Distribution", 
            marginal="box",
            color_discrete_sequence=["#ff758c"]
        )
        st.plotly_chart(fig_rating_dist, use_container_width=True)
    
    if has_rating and has_votes and len(movies_df) > 5:
        # Correlation plot
        st.subheader("📉 Correlation Between Ratings & Votes")
        fig_corr = px.scatter(
            movies_df, 
            x="Rating", 
            y="Votes",
            title="Correlation Between Ratings & Votes", 
            trendline="ols",
            color="genre" if has_genre else None
        )
        st.plotly_chart(fig_corr, use_container_width=True)
    
    if has_title:
        # Movie details section
        st.subheader("Movie Search")
        search_term = st.text_input("Enter a movie title to search")
        if search_term:
            search_results = movies_df[movies_df["Title"].str.contains(search_term, case=False)]
            if not search_results.empty:
                st.dataframe(search_results)
            else:
                st.info("No movies found matching your search.")
    
    if has_duration and has_title and len(movies_df) > 1:
        # Shortest & Longest Movies
        st.subheader("🎥 Shortest & Longest Movies")
        shortest_movie = movies_df.nsmallest(1, "Duration_Minutes")
        longest_movie = movies_df.nlargest(1, "Duration_Minutes")
        
        col1, col2 = st.columns(2)
        col1.metric("Shortest Movie", shortest_movie["Title"].values[0], f"{shortest_movie['Duration'].values[0]}")
        col2.metric("Longest Movie", longest_movie["Title"].values[0], f"{longest_movie['Duration'].values[0]}")
    
    if has_title and has_rating:
        # Top Movies Listing
        st.subheader("🎬 Top 10 Movies (Based on current sorting)")
        top_movies = movies_df.head(10)
        
        # Display with emojis based on rating
        for _, row in top_movies.iterrows():
            st.write(f"🎬 {row['Title']} - ⭐ {row['Rating']} {'🔥' if row['Rating'] > 8 else '👍'}")

else:
    st.error("No movie data available based on your query. Please try a different query or check your database connection.")