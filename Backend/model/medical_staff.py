from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy import Column, ForeignKey, Table
from config.db import engine, meta_data


#Modelo para personal medico
medical_staffs = Table("medical_staffs",meta_data,
              Column("id", Integer, primary_key=True),
              Column("professional_card",Integer),
              Column("specialty",String(255),nullable=False),
              Column("personal_type",String(255),nullable=False),
              Column("user_id", ForeignKey("users.id")))



meta_data.create_all(engine)