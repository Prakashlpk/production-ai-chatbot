"""
postgres_service.py

Handles PostgreSQL connection.
"""

import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")


class PostgresService:

    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=POSTGRES_HOST,
                port=POSTGRES_PORT,
                database=POSTGRES_DATABASE,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD
            )

            self.cursor = self.connection.cursor()
            self.cursor.execute("SELECT current_database();")

            print(
                "Connected Database :",
                self.cursor.fetchone()[0]
            )

            print("✅ PostgreSQL Connected")

        except Exception as error:
            print(f"PostgreSQL Connection Error: {error}")

    def create_tables(self):
        """
        Create required PostgreSQL tables.
        """

        try:
            print("Creating PostgreSQL Tables...")
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_logs (

                    id SERIAL PRIMARY KEY,

                    session_id VARCHAR(100),

                    user_message TEXT,

                    assistant_response TEXT,

                    model_name VARCHAR(50),

                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

                );
            """)

            self.connection.commit()

            print("✅ PostgreSQL Tables Created")

        except Exception as error:

            print(f"Table Creation Error: {error}")



    # ------------------------------------------------------

    def save_chat_log(
        self,
        session_id: str,
        user_message: str,
        assistant_response: str,
        model_name: str
    ):

        """
        Save one chat into PostgreSQL.
        """

        try:

            self.cursor.execute(

                """
                INSERT INTO chat_logs
                (
                    session_id,
                    user_message,
                    assistant_response,
                    model_name
                )

                VALUES
                (%s,%s,%s,%s)
                """,

                (

                    session_id,

                    user_message,

                    assistant_response,

                    model_name

                )

            )

            self.connection.commit()

        except Exception as error:

            print(

                f"PostgreSQL Save Error : {error}"

            )        


postgres = PostgresService()