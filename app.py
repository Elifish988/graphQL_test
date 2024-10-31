from flask import Flask
from flask_graphql import GraphQLView
from db.database import connection_url, db_session
from schema import schema
import psycopg2


app = Flask(__name__)
app.debug = True

app.config["SQLALCHEMY_DATABASE_URI"] = connection_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False




app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)




if __name__ == "__main__":
    app.run()
