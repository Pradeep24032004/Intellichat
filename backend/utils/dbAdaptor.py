# utils/dbAdaptor.py (Updated with AI message support)

from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import os
from dotenv import load_dotenv
from ..auth import hash_password, verify_password
from ..utils import openai_client


load_dotenv()

class DBAdaptor:
    def __init__(self):
        self.client = None
        self.db = None
        self.users_collection = None
        self.messages_collection = None

    async def init_room(self):
        # Initialize MongoDB connection
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")
        self.client = MongoClient(mongodb_url)
        self.db = self.client["chat_app"]
        self.users_collection = self.db["users"]
        self.messages_collection = self.db["messages"]

    async def sign_up_user(self, username: str, email: str, password: str):
        # Check if user already exists
        existing_user = self.users_collection.find_one({"email": email})
        if existing_user:
            return None
        
        # Hash password and create user
        hashed_password = hash_password(password)
        user_data = {
            "username": username,
            "email": email,
            "password": hashed_password,
            "created_at": datetime.utcnow()
        }
        
        result = self.users_collection.insert_one(user_data)
        if result.inserted_id:
            return {
                "id": str(result.inserted_id),
                "username": username,
                "email": email
            }
        return None

    async def sign_in_user(self, email: str, password: str):
        user = self.users_collection.find_one({"email": email})
        if user and verify_password(password, user["password"]):
            return {
                "id": str(user["_id"]),
                "username": user["username"],
                "email": user["email"]
            }
        return None

    async def get_user_by_email(self, email: str):
        user = self.users_collection.find_one({"email": email})
        if user:
            return {
                "_id": user["_id"],
                "username": user["username"],
                "email": user["email"]
            }
        return None

    async def get_user_by_id(self, user_id: str):
        try:
            user = self.users_collection.find_one({"_id": ObjectId(user_id)})
            if user:
                return {
                    "_id": user["_id"],
                    "username": user["username"],
                    "email": user["email"]
                }
        except:
            pass
        return None
    """
    async def post_message(self, content: str, user_id: str):
        user = await self.get_user_by_id(user_id)
        if not user:
            return None
        
        message_data = {
            "content": content,
            "user_id": user_id,
            "username": user["username"],
            "timestamp": datetime.utcnow(),
            "is_ai": False
        }
        
        result = self.messages_collection.insert_one(message_data)
        if result.inserted_id:
            return {
                "id": str(result.inserted_id),
                "content": content,
                "user_id": user_id,
                "username": user["username"],
                "timestamp": message_data["timestamp"],
                "is_ai": False
            }
        return None
    """ 
    async def post_message(self, content: str, email: str):
        user = await self.get_user_by_email(email)
        if not user:
            return None

        message_data = {
            "content": content,
            "user_id": str(user["_id"]),
            "username": user["username"],
            "timestamp": datetime.utcnow(),
            "is_ai": False,
            "email": user["email"]
        }

        result = self.messages_collection.insert_one(message_data)
        if result.inserted_id:
            return {
                "id": str(result.inserted_id),
                "content": content,
                "user_id": str(user["_id"]),
                "username": user["username"],
                "timestamp": message_data["timestamp"],
                "is_ai": False,
                "email": user["email"]
            }
        return None

    async def post_ai_message(self, content: str, requesting_user_id: str):
        message_data = {
            "content": content,
            "user_id": "ai_assistant",
            "username": "AI Assistant",
            "timestamp": datetime.utcnow(),
            "is_ai": True,
            "requested_by": requesting_user_id
        }
        
        result = self.messages_collection.insert_one(message_data)
        if result.inserted_id:
            return {
                "id": str(result.inserted_id),
                "content": content,
                "user_id": "ai_assistant",
                "username": "AI Assistant",
                "timestamp": message_data["timestamp"],
                "is_ai": True,
                "email": "ai@assistant.com"
            }
        return None
    async def post_ai_message(self, user_message: str, requesting_user_email: str):
        # Get AI response text from OpenAI API
        ai_response_text = await openai_client.get_ai_response(user_message)  # since your get_ai_response is async

        message_data = {
            "content": ai_response_text,
            "user_id": "ai_assistant",
            "username": "AI Assistant",
            "timestamp": datetime.utcnow(),
            "is_ai": True,
            "requested_by": requesting_user_email
        }
    
        result = self.messages_collection.insert_one(message_data)
        if result.inserted_id:
            return {
                "id": str(result.inserted_id),
                "content": ai_response_text,
                "user_id": "ai_assistant",
                "username": "AI Assistant",
                "timestamp": message_data["timestamp"],
                "is_ai": True,
                "email": "ai@assistant.com"
            }
        return None

    async def get_all_messages(self):
        messages = list(self.messages_collection.find().sort("timestamp", 1))
        result = []
        
        for msg in messages:
            result.append({
                "id": str(msg["_id"]),
                "content": msg["content"],
                "user_id": msg["user_id"],
                "username": msg["username"],
                "email": msg.get("email", ""),
                "timestamp": msg["timestamp"],
                "is_ai": msg.get("is_ai", False)
            })

            """
            result.append({
                "id": str(msg["_id"]),
                "content": msg["content"],
                "user_id": msg["user_id"],
                "username": msg["username"],
                "timestamp": msg["timestamp"],
                "is_ai": msg.get("is_ai", False)
            })
            """
        return result

    async def delete_user_message(self, message_id: str, user_id: str):
        try:
            # Check if message exists and belongs to user (or if user is admin)
            message = self.messages_collection.find_one({
                "_id": ObjectId(message_id),
                "$or": [
                    {"user_id": user_id},
                    {"requested_by": user_id}  # Allow deletion of AI messages requested by user
                ]
            })
            
            if message:
                result = self.messages_collection.delete_one({"_id": ObjectId(message_id)})
                return result.deleted_count > 0
        except:
            pass
        return False

