"""
mongo_service.py

Handles all MongoDB operations.
"""

# ==========================================================
# IMPORTS
# ==========================================================

import os

from datetime import datetime

from dotenv import load_dotenv

from pymongo import MongoClient


# ==========================================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================================

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

DATABASE_NAME = os.getenv(
    "MONGODB_DATABASE",
    "AI_CHATBOT"
)


# ==========================================================
# MONGO SERVICE
# ==========================================================

class MongoService:

    """
    Handles MongoDB connection.
    """

    def __init__(self):

        self.client = None

        self.database = None

    # ------------------------------------------------------

    def connect(self):
        """
        Connect to MongoDB.
        """
        if not MONGODB_URI:
            print("MONGODB_URI is missing.")
            return False

        try:

            self.client = MongoClient(
                MONGODB_URI,
                serverSelectionTimeoutMS=5000
            )

            # Force a connection attempt
            self.client.admin.command("ping")

            self.database = self.client[
                DATABASE_NAME
            ]

            print("✅ MongoDB Connected")

            return True

        except Exception as error:

            print(f"MongoDB Connection Error: {error}")

            self.client = None
            self.database = None

            return False
        # ------------------------------------------------------
        # ------------------------------------------------------

    def save_message(
        self,
        session_id: str,
        role: str,
        content: str
    ):

        """
        Save one message into MongoDB.
        """

        if self.database is None:
            print("MongoDB unavailable. Message not saved.")
            return

        try:

            collection = self.database["chat_history"]

            collection.insert_one(

                {

                    "session_id": session_id,

                    "role": role,

                    "content": content,

                    "timestamp": datetime.utcnow()

                }

            )

        except Exception as error:

            print(f"MongoDB Error: {error}")    
        # ------------------------------------------------------
    # ------------------------------------------------------

    def create_session(
        self,
        session_id: str,
        title: str
    ):

        print("create_session() called")

        if self.database is None:
            print("MongoDB unavailable. Session not created.")
            return

        try:

            collection = self.database["sessions"]

            existing = collection.find_one(

                {

                    "session_id": session_id

                }

            )

            if existing:

                return

            collection.insert_one(

                {

                    "session_id": session_id,

                    "title": title,

                    "created_at": datetime.utcnow(),

                    "last_updated": datetime.utcnow()

                }

            )

        except Exception as error:

            print(f"MongoDB Error: {error}")


    def load_messages(
        self,
        session_id: str
    ):

        """
        Load all messages for one session.
        """

        if self.database is None:
            print("MongoDB unavailable. Returning empty messages.")
            return []

        try:

            collection = self.database["chat_history"]

            messages = collection.find(

                {

                    "session_id": session_id

                }

            ).sort(

                "timestamp",

                1

            )

            history = []

            for message in messages:

                history.append(

                    {

                        "role": message["role"],

                        "content": message["content"]

                    }

                )

            return history

        except Exception as error:

            print(f"MongoDB Error: {error}")

            return []
    # ------------------------------------------------------

    def get_recent_sessions(self):

        """
        Return all conversation sessions.
        """

        if self.database is None:
            print("MongoDB unavailable. Returning empty sessions.")
            return []

        try:

            collection = self.database["sessions"]

            sessions = collection.find().sort(

                "last_updated",

                -1

            )

            recent = []

            for session in sessions:

                recent.append(

                    {

                        "session_id": session["session_id"],

                        "title": session["title"]

                    }

                )

            return recent

        except Exception as error:

            print(f"MongoDB Error: {error}")

            return []
    # ------------------------------------------------------

    def clear_session(
        self,
        session_id: str
    ):

        """
        Delete all messages belonging to one session.
        """

        if self.database is None:
            print("MongoDB unavailable. Session not cleared.")
            return

        try:

            collection = self.database["chat_history"]

            collection.delete_many(

                {

                    "session_id": session_id

                }

            )

        except Exception as error:

            print(f"MongoDB Error: {error}")

    def get_database(self):

        """
        Return the database instance.
        """

        return self.database


# ==========================================================
# GLOBAL INSTANCE
# ==========================================================

mongo = MongoService()