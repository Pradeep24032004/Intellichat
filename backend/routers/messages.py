"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from .. import models, oauth2
from ..utils import dbAdaptor, openai_client

router = APIRouter()
db = dbAdaptor.DBAdaptor()

@router.post("/message", response_model=models.MessageOut)
async def post_message(
    message: models.MessageCreate,
    current_user: dict = Depends(oauth2.get_current_user)
):
    user = await db.get_user_by_email(current_user["email"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    posted = await db.post_message(message.content, str(user["_id"]))
    if not posted:
        raise HTTPException(status_code=500, detail="Message could not be posted")
    
    # Add user_id to the response so frontend can identify current user
    posted["user_id"] = str(user["_id"])
    posted["email"] = current_user["email"]
    posted["is_ai"] = False
    
    return posted

@router.post("/ai-message", response_model=models.MessageOut)
async def post_ai_message(
    message: models.AIMessageCreate,
    current_user: dict = Depends(oauth2.get_current_user)
):
    user = await db.get_user_by_email(current_user["email"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # First, post the user's message
    user_message = await db.post_message(message.content, str(user["_id"]))
    if not user_message:
        raise HTTPException(status_code=500, detail="Message could not be posted")

    # Get AI response
    try:
        ai_response = await openai_client.get_ai_response(message.content)
        
        # Post AI response as a message
        ai_message = await db.post_ai_message(ai_response, str(user["_id"]))
        if not ai_message:
            raise HTTPException(status_code=500, detail="AI response could not be posted")
        
        return ai_message
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")

@router.get("/messages", response_model=List[models.MessageOut])
async def get_messages(current_user: dict = Depends(oauth2.get_current_user)):
    messages = await db.get_all_messages()
    
    # Add email information to each message for proper user identification
    for message in messages:
        if not message.get("is_ai", False):
            # Get user info for each message
            user = await db.get_user_by_id(message["user_id"])
            if user:
                message["email"] = user["email"]
        else:
            message["email"] = "ai@assistant.com"  # Special email for AI messages
    
    return messages

@router.delete("/delete_message/message_id}", status_code=204)
async def delete_message(
    message_id: str,
    current_user: dict = Depends(oauth2.get_current_user)
):
    user = await db.get_user_by_email(current_user["email"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    success = await db.delete_user_message(message_id, str(user["_id"]))
    if not success:
        raise HTTPException(status_code=403, detail="Not authorized to delete this message")

    return
"""

from fastapi import APIRouter, HTTPException, Depends
from .. import models, oauth2

def get_router(db):
    router = APIRouter()

    @router.get("/messages", response_model=list[models.MessageOut])
    async def get_all_messages():
        return await db.get_all_messages()

    @router.post("/messages", response_model=models.MessageOut)
    async def post_message(msg: models.MessageCreate, current_user=Depends(oauth2.get_current_user)):
        return await db.post_message(msg.content, current_user["email"])

    @router.post("/ai-message", response_model=models.MessageOut)
    async def post_ai_message(msg: models.AIMessageCreate, current_user=Depends(oauth2.get_current_user)):
        return await db.post_ai_message(msg.content, current_user["email"])

    @router.delete("/messages/{message_id}")
    async def delete_message(message_id: str, current_user=Depends(oauth2.get_current_user)):
        success = await db.delete_user_message(message_id, current_user["email"])
        if not success:
            raise HTTPException(status_code=403, detail="Not authorized or message not found")
        return {"status": "deleted"}

    return router
