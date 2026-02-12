import streamlit as st
import pandas as pd
from db_config import get_connection

def run_query(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def run_query_with_param(query, param):
    conn = get_connection()
    df = pd.read_sql(query, conn, params=(param,))
    conn.close()
    return df


st.set_page_config(page_title="StreamInsight", layout="wide")

st.title("🎬 StreamInsight – Movie Analytics Dashboard")

# Sidebar Menu
option = st.sidebar.selectbox(
    "Choose Analytics",
    (
        "Top Rated Movies",
        "Most Active Users",
        "Users Who Watched But Didn't Rate",
        "Movie Ranking (Window Function)"
    )
)

# Update duplicate key to ensure uniqueness
duration_sidebar = st.number_input("Duration (minutes)", 1, 300, step=1, key="movie_duration_sidebar")

# Modify the 'Add New Movie' form to handle auto-incrementing movie_id
st.subheader("➕ Add New Movie")

title = st.text_input("Title")
genre = st.text_input("Genre")
year = st.number_input("Release Year", 1900, 2025, step=1, key="release_year_movie_form")
duration_form = st.number_input("Duration (minutes)", 1, 300, step=1, key="movie_duration_form")

if st.button("Add Movie"):
    if title and genre:
        conn = get_connection()
        cursor = conn.cursor()

        # Insert movie without specifying movie_id (auto-increment)
        cursor.execute(
            "INSERT INTO movies (title, genre, release_year, duration) VALUES (%s, %s, %s, %s)",
            (title, genre, year, duration_form)
        )
        conn.commit()
        conn.close()
        st.success("Movie Added Successfully!")
    else:
        st.error("Please fill in all fields.")

# 🔥 1️⃣ Move Transaction into Button
st.subheader("💳 Simulate Watch + Rating Transaction")

# Fetch user names and movie titles from the database
conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT user_id, name FROM users")
users = cursor.fetchall()
user_dict = {user_id: name for user_id, name in users}

cursor.execute("SELECT movie_id, title FROM movies")
movies = cursor.fetchall()
movie_dict = {movie_id: title for movie_id, title in movies}

conn.close()

# Dropdowns for user and movie names
user_name = st.selectbox("User Name", options=list(user_dict.values()))
movie_name = st.selectbox("Movie Name", options=list(movie_dict.values()))
rating_value = st.number_input("Rating (1-5)", min_value=1, max_value=5)

if st.button("Execute Transaction"):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        conn.start_transaction()

        # Get user_id and movie_id from selected names
        user_id = [uid for uid, name in user_dict.items() if name == user_name][0]
        movie_id_tx = [mid for mid, title in movie_dict.items() if title == movie_name][0]

        # Check movie exists
        cursor.execute("SELECT COUNT(*) FROM movies WHERE movie_id = %s", (movie_id_tx,))
        if cursor.fetchone()[0] == 0:
            raise ValueError("Movie does not exist")

        # Insert watch
        cursor.execute(
            "INSERT INTO watch_history (user_id, movie_id, watched_on) VALUES (%s, %s, CURDATE())",
            (user_id, movie_id_tx)
        )

        # Insert rating
        cursor.execute(
            "INSERT INTO ratings (user_id, movie_id, rating, rated_on) VALUES (%s, %s, %s, CURDATE())",
            (user_id, movie_id_tx, rating_value)
        )

        conn.commit()
        st.success("Transaction completed successfully!")

    except Exception as e:
        conn.rollback()
        st.error(f"Transaction failed: {e}")

    finally:
        conn.close()

# 🔥 2️⃣ Fix Release Year Filter (Only Once)
release_year_filter = st.sidebar.number_input(
    "Filter Movies After Year",
    min_value=1900,
    max_value=2025,
    value=2010
)

# 🔥 3️⃣ Safe Parameterized Query
def run_query_with_param(query, param):
    conn = get_connection()
    df = pd.read_sql(query, conn, params=(param,))
    conn.close()
    return df

query = """
    SELECT title, genre
    FROM movies
    WHERE release_year >= %s;
"""

df = run_query_with_param(query, release_year_filter)

# 1️⃣ Top Rated Movies
if option == "Top Rated Movies":

    query = """
        SELECT m.title, ROUND(AVG(r.rating),2) AS avg_rating
        FROM ratings r
        JOIN movies m ON r.movie_id = m.movie_id
        GROUP BY m.title
        ORDER BY avg_rating DESC
        LIMIT 5;
    """

    df = run_query(query)  # No parameters needed for this query
    st.subheader("⭐ Top Rated Movies")
    if not df.empty:
        st.bar_chart(df.set_index(df.columns[0]))
    else:
        st.write("No data available to display.")

# 2️⃣ Most Active Users
elif option == "Most Active Users":

    query = """
        SELECT u.name, COUNT(w.watch_id) AS watch_count
        FROM watch_history w
        JOIN users u ON w.user_id = u.user_id
        GROUP BY u.name
        ORDER BY watch_count DESC
        LIMIT 5;
    """

    df = run_query(query)
    st.subheader("🔥 Most Active Users")
    if not df.empty:
        st.bar_chart(df.set_index(df.columns[0]))
    else:
        st.write("No data available to display.")

# 3️⃣ Users Who Watched But Didn't Rate
elif option == "Users Who Watched But Didn't Rate":

    query = """
        SELECT DISTINCT u.name
        FROM users u
        JOIN watch_history w ON u.user_id = w.user_id
        LEFT JOIN ratings r 
        ON w.user_id = r.user_id AND w.movie_id = r.movie_id
        WHERE r.rating IS NULL;
    """

    df = run_query(query)
    st.subheader("👀 Watched But Didn't Rate")
    if not df.empty:
        st.bar_chart(df.set_index(df.columns[0]))
    else:
        st.write("No data available to display.")

# 4️⃣ Movie Ranking (Window Function)
elif option == "Movie Ranking (Window Function)":

    query = """
        SELECT title,
               RANK() OVER (ORDER BY AVG(rating) DESC) AS rank_position
        FROM ratings
        JOIN movies USING(movie_id)
        GROUP BY title;
    """

    df = run_query(query)
    st.subheader("🏆 Movie Ranking")
    if not df.empty:
        st.bar_chart(df.set_index(df.columns[0]))
    else:
        st.write("No data available to display.")



query = """
    SELECT title, genre
    FROM movies
    WHERE release_year >= %s;
"""

df = run_query_with_param(query, release_year_filter)

st.subheader(f"Movies Released After {release_year_filter}")
if not df.empty:
    st.dataframe(df)
else:
    st.write("No movies found for the selected year.")
