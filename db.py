import os
import sqlalchemy as db
from sqlalchemy import inspect

SQLDEF = "localhost:5432"
SQLHOST = os.environ.get("SQLHOST",SQLDEF)

def connect():
    db_type = "postgresql"
    user = "postgres"
    passwd = "mysecretpassword"
    address = SQLHOST
    db_name = "sysml2"

    address = db_type+"://"+user+":"+passwd+"@"+address+"/"+db_name
    engine = db.create_engine(address)
    conn = engine.connect()

    return conn, engine

def make_tables(engine):
    metadata = db.MetaData()
    if not 'models' in metadata_obj.sorted_tables():
        Models = db.Table('models', metadata,
                  db.Column('id', db.Integer(), primary_key=True),
                  db.Column('name', db.String(255), nullable=False), #notebook id
                  db.Column('ref', db.String(255), nullable=False), # branch
                  db.Column('commit', db.String(255), nullable=False), # commit hash
                  db.Column('nbhash', db.String(255), nullable=False), # notebook path hash
                  db.Column('hash', db.String(255), nullable=False), # model hash
                  db.Column('model', db.String(), nullable=False), # model text
                  db.Column('date', db.DateTime(), nullable=False) # commit date
        )
        metadata.create_all(engine)

if __name__ == '__main__':
    _, engine = connect()

    inspector = inspect(engine)
    schemas = inspector.get_schema_names()

    for schema in schemas:
        print("schema: %s" % schema)
        for table_name in inspector.get_table_names(schema=schema):
            print('Table: %s' % table_name)
            for column in inspector.get_columns(table_name, schema=schema):
                print("Column: %s" % column)

    metadata = db.MetaData()

    Commits = db.Table('commits', metadata,
              db.Column('id', db.Integer(), primary_key=True),
              db.Column('ref', db.String(255), nullable=False), # branch
              db.Column('commit', db.String(255), nullable=False), # commit hash
              db.Column('date', db.DateTime(), nullable=False) # commit date
    )
    Models = db.Table('models', metadata,
              db.Column('id', db.Integer(), primary_key=True),
              db.Column("commit_id", db.Integer(), db.ForeignKey("commits.id"), nullable=False),
              db.Column('nb_id', db.String(36), nullable=False), #notebook id
              db.Column('execution_order', db.Integer(), nullable=False),
              db.Column('model_text', db.String(), nullable=False),
              db.Column('model_hash', db.String(40), nullable=False),
              db.Column('path_text', db.String(255), nullable=False),
              db.Column('path_hash', db.String(40), nullable=False),
              db.Column('element_name', db.String(255), nullable=False),
    )
    Elements = db.Table('elements', metadata,
              db.Column('id', db.Integer(), primary_key=True),
              db.Column("commit_id", db.Integer(), db.ForeignKey("commits.id"), nullable=False),
              db.Column('element_id', db.String(36), nullable=False),
              db.Column('element_text', db.String(), nullable=False),
              db.Column('element_name', db.String(255), nullable=False),
    )
    Models_Elements = db.Table('models_elements', metadata,
              db.Column('id', db.Integer(), primary_key=True),
              db.Column("model_id", db.Integer(), db.ForeignKey("models.id"), nullable=False),
              db.Column("element_id", db.Integer(), db.ForeignKey("elements.id"), nullable=False),
    )
    Requirements = db.Table('requirements', metadata,
              db.Column('id', db.Integer(), primary_key=True),
              db.Column('name', db.String(255), nullable=False), # branch
              db.Column("element_id", db.Integer(), db.ForeignKey("elements.id"), nullable=False),
    )
    Verifications = db.Table('verifications', metadata,
              db.Column('id', db.Integer(), primary_key=True),
              db.Column("element_id", db.Integer(), db.ForeignKey("elements.id"), nullable=False),
              db.Column("requirement_id", db.Integer(), db.ForeignKey("requirements.id"), nullable=False),
    )
    Actions = db.Table('actions', metadata,
              db.Column('id', db.Integer(), primary_key=True),
              db.Column("element_id", db.Integer(), db.ForeignKey("elements.id"), nullable=False),
              db.Column("verifications_id", db.Integer(), db.ForeignKey("verifications.id"), nullable=False),
              db.Column('declaredName', db.String(255), nullable=False),
              db.Column('qualifiedName', db.String(), nullable=False),
              db.Column('harbor', db.String(), nullable=True),
              db.Column('artifacts', db.String(), nullable=True),
              db.Column('variables', db.String(), nullable=True),
    )
    #Verifications_Actions = db.Table('verifications_actions', metadata,
    #          db.Column('id', db.Integer(), primary_key=True),
    #          db.Column("verifications_id", db.Integer(), db.ForeignKey("verifications.id"), nullable=False),
    #          db.Column("actions_id", db.Integer(), db.ForeignKey("actions.id"), nullable=False),
    #)

    Containers = db.Table('containers', metadata,
              db.Column('id', db.Integer(), primary_key=True),
              db.Column("resource_url", db.String(255), nullable=False),
              db.Column("host", db.String(255), nullable=False),
              db.Column('project', db.String(255), nullable=False),
              db.Column('image', db.String(255), nullable=False),
              db.Column('tag', db.String(255), nullable=False),
              db.Column('digest', db.String(64), nullable=False),
              db.Column('date', db.DateTime(), nullable=False),
    )

    Artifacts = db.Table('artifacts', metadata,
              db.Column('id', db.Integer(), primary_key=True),
              db.Column('full_name', db.String(255), nullable=False), # artifact repo path
              db.Column('commit_url', db.String(), nullable=False), # artifact repo path
              db.Column('ref', db.String(255), nullable=False), # branch
              db.Column('commit', db.String(255), nullable=False), # commit hash
              db.Column('date', db.DateTime(), nullable=False) # commit date
    )
    metadata.create_all(engine)
