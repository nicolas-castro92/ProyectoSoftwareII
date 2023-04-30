from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import engine, meta_data


#Modelo para personal medico
medical_staffs = Table("medical_staffs",meta_data,
              Column("id", Integer, primary_key=True),
              Column("professional_card",Integer),
              Column("specialty",String(255),nullable=False),
              Column("personal_type",String(255),nullable=False),
              Column("user_id", ForeignKey("users.id")))

#Primero se debe de crear la tabla de users, ya que de lo contrario la tabla medical_staff
#no tendrá una tabla a la cual hacer referencia para implementar la ForeignKey("user.id")



meta_data.create_all(engine)