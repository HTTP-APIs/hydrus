"""Initialize database for hydrus."""
# from hydrus.metadata.doc import doc
from hydrus.metadata.doc_gen import doc_gen
from hydrus.data.doc_parse import get_classes, insert_classes, get_all_properties, insert_properties
from hydrus.data.db_models import Base, engine
from sqlalchemy.orm import sessionmaker


def main():
    """Initialize the drone database."""
    # Drop database if exists and create a new one.
    print("Droping database if exist")
    Base.metadata.drop_all(engine)

    print("Creating models....")
    Base.metadata.create_all(engine)
    print("Done")

    # Parse and insert classes to DB

    Session = sessionmaker(bind=engine)
    session = Session()

    doc = doc_gen("dummy", "dummy")

    doc_classes = get_classes(doc.generate())
    doc_properties = get_all_properties(doc_classes)

    insert_classes(doc_classes, session=session)
    print("Classes inserted successfully.")

    insert_properties(doc_properties, session=session)
    print("Properties inserted successfully.")

    return None


if __name__ == "__main__":
    main()
