from threading import Timer
from hydrus.data.db_models import Modification
from sqlalchemy.orm import scoped_session


def remove_stale_modification_records(session: scoped_session,
                                      stale_records_removal_interval: int=900):
    """
    Remove modification records which are older than last 1000 records.
    :param session: sqlalchemy session.
    :param stale_records_removal_interval: Interval time to run the removal job.
    """
    timer = Timer(stale_records_removal_interval,
                  remove_stale_modification_records, [session])
    timer.daemon = True
    timer.start()
    # Get all valid records.
    valid_records = session.query(Modification).order_by(
        Modification.job_id.desc()).limit(1000).all()
    # If number of returned valid records is less than set limit then
    # there is nothing to clean up.
    if len(valid_records) < 1000:
        return
    else:
        # Get the job_id of last (oldest) valid record.
        job_id_of_last_valid_record = valid_records[-1].job_id
        # Get all records which are older than the oldest valid record.
        stale_records = session.query(Modification).filter(
            Modification.job_id < job_id_of_last_valid_record).all()
        for record in stale_records:
            session.delete(record)
        session.commit()
    session.remove()
