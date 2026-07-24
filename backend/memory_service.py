"""
memory_service.py

Handles conversation memory for the chatbot.

Initially this service stores chat history in memory.

Later it can be extended to MongoDB
without changing the Conversation Manager.
"""


# ==========================================================
# MEMORY SERVICE
# ==========================================================

import uuid

from datetime import datetime

from database.mongo_service import mongo

class MemoryService:
    """
    Handles loading, saving and clearing
    conversation history.
    """

    def __init__(self):

        self.chat_history = []

        self.session_id = str(uuid.uuid4())

        self.created_at = datetime.utcnow()

        print(
        f"Session Started : {self.session_id}"
    )

    # def load_chat(
    #         self,
    #     session_id=None
    # ):

    #     """
    #     Load conversation from MongoDB.

    #     If session_id is None,
    #     load the current session.
    #     """

    #     if session_id is None:

    #         session_id = self.session_id

    #     return mongo.load_messages(
    #         session_id
    #     )
    def load_chat(
        self,
        session_id=None
    ):

        if session_id is None:
            session_id = self.session_id

        messages = mongo.load_messages(session_id)

        print(f"Loading session: {session_id}")
        print(f"Messages loaded: {len(messages)}")

        return messages
    # ------------------------------------------------------
    def set_current_session(
        self,
        session_id: str
    ):

        """
        Switch to an existing session.
        """

        self.session_id = session_id


    def save_chat(
        self,
        user_message: str,
        assistant_message: str
    ):
        print("save_chat() called")
        """
        Save one conversation turn.
        """

        self.chat_history.append({

            "role": "user",

            "content": user_message

        })

        self.chat_history.append({

            "role": "assistant",

            "content": assistant_message

        })
        mongo.create_session(

        self.session_id,

        user_message

    )
        mongo.save_message(

        self.session_id,

        "user",

        user_message

    )

        mongo.save_message(

        self.session_id,

        "assistant",

        assistant_message

    )

    # ------------------------------------------------------

    def clear_chat(self):
        """
        Clear only the UI memory.
        Do NOT delete MongoDB history.
        """

        self.chat_history = []

        self.session_id = str(uuid.uuid4())

        self.created_at = datetime.utcnow()

        print(
            f"New Session Started : {self.session_id}"
        )

    # ------------------------------------------------------
    

    # ------------------------------------------------------

    def get_recent_sessions(self):

        """
        Return all recent conversation titles.
        """

        return mongo.get_recent_sessions()




    
    def get_recent_history(
        self,
        max_messages: int = 10
    ):

        """
        Return only the recent messages.
        """

        return self.chat_history[-max_messages:]


# ==========================================================
# GLOBAL INSTANCE
# ==========================================================

memory = MemoryService()