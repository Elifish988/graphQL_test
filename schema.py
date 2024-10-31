import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from db.database import db_session
from db.models import CountriesModel, CitiesModel, MissionsModel, TargetTypesModel, TargetsModel


class Countries(SQLAlchemyObjectType):
    class Meta:
        model = CountriesModel
        interfaces = (graphene.relay.Node,)


class Cities(SQLAlchemyObjectType):
    class Meta:
        model = CitiesModel
        interfaces = (graphene.relay.Node,)


class Missions(SQLAlchemyObjectType):
    class Meta:
        model = MissionsModel
        interfaces = (graphene.relay.Node,)


class TargetTypes(SQLAlchemyObjectType):
    class Meta:
        model = TargetTypesModel
        interfaces = (graphene.relay.Node,)


class Targets(SQLAlchemyObjectType):
    class Meta:
        model = TargetsModel
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    City_by_id = graphene.Field(Cities, id=graphene.Int(required=True))


    def resolve_user_by_id(self, info, id):
        return db_session.query(CitiesModel).get(id)





schema = graphene.Schema(query=Query)