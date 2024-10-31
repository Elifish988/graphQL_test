from sqlalchemy import Column, Integer, String, Date, Table, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class CountriesModel(Base):
    __tablename__ = 'countries'
    countries_id = Column(Integer, primary_key=True)
    countries_name = Column(String)

    city = relationship("CitiesModel", back_populates="countries")


class CitiesModel(Base):
    __tablename__ = 'cities'
    cities_id = Column(Integer, primary_key=True)
    cities_name = Column(String)
    countries_id = Column(Integer, ForeignKey("countries.countries_id"))
    latitude = Column(Float)
    longitude = Column(Float)

    countries = relationship("CountriesModel", back_populates="city")
    target = relationship("TargetsModel", back_populates="city")


class MissionsModel(Base):
    __tablename__ = 'missions'
    mission_id = Column(Integer, primary_key=True)
    mission_date = Column(Date)
    airborne_aircraft = Column(Float)
    attacking_aircraft = Column(Float)
    bombing_aircraft = Column(Float)
    aircraft_returned = Column(Float)
    aircraft_failed = Column(Float)
    aircraft_damaged = Column(Float)
    aircraft_lost = Column(Float)

    target = relationship("TargetsModel", back_populates="mission")


class TargetTypesModel(Base):
    __tablename__ = 'targettypes'
    target_type_id = Column(Integer, primary_key=True)
    target_type_name = Column(String)

    target = relationship("TargetsModel", back_populates="target_type")

class TargetsModel(Base):
    __tablename__ = 'targets'
    target_id = Column(Integer, primary_key=True)
    mission_id = Column(Integer, ForeignKey("MissionsModel.mission_id"))
    target_industry = Column(String)
    city_id = Column(Integer, ForeignKey("CitiesModel.cities_id"))
    target_type_id = Column(Integer, ForeignKey("TargetTypesModel.target_type_id"))
    target_priority = Column(Integer)

    mission = relationship("MissionsModel", back_populates="target")
    city = relationship("CitiesModel", back_populates="target")
    target_type = relationship("TargetTypesModel", back_populates="target")



