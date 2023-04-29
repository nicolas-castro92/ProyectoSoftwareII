from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy import Column, ForeignKey, Table
from config.db import engine, meta_data

patients = Table("patients",meta_data,
    Column("id", Integer, primary_key=True),
    Column("familiar_id", ForeignKey("familiars.id")),     
    Column("user_id", ForeignKey("users.id"))
)

meta_data.create_all(engine)