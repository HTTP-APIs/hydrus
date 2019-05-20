
Alembic - Database Migration Tool
===================

[Alembic](https://alembic.sqlalchemy.org/en/latest/) is a lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python.

-----------------

First make sure you set up hydrus as the [instructions here](https://github.com/HTTP-APIs/hydrus/blob/master/README.md).

  

## Running a basic demo migration

With the default hydrus clone run it with a sqlite database:

    hydrus serve --dburl sqlite:///hydrus/data/database.db

### Point to your DB Url( ):

If following this tutorial **the DB Url is already set accordingly** . *If not* go to **hydrus/migration/alembic.ini** and edit pointing to your DB Address:

    sqlalchemy.url = sqlite:///database.db

### Create migration script
Navigate to **.../hydrus/data** first, then run:

    alembic revision -m "creating obs. table and adding prop. column"
    
You should get something like this:

    Generating .../hydrus/hydrus/data/migrations/versions/f1359b4901c9__creating_obs_table_and_adding_prop_.py ... done

  That means it created an default migration script under the revision number of f1359b4901c9. Now it's time to write the wanted changes to the DB.

### Adjust migration script  

In our example, we will be creating a new table and adding a column, head over to the new created file by the previous command under **.../hydrus/hydrus/data/migrations/versions/...** And add the following lines:
    
	def upgrade():
		op.create_table(
			'observations',
			sa.Column('id', sa.Integer, primary_key=True),
			sa.Column('drone_name', sa.String(50), nullable=False),
			sa.Column('observations', sa.Unicode(200)),
		)
		op.add_column('property', sa.Column('description', sa.String(20),
											server_default="Prop. Description"))


	def downgrade():
		op.drop_table('observations')
		op.drop_column('property', 'description')

**More information** on operations available to your migration here: https://alembic.sqlalchemy.org/en/latest/ops.html

  

### Run migration script

To run the migration script run:

  

    alembic upgrade head

  

To go back with your migration run:

  

    alembic downgrade head

  

To go to a specific revision you can run, for example:

  

     alembic upgrade f1359b4901c9

*Obs.: If using SQLite you can just use https://sqliteonline.com/ to check the changes.*

##  Troubleshoot and updates

There's always an updated full getting start tutorial on Alembic here: https://alembic.sqlalchemy.org/en/latest/tutorial.html

  
 *Please note that the above described is a very basic migration process, head over to the official Alembic page for all the possibilities you have:* https://alembic.sqlalchemy.org/

