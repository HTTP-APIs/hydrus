from flask_socketio import Namespace, emit
from hydrus.data.crud import get_modification_table_diff, get_last_modification_job_id


class SyncNamespace(Namespace):

    def __init__(self, namespace, db_session):
        Namespace.__init__(self, namespace=namespace)
        self.db_session = db_session

    def on_connect(self):
        print('A client connected')
        emit('connect', {'last_job_id': get_last_modification_job_id(self.db_session)})

    def on_disconnect(self):
        print('A client disconnected')

    def on_reconnect(self):
        print('A client reconnected.')
        emit('connect', {'last_job_id': get_last_modification_job_id(self.db_session)})

    def on_get_modification_table_diff(self, data):
        """Get modification table diff and emit it to the client.
        :param data: Dict with 'agent_job_id' key.
        """
        if 'agent_job_id' in data:
            agent_job_id = data['agent_job_id']
            modification_table_diff = get_modification_table_diff(self.db_session,
                                                                  agent_job_id)
        else:
            modification_table_diff = get_modification_table_diff(self.db_session)
        emit('modification_table_diff', modification_table_diff)
