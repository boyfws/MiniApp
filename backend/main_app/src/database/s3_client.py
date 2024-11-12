import asyncio
from contextlib import asynccontextmanager

from aiobotocore.client import AioBaseClient
from aiobotocore.session import get_session
from fastapi import UploadFile
from src.config import configuration

class S3Client:
    def __init__(self) -> None:
        self.config = {
            "aws_access_key_id": configuration.s3.access_key,
            "aws_secret_access_key": configuration.s3.secret_key,
            "endpoint_url": "https://s3.storage.selcloud.ru",
        }
        self.bucket_name = configuration.s3.bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self) -> AioBaseClient:
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(
            self,
            file: UploadFile
    ):
        async with self.get_client() as client:
            await client.put_object(
                Bucket=self.bucket_name,
                Body=file.file.read(),
            )

    async def delete_file(
            self,
            object_name: str
    ):
        async with self.get_client() as client:
            await client.delete_object(Bucket=self.bucket_name, Key=object_name)
