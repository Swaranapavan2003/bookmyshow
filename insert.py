import psycopg2
import dj_database_url

# Database URL from Django settings
DATABASE_URL = 'postgresql://bookmyshow_x782_user:7NLMTMk800qEqu2UjBoq7hDxZ0A3o1ap@dpg-cts1t6a3esus73dlof10-a.oregon-postgres.render.com/bookmyshow_x782'

# Parse the URL to get the connection parameters
db_params = dj_database_url.parse(DATABASE_URL)

def insert_sample_data():
    connection = None  # Initialize connection to avoid UnboundLocalError
    try:
        # Establish connection using parsed parameters
        connection = psycopg2.connect(
            host=db_params['HOST'],
            port=db_params['PORT'],
            database=db_params['NAME'],
            user=db_params['USER'],
            password=db_params['PASSWORD']
        )
        cursor = connection.cursor()

        # Truncate tables to ensure they are empty before inserting new data
        cursor.execute("TRUNCATE TABLE movies_seat, movies_theater, movies_movie RESTART IDENTITY CASCADE;")
        
        # Insert 5 sample movies
        cursor.execute(""" 
            INSERT INTO movies_movie (name, image, rating, "cast", description)
            VALUES
                ('Inception', 'inception.jpg', 8.8, 'Leonardo DiCaprio, Joseph Gordon-Levitt', 'A mind-bending thriller.'),
                ('The_Dark_Knight', 'dark_knight.jpg', 9.0, 'Christian Bale, Heath Ledger', 'A dark and gripping superhero tale.'),
                ('Avatar', 'avatar.jpg', 7.8, 'Sam Worthington, Zoe Saldana', 'A visually stunning alien world adventure.'),
                ('Titanic', 'titanic.jpg', 7.8, 'Leonardo DiCaprio, Kate Winslet', 'A tragic love story set on the ill-fated ship.'),
                ('TheMatrix', 'matrix.jpg', 8.7, 'Keanu Reeves, Laurence Fishburne', 'A hacker discovers a shocking truth about reality.');
        """)

        # Insert 5 theaters and assign 3 showings for each movie
        cursor.execute("""
            INSERT INTO movies_theater (name, movie_id, time)
            VALUES
                ('Theater1', 1, '2024-12-19 10:00:00+00'),
                ('Theater1', 1, '2024-12-19 14:00:00+00'),
                ('Theater1', 1, '2024-12-19 18:00:00+00'),
                ('Theater2', 2, '2024-12-20 12:00:00+00'),
                ('Theater2', 2, '2024-12-20 16:00:00+00'),
                ('Theater2', 2, '2024-12-20 20:00:00+00'),
                ('Theater3', 3, '2024-12-21 10:00:00+00'),
                ('Theater3', 3, '2024-12-21 14:00:00+00'),
                ('Theater3', 3, '2024-12-21 18:00:00+00'),
                ('Theater4', 4, '2024-12-22 12:00:00+00'),
                ('Theater4', 4, '2024-12-22 16:00:00+00'),
                ('Theater4', 4, '2024-12-22 20:00:00+00'),
                ('Theater5', 5, '2024-12-23 12:00:00+00'),
                ('Theater5', 5, '2024-12-23 16:00:00+00'),
                ('Theater5', 5, '2024-12-23 20:00:00+00');
        """)

        # Insert 5 seats per showing for each movie in each theater
        cursor.execute("""
            INSERT INTO movies_seat (seat_number, is_booked, theater_id, payment)
            VALUES
                ('A1', false, 1, false), ('A2', false, 1, false), ('A3', false, 1, false), ('A4', false, 1, false), ('A5', false, 1, false),
                ('B1', false, 2, false), ('B2', false, 2, false), ('B3', false, 2, false), ('B4', false, 2, false), ('B5', false, 2, false),
                ('C1', false, 3, false), ('C2', false, 3, false), ('C3', false, 3, false), ('C4', false, 3, false), ('C5', false, 3, false),
                ('D1', false, 4, false), ('D2', false, 4, false), ('D3', false, 4, false), ('D4', false, 4, false), ('D5', false, 4, false),
                ('E1', false, 5, false), ('E2', false, 5, false), ('E3', false, 5, false), ('E4', false, 5, false), ('E5', false, 5, false),
                       

                ('F1', false, 6, false), ('F2', false, 6, false), ('F3', false, 6, false), ('F4', false, 6, false), ('F5', false, 6, false),
                ('G1', false, 7, false), ('G2', false, 7, false), ('G3', false, 7, false), ('G4', false, 7, false), ('G5', false, 7, false),
                ('H1', false, 8, false), ('H2', false, 8, false), ('H3', false, 8, false), ('H4', false, 8, false), ('H5', false, 8, false),
                ('I1', false, 9, false), ('I2', false, 9, false), ('I3', false, 9, false), ('I4', false, 9, false), ('I5', false, 9, false),
                ('J1', false, 10, false), ('J2', false, 10, false), ('J3', false, 10, false), ('J4', false, 10, false), ('J5', false, 10, false),
                       
                   

    ('K1', false, 11, false), ('K2', false, 11, false), ('K3', false, 11, false), ('K4', false, 11, false), ('K5', false, 11, false),
    ('L1', false, 12, false), ('L2', false, 12, false), ('L3', false, 12, false), ('L4', false, 12, false), ('L5', false, 12, false),
    ('M1', false, 13, false), ('M2', false, 13, false), ('M3', false, 13, false), ('M4', false, 13, false), ('M5', false, 13, false),
    ('N1', false, 14, false), ('N2', false, 14, false), ('N3', false, 14, false), ('N4', false, 14, false), ('N5', false, 14, false),
    ('O1', false, 15, false), ('O2', false, 15, false), ('O3', false, 15, false), ('O4', false, 15, false), ('O5', false, 15, false)

 
                       
                       ;
        """)

        # Commit the transaction
        connection.commit()
        print("Sample data inserted successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection and cursor, ensuring they are only accessed if initialized
        if connection:
            cursor.close()
            connection.close()

# Call the function to insert sample data
insert_sample_data()
