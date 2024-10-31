from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class CountriesModel(Base):
    __tablename__ = 'countries'
    country_id  = Column(Integer, primary_key=True)
    country_name = Column(String)

    cities = relationship("CitiesModel", back_populates="country")  # Updated back_populates


class CitiesModel(Base):
    __tablename__ = 'cities'
    city_id  = Column(Integer, primary_key=True)
    city_name = Column(String)
    country_id = Column(Integer, ForeignKey("countries.country_id"))
    latitude = Column(Numeric)
    longitude = Column(Numeric)

    country = relationship("CountriesModel", back_populates="cities")  # Updated relationship name
    targets = relationship("TargetsModel", back_populates="city")  # Updated back_populates


class MissionsModel(Base):
    __tablename__ = 'missions'
    mission_id = Column(Integer, primary_key=True)
    mission_date = Column(Date)
    airborne_aircraft = Column(Numeric(10, 2))
    attacking_aircraft = Column(Numeric(10, 2))
    bombing_aircraft = Column(Numeric(10, 2))
    aircraft_returned = Column(Numeric(10, 2))
    aircraft_failed = Column(Numeric(10, 2))
    aircraft_damaged = Column(Numeric(10, 2))
    aircraft_lost = Column(Numeric(10, 2))

    targets = relationship("TargetsModel", back_populates="mission")  # Updated relationship name


class TargetTypesModel(Base):
    __tablename__ = 'targettypes'
    target_type_id = Column(Integer, primary_key=True)
    target_type_name = Column(String)

    targets = relationship("TargetsModel", back_populates="target_type")  # Updated back_populates


class TargetsModel(Base):
    __tablename__ = 'targets'
    target_id = Column(Integer, primary_key=True)
    mission_id = Column(Integer, ForeignKey("missions.mission_id"))
    target_industry = Column(String)
    city_id = Column(Integer, ForeignKey("cities.city_id"))  # Correct ForeignKey reference
    target_type_id = Column(Integer, ForeignKey("targettypes.target_type_id"))
    target_priority = Column(Integer)

    mission = relationship("MissionsModel", back_populates="targets")  # Updated relationship name
    city = relationship("CitiesModel", back_populates="targets")  # Updated relationship name
    target_type = relationship("TargetTypesModel", back_populates="targets")  # Updated relationship name
