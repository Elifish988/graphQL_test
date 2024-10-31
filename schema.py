import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from db.database import db_session
from db.models import CountriesModel, CitiesModel, MissionsModel, TargetTypesModel, TargetsModel


class Countries(graphene.ObjectType):
    class Meta:
        model = CountriesModel
        interfaces = (graphene.relay.Node,)


class Cities(graphene.ObjectType):
    class Meta:
        model = CitiesModel
        interfaces = (graphene.relay.Node,)


class Missions(graphene.ObjectType):
    class Meta:
        model = MissionsModel
        interfaces = (graphene.relay.Node,)


class TargetTypes(graphene.ObjectType):
    class Meta:
        model = TargetTypesModel
        interfaces = (graphene.relay.Node,)


class Targets(graphene.ObjectType):
    class Meta:
        model = TargetsModel
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    missions_by_id = graphene.Field(Missions, mission_id=graphene.Int(required=True))
    missions_by_age_range = graphene.List(Missions, min_date=graphene.Date(required=True), max_date=graphene.Date(required=True))
    missions_by_country = graphene.Field(Missions, country_name=graphene.String(required=True))
    missions_by_target_industry = graphene.Field(Missions, target_industry=graphene.String(required=True))


    def resolve_missions_by_id(self, info, mission_id):
        return db_session.query(MissionsModel).get(mission_id)

    def resolve_missions_by_age_range(self, info, min_date, max_date):
        return db_session.query(MissionsModel).filter(MissionsModel.mission_date.between(min_date, max_date)).all()

    def resolve_missions_by_country(self, info, country_name):
        return db_session.query(MissionsModel).filter(MissionsModel.target.city.countries.country_name == country_name).all()

    def resolve_missions_by_target_industry(self, info, target_industry):
        return db_session.query(MissionsModel).filter(MissionsModel.target.target_industry == target_industry).all()


class CreateMission(graphene.Mutation):
    class Arguments:
        mission_date = graphene.Date(required=True)
        airborne_aircraft = graphene.Float()
        attacking_aircraft = graphene.Float()
        bombing_aircraft = graphene.Float()
        aircraft_returned = graphene.Float()
        aircraft_failed = graphene.Float()
        aircraft_damaged = graphene.Float()
        aircraft_lost = graphene.Float()

    mission = graphene.Field(Missions)

    def mutate(self, info, mission_date, airborne_aircraft=None, attacking_aircraft=None,
               bombing_aircraft=None, aircraft_returned=None, aircraft_failed=None,
               aircraft_damaged=None, aircraft_lost=None):
        mission = MissionsModel(
            mission_date=mission_date,
            airborne_aircraft=airborne_aircraft,
            attacking_aircraft=attacking_aircraft,
            bombing_aircraft=bombing_aircraft,
            aircraft_returned=aircraft_returned,
            aircraft_failed=aircraft_failed,
            aircraft_damaged=aircraft_damaged,
            aircraft_lost=aircraft_lost
        )
        db_session.add(mission)
        db_session.commit()
        return CreateMission(mission=mission)


class CreateTarget(graphene.Mutation):
    class Arguments:
        mission_id = graphene.Int(required=True)
        target_industry = graphene.String(required=True)
        target_priority = graphene.Int()
        city_id = graphene.Int(required=True)
        target_type_id = graphene.Int(required=True)

    target = graphene.Field(Targets)

    def mutate(self, info, mission_id, target_industry, target_priority=None, city_id=None, target_type_id=None):
        target = TargetsModel(
            mission_id=mission_id,
            target_industry=target_industry,
            target_priority=target_priority,
            city_id=city_id,
            target_type_id=target_type_id
        )
        db_session.add(target)
        db_session.commit()
        return CreateTarget(target=target)


class AddAttackResult(graphene.Mutation):
    class Arguments:
        mission_id = graphene.Int(required=True)
        returned_aircraft = graphene.Float(required=True)
        failed_aircraft = graphene.Float(required=True)
        damaged_aircraft = graphene.Float(required=True)
        lost_aircraft = graphene.Float(required=True)
        damage_assessment = graphene.String(required=True)

    mission = graphene.Field(Missions)

    def mutate(self, info, mission_id, returned_aircraft, failed_aircraft, damaged_aircraft, lost_aircraft, damage_assessment):
        mission = db_session.query(MissionsModel).filter(MissionsModel.mission_id == mission_id).first()
        if mission:
            mission.aircraft_returned = returned_aircraft
            mission.aircraft_failed = failed_aircraft
            mission.aircraft_damaged = damaged_aircraft
            mission.aircraft_lost = lost_aircraft
            mission.damage_assessment = damage_assessment
            db_session.commit()
            return AddAttackResult(mission=mission)
        return None


class UpdateAttackResult(graphene.Mutation):
    class Arguments:
        mission_id = graphene.Int(required=True)
        returned_aircraft = graphene.Float()
        failed_aircraft = graphene.Float()
        damaged_aircraft = graphene.Float()
        lost_aircraft = graphene.Float()
        damage_assessment = graphene.String()

    mission = graphene.Field(Missions)

    def mutate(self, info, mission_id, returned_aircraft=None, failed_aircraft=None,
               damaged_aircraft=None, lost_aircraft=None, damage_assessment=None):
        mission = db_session.query(MissionsModel).filter(MissionsModel.mission_id == mission_id).first()
        if mission:
            if returned_aircraft is not None:
                mission.aircraft_returned = returned_aircraft
            if failed_aircraft is not None:
                mission.aircraft_failed = failed_aircraft
            if damaged_aircraft is not None:
                mission.aircraft_damaged = damaged_aircraft
            if lost_aircraft is not None:
                mission.aircraft_lost = lost_aircraft
            if damage_assessment is not None:
                mission.damage_assessment = damage_assessment
            db_session.commit()
            return UpdateAttackResult(mission=mission)
        return None


class DeleteMission(graphene.Mutation):
    class Arguments:
        mission_id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, mission_id):
        mission = db_session.query(MissionsModel).filter(MissionsModel.mission_id == mission_id).first()
        if mission:
            db_session.delete(mission)
            db_session.commit()
            return DeleteMission(success=True)
        return DeleteMission(success=False)


class Mutation(graphene.ObjectType):
    create_mission = CreateMission.Field()
    create_target = CreateTarget.Field()
    add_attack_result = AddAttackResult.Field()
    update_attack_result = UpdateAttackResult.Field()
    delete_mission = DeleteMission.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)



