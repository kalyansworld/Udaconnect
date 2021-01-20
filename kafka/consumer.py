from __future__ import annotations
from kafka import KafkaConsumer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from geoalchemy2.types import Geometry as GeometryType
from marshmallow import Schema, fields
from marshmallow_sqlalchemy.convert import ModelConverter as BaseModelConverter
from dataclasses import dataclass
from datetime import datetime
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from shapely.geometry.point import Point
from sqlalchemy import BigInteger, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.hybrid import hybrid_property
import json
import ast

base = declarative_base()

class Person(base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    company_name = Column(String, nullable=False)


class Location(base):
    __tablename__ = "location"

    id = Column(BigInteger, primary_key=True)
    person_id = Column(Integer, ForeignKey(Person.id), nullable=False)
    coordinate = Column(Geometry("POINT"), nullable=False)
    creation_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    _wkt_shape: str = None

    @property
    def wkt_shape(self) -> str:
        # Persist binary form into readable text
        if not self._wkt_shape:
            point: Point = to_shape(self.coordinate)
            # normalize WKT returned by to_wkt() from shapely and ST_AsText() from DB
            self._wkt_shape = point.to_wkt().replace("POINT ", "ST_POINT")
        return self._wkt_shape

    @wkt_shape.setter
    def wkt_shape(self, v: str) -> None:
        self._wkt_shape = v

    def set_wkt_with_coords(self, lat: str, long: str) -> str:
        self._wkt_shape = f"ST_POINT({lat} {long})"
        return self._wkt_shape

    @hybrid_property
    def longitude(self) -> str:
        coord_text = self.wkt_shape
        return coord_text[coord_text.find(" ") + 1 : coord_text.find(")")]

    @hybrid_property
    def latitude(self) -> str:
        coord_text = self.wkt_shape
        return coord_text[coord_text.find("(") + 1 : coord_text.find(" ")]


class LocationSchema(Schema):
    id = fields.Integer()
    person_id = fields.Integer()
    longitude = fields.String(attribute="longitude")
    latitude = fields.String(attribute="latitude")
    creation_time = fields.DateTime()

    class Meta:
        model = Location


def create_person(resp):
    new_person = Person()
    new_person.first_name = resp["first_name"]
    new_person.last_name = resp["last_name"]
    new_person.company_name = resp["company_name"]
    db_string = "postgres://ct_admin:wowimsosecure@localhost:32234/geoconnections"
    db = create_engine(db_string)
    Session = sessionmaker(bind=db)
    session = Session()
    qry=session.query(func.max(Person.id).label("max_id"))
    new_person.id=(qry.one().max_id)+1
    session.add(new_person)
    session.commit()
    print(new_person)


def create_location(resp):
    validation_results: Dict = LocationSchema().validate(location)
    if validation_results:
        logger.warning(f"Unexpected data format in payload: {validation_results}")
        raise Exception(f"Invalid payload: {validation_results}")

    new_location = Location()
    new_location.person_id = location["person_id"]
    new_location.creation_time = location["creation_time"]
    new_location.coordinate = ST_Point(location["latitude"], location["longitude"])

    db_string = "postgres://ct_admin:wowimsosecure@localhost:32234/geoconnections"
    db = create_engine(db_string)
    Session = sessionmaker(bind=db)
    session = Session()
    qry=session.query(func.max(Location.id).label("max_id"))
    new_location.id=(qry.one().max_id)+1
    session.add(new_location)
    session.commit()
    print(new_location)

consumer = KafkaConsumer('sample',
     bootstrap_servers=['kafka:9092'],
     value_deserializer=lambda m: json.dumps(m.decode('utf-8')))

for message in consumer:
    resp=eval(json.loads((message.value)))
    if "first_name" in resp:
        print("Person")
    else:
         create_location(resp)
