
import os
import uuid

from fastapi import HTTPException, UploadFile
from db import session
from app.baseController import ControllerBase
from app.company.companyDTO import CompanyCreate, CompanyUpdate, CompanySoftDelete
from cryptography.fernet import Fernet
import boto3

from models.models import Company

s3_client = boto3.client(
    's3',
    aws_access_key_id='your_access_key_id',
    aws_secret_access_key='your_secret_access_key'
)

S3_BUCKET_NAME = "your-bucket-name"


class ServiceCompany(ControllerBase[Company, CompanyCreate, CompanyUpdate, CompanySoftDelete]): 
    ...

company = ServiceCompany(Company)

def getByName(db: session, uid: str) -> Company:
    fernet = Fernet(os.getenv("UID_KEY"))
    try:
        name = fernet.decrypt(uid).decode()
    except:
        raise HTTPException(status_code=404, detail="No company with given uid")     
    return db.query(Company).filter(Company.name == name).first()

def upload_picture_to_s3(picture: UploadFile) -> str:
    try:
        # Generate a unique file name
        file_extension = picture.filename.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"

        # Upload the file to S3
        s3_client.upload_fileobj(
            picture.file,
            S3_BUCKET_NAME,
            unique_filename,
            ExtraArgs={"ContentType": picture.content_type}
        )

        # Generate the URL to the file
        picture_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{unique_filename}"

        return picture_url

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload picture: {str(e)}")