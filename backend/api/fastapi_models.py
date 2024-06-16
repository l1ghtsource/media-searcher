from pydantic import BaseModel
from typing import List

class UploadUrl(BaseModel):
    url: str
    id: int

class UploadCompleteReport(BaseModel):
    id: int
    description: str

class StartProcessAnswer(BaseModel):
    id: int

class UploadByUrl(BaseModel):
    url: str
    description: str

class ShortCluster(BaseModel):
    id: int
    name: str

class ShortFace(BaseModel):
    id: int
    name: str
    url: str

class Video(BaseModel):
    url: str
    description: str
    faces: List[ShortFace]
    cluster: List[ShortCluster]

class SearchSuggest(BaseModel):
    text: str

class ObjectId(BaseModel):
    id: int

class ClustersList(BaseModel):
    title:str = 'Подборки'
    options: List[ShortCluster]

class FacesList(BaseModel):
    title:str = 'Блогеры'
    options: List[ShortFace]