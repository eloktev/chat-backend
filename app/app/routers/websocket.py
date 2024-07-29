from fastapi import APIRouter, WebSocket, Depends, WebSocketDisconnect
from sqlalchemy.orm import Session
from ..db import get_db
from .. import crud
from typing import List, Dict
from loguru import logger

router = APIRouter()

# Store connected clients
active_connections: Dict[int, List[WebSocket]] = {}

@router.websocket("/ws/chats/{topic_id}")
async def websocket_endpoint(websocket: WebSocket, topic_id: int, db: Session = Depends(get_db)):
    await websocket.accept()
    logger.info(f"WebSocket connection established for topic_id: {topic_id}")

    # Initialize the topic in active_connections if not already
    if topic_id not in active_connections:
        active_connections[topic_id] = []

    # Check if the topic already has two users connected
    if len(active_connections[topic_id]) >= 2:
        await websocket.close()
        logger.info(f"WebSocket connection closed: too many connections for topic_id: {topic_id}")
        return

    # Add the connection to the list
    active_connections[topic_id].append(websocket)
    logger.info(f"Added connection for topic_id: {topic_id}. Total connections: {len(active_connections[topic_id])}")

    try:
        if len(active_connections[topic_id]) == 2:
            # Notify both users to start the chat and mark the topic as inactive
            crud.mark_topic_inactive(db, topic_id)
            logger.info(f"Marking topic_id: {topic_id} as inactive and starting chat")
            for connection in active_connections[topic_id]:
                await connection.send_json({"action": "start_chat", "topic_id": topic_id})

        # Main communication loop
        while True:
            data = await websocket.receive_text()
            logger.info(f"Received message for topic_id: {topic_id}: {data}")
            # Broadcast the received message to all connected clients
            for connection in active_connections[topic_id]:
                if connection != websocket:
                    await connection.send_text(data)
    except WebSocketDisconnect:
        # Remove the connection when the client disconnects
        if websocket in active_connections[topic_id]:
            active_connections[topic_id].remove(websocket)
            logger.info(f"Connection removed for topic_id: {topic_id}. Total connections: {len(active_connections[topic_id])}")
            if active_connections[topic_id]:
                # Notify the remaining user that their partner has left
                remaining_user = active_connections[topic_id][0]
                await remaining_user.send_json({"action": "user_left"})
                logger.info(f"Notified remaining user that their partner has left for topic_id: {topic_id}")
            if not active_connections[topic_id]:
                del active_connections[topic_id]
                logger.info(f"Deleted topic_id: {topic_id} from active connections")