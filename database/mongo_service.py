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

        try:

            self.client = MongoClient(
                MONGODB_URI
            )

            self.database = self.client[
                DATABASE_NAME
            ]

            print("✅ MongoDB Connected")

        except Exception as error:

            print(
                f"MongoDB Connection Error: {error}"
            )

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

        collection = self.database["chat_history"]

        collection.insert_one(

        {

            "session_id": session_id,

            "role": role,

            "content": content,

            "timestamp": datetime.utcnow()

        }

    )
        
    # ------------------------------------------------------
    # ------------------------------------------------------

    def create_session(
        self,
        session_id: str,
        title: str
    ):
        print("create_session() called")

        """
        Create a new conversation session.
        """

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


    def load_messages(
        self,
        session_id: str
    ):

        """
        Load all messages for one session.
        """

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
    
    # ------------------------------------------------------

    def get_recent_sessions(self):

        """
        Return all conversation sessions.
        """

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

    # ------------------------------------------------------

    def clear_session(
        self,
        session_id: str
    ):

        """
        Delete all messages
        belonging to one session.
        """

        collection = self.database["chat_history"]

        collection.delete_many(

            {

                "session_id": session_id

            }

        )

    def get_database(self):

        """
        Return the database instance.
        """

        return self.database


# ==========================================================
# GLOBAL INSTANCE
# ==========================================================

mongo = MongoService()