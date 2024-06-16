from sqlalchemy import Column, Integer, String, Boolean, Float, ARRAY, Table, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


Video2Face = Table(
    "Video2Face",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("videoId", Integer, ForeignKey("Video.id")),
    Column("faceId", Integer, ForeignKey("Face.id")),
)


class Video(Base):
    __tablename__ = "Video"
    id = Column(Integer, primary_key=True, index=True)
    clickhouse_id = Column(Integer, default=-1)
    description = Column(String, default="")
    speech_text = Column(String, default="")
    known_faces = relationship("Face", secondary=Video2Face, back_populates="videos")
    cluster_id = Column(Integer, ForeignKey("Cluster.id"))
    #cluster = relationship("Cluster", back_populates="videos")
    url = Column(String, default="")
    url_expire = Column(Integer, default=0)

    def to_json(self):
        if self.cluster is None:
            cluster = []
        else:
            cluster = [{"id": self.cluster.id, "name": self.cluster.name}]
        return {
            "url": self.url,
            "description": self.description,
            "faces": [{"id": f.id, "name": f.name, "url": f.image_url} for f in self.known_faces],
            "cluster": cluster
        }

class Face(Base):
    __tablename__ = "Face"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="")
    embedding_uuid = Column(String)
    image_id = Column(Integer, default=0)
    image_url = Column(String, default="")
    image_url_expire = Column(Integer, default=0)
    videos = relationship("Video", secondary=Video2Face, back_populates ="known_faces")

class Cluster(Base):
    __tablename__ = "Cluster"
    id = Column(Integer, primary_key=True, index=True)
    cluster_df_id = Column(Integer)
    clickhouse_id = Column(Integer, default=-1)
    name =  Column(String, default="")
    videos = relationship("Video", backref="cluster")
