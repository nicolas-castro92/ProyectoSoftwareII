from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy import Column, ForeignKey, Table
from config.db import engine, meta_data

users = Table(
    "users",meta_data,
    Column("id", Integer, primary_key=True),
    Column("name",String(255),nullable=False),
    Column("last_name",String(255),nullable=False),
    Column("identification_card",Integer,nullable=False),
    Column("age",Integer,nullable=False),
    Column("phone",Integer,nullable=False),
    Column("email", String(255),nullable=False),
    Column("password", String(255)),
    Column("address", String(255),nullable=False),
)



meta_data.create_all(engine)