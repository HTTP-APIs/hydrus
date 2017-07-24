"""."""
from hydrus.app import app, set_session
from hydrus.data import doc_parse
from hydrus.metadata.doc_gen import doc_gen
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hydrus.data.db_models import Base
import pdb

print("Create the db...")
new_engine = create_engine('sqlite:///sqlalchemy_example.db')
Base.metadata.create_all(new_engine)
temp_session = sessionmaker(bind=new_engine)()
doc = doc_gen("api", "http://localhost:8080/")
test_classes = doc_parse.get_classes(doc.generate())
test_properties = doc_parse.get_all_properties(test_classes)
doc_parse.insert_classes(test_classes, temp_session)
doc_parse.insert_properties(test_properties, temp_session)
print("Update connector on app")

# pdb.set_trace()
with set_doc(app, api_doc):
    with set_session(app, temp_session):
        app.run(host='127.0.0.1', debug=True, port=8080)
