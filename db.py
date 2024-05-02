# Copyright (c) 2023-2024 Westfall Inc.
#
# This file is part of Windcarver.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, and can be found in the file NOTICE inside this
# git repository.
#
# This program is distributed in the hope that it will be useful
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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

    Model_Repo = db.Table('model_repo', metadata,
              db.Column('id', db.Integer(), primary_key=True, unique=True),
              db.Column('default_branch', db.String(255), nullable=False),
              db.Column('full_name', db.String(), nullable=False),
    )

    Commits = db.Table('commits', metadata,
              db.Column('id', db.Integer(), primary_key=True, unique=True),
              db.Column('ref', db.String(255), nullable=False), # branch
              db.Column('commit', db.String(255), nullable=False), # commit hash
              db.Column('processed', db.Boolean(), nullable=False),
              db.Column('date', db.DateTime(), nullable=False) # commit date
    )

    Models = db.Table('models', metadata,
              db.Column('id', db.Integer(), primary_key=True, unique=True),
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
              db.Column('id', db.Integer(), primary_key=True, unique=True),
              db.Column("commit_id", db.Integer(), db.ForeignKey("commits.id"), nullable=False),
              db.Column('element_id', db.String(36), nullable=False),
              db.Column('element_text', db.String(), nullable=False),
              db.Column('element_name', db.String(255), nullable=False),
    )
    Models_Elements = db.Table('models_elements', metadata,
              db.Column('id', db.Integer(), primary_key=True, unique=True),
              db.Column("model_id", db.Integer(), db.ForeignKey("models.id"), nullable=False),
              db.Column("element_id", db.Integer(), db.ForeignKey("elements.id"), nullable=False),
              db.Column("commit_id", db.Integer(), db.ForeignKey("commits.id"), nullable=False),
    )
    Requirements = db.Table('requirements', metadata,
              db.Column('id', db.Integer(), primary_key=True, unique=True),
              db.Column("commit_id", db.Integer(), db.ForeignKey("commits.id"), nullable=False),
              db.Column('declaredName', db.String(255), nullable=True),
              db.Column('shortName', db.String(255), nullable=True),
              db.Column('qualifiedName', db.String(255), nullable=True),
              db.Column("element_id", db.Integer(), db.ForeignKey("elements.id"), nullable=False),
    )

    Verifications = db.Table('verifications', metadata,
              db.Column('id', db.Integer(), primary_key=True, unique=True),
              db.Column("commit_id", db.Integer(), db.ForeignKey("commits.id"), nullable=False),
              db.Column("element_id", db.Integer(), db.ForeignKey("elements.id"), nullable=False),
              db.Column("requirement_id", db.Integer(), db.ForeignKey("requirements.id"), nullable=False),
              db.Column("verified", db.Boolean(), default=False),
              db.Column("attempted", db.Boolean(), default=False)
    )
    Actions = db.Table('actions', metadata,
        db.Column('id', db.Integer(), primary_key=True, unique=True),
        db.Column("commit_id", db.Integer(), db.ForeignKey("commits.id"), nullable=False),
        db.Column("element_id", db.Integer(), db.ForeignKey("elements.id"), nullable=False),
        db.Column("verifications_id", db.Integer(), db.ForeignKey("verifications.id"), nullable=False),
        db.Column('shortName', db.String(255), default=None),
        db.Column('declaredName', db.String(255), nullable=False),
        db.Column('qualifiedName', db.String(), nullable=False),
        db.Column('harbor', db.String(), nullable=True),
        db.Column('artifacts', db.String(), nullable=True),
        db.Column('variables', db.String(), nullable=True),
        db.Column('valid', db.Boolean(), default=False),
        db.Column('dependency', db.Integer(), nullable=True, default=None)
    )
    Containers = db.Table('containers', metadata,
              db.Column('id', db.Integer(), primary_key=True, unique=True),
              db.Column("resource_url", db.String(255), nullable=False),
              db.Column("host", db.String(255), nullable=False),
              db.Column('project', db.String(255), nullable=False),
              db.Column('project_id', db.Integer(), nullable=True),
              db.Column('image', db.String(255), nullable=False),
              db.Column('image_id', db.Integer(), nullable=True),
              db.Column('tag', db.String(255), nullable=False),
    )
    Container_Commits = db.Table('container_commits', metadata,
              db.Column('id', db.Integer(), primary_key=True, unique=True),
              db.Column("containers_id", db.Integer(), db.ForeignKey("containers.id"), nullable=False),
              db.Column('digest', db.String(64), nullable=False),
              db.Column('date', db.DateTime(), nullable=False),
              db.Column('cmd', db.String(), nullable=True),
              db.Column('working_dir', db.String(255), nullable=True)
    )

    Artifacts = db.Table('artifacts', metadata,
              db.Column('id', db.Integer(), primary_key=True),
              db.Column('full_name', db.String(255), nullable=False), # artifact repo path
              db.Column('commit_url', db.String(), nullable=False), # artifact repo path
              db.Column('default_branch', db.String(255), nullable=False),
    )

    Artifacts_Commits = db.Table('artifact_commits', metadata,
              db.Column('id', db.Integer(), primary_key=True),
              db.Column("artifacts_id", db.Integer(), db.ForeignKey("artifacts.id"), nullable=False),
              db.Column('ref', db.String(255), nullable=False), # branch
              db.Column('commit', db.String(255), nullable=False), # commit hash
              db.Column('date', db.DateTime(), nullable=False) # commit date
    )

    Thread_Executions = db.Table('thread_executions', metadata,
        db.Column('id', db.Integer(), primary_key=True, unique=True),
        db.Column('name', db.String(255), nullable=False),
        db.Column("action_id", db.Integer(), db.ForeignKey(Actions.c.id), nullable=False),
        db.Column("model_commit_id", db.Integer(), db.ForeignKey(Commits.c.id), nullable=False),
        db.Column("container_commit_id", db.Integer(), db.ForeignKey(Container_Commits.c.id), nullable=False),
        db.Column("artifact_commit_id", db.Integer(), db.ForeignKey(Artifacts_Commits.c.id), nullable=False),
        db.Column("source", db.String(255), nullable=False),
        db.Column("state", db.String(255), nullable=False),
        db.Column('date_created', db.DateTime(), nullable=False),
        db.Column('date_updated', db.DateTime(), nullable=False),
    )
    metadata.create_all(engine)
