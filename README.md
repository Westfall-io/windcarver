# windcarver
WindstormDB Init

This will initialize a postgres database with the schema required to support
DigitalForge. If deployed to kubernetes, a port forward command:

`kubectl -n <namespace> portforward svc/<postgres service name> 5432:5432`

Running this db.py script will ask for username, password, and database name
and will create the tables required.
