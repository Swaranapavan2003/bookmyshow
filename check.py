import psycopg2
import dj_database_url

# Database URL from Django settings (replace with your actual DATABASES configuration if needed)
DATABASE_URL = 'postgresql://bookmyshow_x782_user:7NLMTMk800qEqu2UjBoq7hDxZ0A3o1ap@dpg-cts1t6a3esus73dlof10-a.oregon-postgres.render.com/bookmyshow_x782'

# Parse the URL to get the connection parameters
db_params = dj_database_url.parse(DATABASE_URL)

def get_tables():
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

        # Query to get all table names
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND (table_name LIKE 'm%' OR table_name LIKE 's%' OR table_name LIKE 'auth_user')
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()

        # If tables are found, print their names and fetch the schema and data
        if tables:
            print("Tables in the database:")
            for table in tables:
                table_name = table[0]
                print(f"\nTable: {table_name}")

                # Get schema (column names and types) for each table
                cursor.execute(f"""
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_name = '{table_name}' AND table_schema = 'public';
                """)
                schema = cursor.fetchall()

                if schema:
                    print("Schema (Columns and Data Types):")
                    for column in schema:
                        print(f"  {column[0]} - {column[1]}")  # column[0] is column name, column[1] is data type
                else:
                    print("No schema found for this table.")

                # Get data from the table
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")  # Limiting to 5 rows for display
                data = cursor.fetchall()

                if data:
                    print("Data (First 5 Rows):")
                    for row in data:
                        print(row)
                else:
                    print("No data found in this table.")
        else:
            print("No tables found in the database.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection and cursor
        if connection:
            cursor.close()
            connection.close()

# Call the function to get the tables
get_tables()
