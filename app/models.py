from sqlalchemy import Column, Integer, Text, ForeignKey, Float, DATETIME, Boolean
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
    modbus_adr = Column(Integer)
    department = Column(Integer)
    number_of_display = Column(Integer)
    cable_number = Column(Integer)
    cable_connection_number = Column(Integer)
    k = Column(Float)
    created_dt = Column(DATETIME, nullable=True)
    description = Column(Text, nullable=True)

    def __repr__(self):
        return f'{self.id} pseudonym = {self.pseudonym}, {self.k} '


class LinesCurrentParams(Base):
    __tablename__ = 'lines_current_params'

    id = Column(Integer, primary_key=True)
    line_number = Column(Integer, unique=True)
    no_connection_counter = Column(Boolean, nullable=True)
    indicator_value = Column(Integer, nullable=True)
    length = Column(Float, nullable=True)
    speed_line = Column(Float, nullable=True)
    updated_dt = Column(DATETIME, nullable=True)

    def __repr__(self):
        return f'{self.id} length = {self.length}, no_connection_counter = {self.no_connection_counter} '




