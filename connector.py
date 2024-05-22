import psycopg2

def store_user_info(user_name, contact, mail_id):
    """Inserts a new row into the any_table table with the provided user_name and contact.

    Args:
        user_name (str): The user name to be inserted.
        contact (str): The user's contact information.

    Returns:
        int: The number of rows inserted (should be 1 for successful insertion).

    Raises:
        psycopg2.OperationalError: If there's an issue connecting to the database.
    """

    connection = None  # Initialize connection to None

    try:
        # Database connection details (replace with your actual credentials)
        db_host = "localhost"
        db_user = "postgres"
        db_password = "123456"
        db_name = "postgres"
        db_port = 5432

        # Establish a connection to the PostgreSQL database
        connection = psycopg2.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=db_port
        )

        # Create a cursor object to execute database operations
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM any_table")
        # Prepare the SQL statement with placeholders for user_name and contact
        print("Connecting to PostgreSQL database...")
        sql = "INSERT INTO any_table (name, contact, email) VALUES (%s, %s, %s)"

        # Create a tuple containing the user_name and contact values
        val = (user_name, contact, mail_id)

        # Execute the INSERT statement with the user_name and contact values
        cursor.execute(sql, val)

        # Commit the changes to the database
        connection.commit()

        # Print the number of rows inserted (should be 1)
        print(cursor.rowcount, "record inserted")

    except psycopg2.OperationalError as err:
        print("Error connecting to PostgreSQL database:", err)
    finally:
        # Ensure proper connection closure (if established)
        if connection:
            cursor.close()
            connection.close()