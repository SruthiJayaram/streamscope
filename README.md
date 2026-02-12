# StreamScope

StreamScope is a movie analytics dashboard built using Streamlit and MySQL. It provides insights into movie ratings, user activity, and other analytics, making it a powerful tool for understanding user behavior and movie trends.

## Features

- **Top Rated Movies**: Displays the top-rated movies based on user ratings.
- **Most Active Users**: Shows the users who have watched the most movies.
- **Users Who Watched But Didn't Rate**: Identifies users who watched movies but did not provide ratings.
- **Movie Ranking**: Ranks movies using a window function based on average ratings.
- **Simulate Transactions**: Allows users to simulate watch and rating transactions with user-friendly dropdowns for selecting user names and movie titles.

## Technologies Used

- **Frontend**: Streamlit
- **Backend**: MySQL
- **Libraries**: pandas, mysql-connector-python

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the MySQL database:
   - Import the SQL scripts from the `sql/` directory to create and seed the database.
4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## File Structure

- `app.py`: Main Streamlit app for the dashboard.
- `db_config.py`: Handles database connection.
- `sql/`: Contains SQL scripts for database setup and seeding.
- `README.md`: Project documentation.

## Future Enhancements

- Add more analytics features.
- Improve the UI/UX of the dashboard.
- Optimize database queries for better performance.

## License

This project is licensed under the MIT License.