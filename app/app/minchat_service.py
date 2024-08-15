import requests
from loguru import logger

class MinchatService:
    headers = {
        "Authorization": "Bearer CLZAZGJBC0C4T3MG9HNS2HVGT"
    }
    endpoint = "https://api.minchat.io"
    admin_user_id = "clzq1lhyk08zd51cdz7mi7w4x"

    def create_user(self, fingerprint):
        response = requests.post(
            f"{self.endpoint}/v1/user",
            headers=self.headers,
            json={
                "name": fingerprint,
                "username": fingerprint
            }
        )
        if response.status_code not in [200, 201]:
            logger.error(response.status_code)
            logger.error(response.json())
        user = response.json()
        if user['success'] != True:
            logger.error(user)
        return user['user']['id']


    def create_chat(self, user_id: str, title: str):
        response = requests.post(
            f"{self.endpoint}/v1/chat",
            headers=self.headers,
            json={
                "user_ids": [user_id, self.admin_user_id],
                "user_id": user_id,
                "title": title
            }
        )
        if response.status_code not in [200, 201]:
            logger.error(response.json())
        chat = response.json()
        logger.info(chat)
        self.send_message(chat['id'], "Waiting for a partner...")
        return chat['id']
    
    def add_user_to_chat(self, minchat_user_id:str, fingerprint:str, chat_id: str):
        response = requests.post(
            f"{self.endpoint}/v1/chat/{chat_id}/participants",
            headers=self.headers,
            json={
                "username": fingerprint,
                "user_id": minchat_user_id,
            }
        )
        if response.status_code not in  [200, 201]:
            logger.error(response.json())
        chat = response.json()
        logger.info(chat)
        self.send_message(chat_id, "Partner joined a chat")
        return True
    
    def send_message(self, chat_id: str, message=""):
        response = requests.post(
            f"{self.endpoint}/v1/messages",
            headers=self.headers,
            json={
                "user_id": self.admin_user_id,
                "chat_id": chat_id,
                "text": message
            }
        )
        if response.status_code not in  [200, 201]:
            logger.error(response.json())
        chat = response.json()
        logger.info(chat)
        return True
    