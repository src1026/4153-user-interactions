import pymysql
from .BaseDataService import DataDataService
from pymysql import Error

class MySQLRDBDataService(DataDataService):
    """
    A generic data service for MySQL databases. The class implements common
    methods from BaseDataService and other methods for MySQL. More complex use cases
    can subclass, reuse methods and extend.
    """

    def __init__(self, context):
        super().__init__(context)

    def _get_connection(self):
        try:
            self.connection = pymysql.connect(
                host=self.context["host"],
                port=self.context["port"],
                user=self.context["user"],
                passwd=self.context["password"],
                cursorclass=pymysql.cursors.DictCursor,
                database=self.context["database"],
                autocommit=True
            )
            if self.connection:
                print("Successfully connected to the database")
                cursor = self.connection.cursor()
                cursor.execute("SELECT 1;")  # Simple query to test the connection
                print("Test query executed successfully")
            else:
                print("Connection failed!")
            return self.connection
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            self.connection = None
    def get_data_object(self, table: str, conditions: dict):
        """
        Fetch a single data object by its key.

        :param table: name of the data table
        :param conditions: a dictionary containing key-value pair for filtering
        :return: A single row matching the key, or None if not found.
        """
        try:
            filter_clause = " AND ".join([f"{key}={value}" for key, value in conditions.items()])
            sql_statement = f"SELECT * FROM `{table}` WHERE {filter_clause}"
            with self._get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(sql_statement)
                    result = cursor.fetchone()
            return result
        except Exception as e:
            # Log the error (you can replace print with a proper logging library)
            print(f"Error fetching data object: {e}")
            return None

    def insert(self, table: str, data: dict) -> dict:
        """
        Insert a new row into the specified table.

        :param table: The name of the table to insert data into.
        :param data: A dictionary of column names and their corresponding values.
        :return: The inserted data with the generated primary key (if any).
        """
        try:
            # Avoid inserting duplicates (especially in the case of following relations)
            filter_clause = " AND ".join([f"{key}=%s" for key in data.keys()])
            sql_check_duplicate = f"SELECT * FROM `{table}` WHERE {filter_clause}"

            columns = ", ".join(data.keys())
            placeholders = ", ".join(["%s"] * len(data))
            sql_statement = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

            with self._get_connection() as connection:
                with connection.cursor() as cursor:
                    # # Inspect table content
                    # print("----------CHECKPOINT----------")
                    # cursor.execute(f"SELECT * FROM `{table}`")
                    # rows = cursor.fetchall()
                    # if rows:
                    #     print("Existing records in the table:")
                    #     for row in rows:
                    #         print(row)  # Print each row as a dictionary
                    # else:
                    #     print("The table is empty.")
                    cursor.execute(sql_check_duplicate, list(data.values()))
                    result = cursor.fetchall()
                    if len(result) > 0:
                        print("Duplicated data entry found.")
                        return None
                    cursor.execute(sql_statement, list(data.values()))
                    inserted_id = cursor.lastrowid  # Get the ID of the newly inserted row
            return {"id": inserted_id, **data}
        except Exception as e:
            print(f"Error inserting data into table {table}: {e}")
            return None

    def update(self, table: str, conditions: dict, data: dict) -> bool:
        """
        Update a row in the specified table.

        :param table: name of the data table
        :param conditions: a dictionary containing key-value pair for filtering
        :param data: A dictionary of column names and new values.
        :return: Updated data if the update was successful, None otherwise.
        """
        try:
            set_clause = ", ".join([f"{col}=%s" for col in data.keys()])
            filter_clause = " AND ".join([f"{key}={value}" for key, value in conditions.items()])
            sql_statement = f"UPDATE `{table}` SET {set_clause} WHERE {filter_clause}"

            with self._get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(sql_statement, list(data.values()))
                    connection.commit()
                    if data is None:
                        return None
                    return data
        except Exception as e:
            print(f"Error updating data: {e}")
            return None

    def delete(self, table: str, conditions: dict) -> bool:
        """
        Delete a row from the specified table.

        :param table: name of the data table
        :param conditions: a dictionary containing key-value pair for filtering
        :return: True if the row was deleted, False otherwise.
        """
        try:
            filter_clause = " AND ".join([f"{key}={value}" for key, value in conditions.items()])
            sql_statement = f"DELETE FROM `{table}` WHERE {filter_clause}"

            with self._get_connection() as connection:
                with connection.cursor() as cursor:
                    # To inspect database content for debugging
                    # print("-------CHECKPOINT----------")
                    # cursor.execute(f"SELECT * FROM `{table}`")
                    # rows = cursor.fetchall()
                    # if rows:
                    #     print("Existing records in the table:")
                    #     for row in rows:
                    #         print(row)
                    # else:
                    #     print("The table is empty.")
                    cursor.execute(sql_statement)
                    return cursor.rowcount > 0  # Check if any rows were deleted
        except Exception as e:
            print(f"Error deleting data: {e}")
            return False