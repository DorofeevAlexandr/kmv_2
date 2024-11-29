from sqlalchemy import Column, Integer, Text, ForeignKey, Float, DATETIME
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass

class Lines(Base):
    __tablename__ = 'lines'

    id = Column(Integer, primary_key=True)
    line_number = Column(Integer, unique=True)
    name = Column(Text, unique=True)
    pseudonym = Column(Text, unique=True)
    port = Column(Text)
    modbus_adr = Column(Integer, )
    department = Column(Integer, )
    number_of_display = Column(Integer, )
    cable_number = Column(Integer, )
    cable_connection_number = Column(Integer, )
    k = Column(Float)
    created_dt = Column(DATETIME, nullable=True)
    description = Column(Text, nullable=True)

    def __repr__(self):
        return f'{self.id} pseudonym = {self.pseudonym}, {self.k} '