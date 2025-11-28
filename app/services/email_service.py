from app.configs.deb_config import DEB_EMAIL_SERVICE_API_URL,DEB_EMAIL_SERVICE_API_KEY
from app.class_models.service_models import EmailModel
from typing import List
from pydantic import EmailStr
from .import httpx,ic


class DebEmailService(EmailModel):
    @staticmethod
    async def send(recivers_email:List[EmailStr],subject:str,body:str,is_html:bool) -> str | bool:
        try:
            async with httpx.AsyncClient(timeout=90) as client:
                payload={
                    "recivers_email":recivers_email,
                    "subject":subject,
                    "body":body,
                    "is_html":is_html
                }
                headers={
                    "X-Api-Key":DEB_EMAIL_SERVICE_API_KEY,
                }

                response=await client.post(
                    url=DEB_EMAIL_SERVICE_API_URL,
                    json=payload,
                    headers=headers,
                )
                response.raise_for_status()

                return "Email sent successfully"
        
        except Exception as e:
            ic(f"Error : Sending Email via DebEmailService {e}")

            return False