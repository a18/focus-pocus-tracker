import os
import sqlite3

from loguru import logger


class FpDatabase:
    """Focus-Pocus database for storing events."""
    def __init__(self, db_path: str):
        """
        Creates instance of Focus-Pocus database.
        Args:
            db_path (str): path to DB file (if not exists, will be created at `connect` phase).
        """
        self.db_path = db_path
        self.conn = None

    def connect(self):
        # Check dir
        db_dir = os.path.dirname(self.db_path)
        assert os.path.isdir(db_dir), f"Dir not found: {db_dir=}, {os.getcwd()=}"

        # Open connection (the file could be absent at first start)
        if not os.path.exists(self.db_path):
            logger.info(f"The db_path is absent -> sqlite db will be created. db_path={self.db_path}, {os.getcwd()=}")
        else:
            logger.info(f"The db_path found -> use it for connecting. db_path={self.db_path}, {os.getcwd()=}")
        self.conn = sqlite3.connect(self.db_path)

        # Create tables if required
        self._create_tables()

        logger.info("... success")

    def _create_tables(self):
        query = '''
        CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            event_type TEXT,
            details TEXT
        )
        '''
        self.conn.execute(query)
        self.conn.commit()

    def insert_log(self, timestamp: str, event_type: str, details: str):
        query = 'INSERT INTO activity_logs (timestamp, event_type, details) VALUES (?, ?, ?)'
        self.conn.execute(query, (timestamp, event_type, details))
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()


# Code for direct DB testing
# if __name__ == "__main__":
#     db = FpDatabase("activity.db")
#     db.connect()
#     db.insert_log("test_event", "Test event details")
#     db.close()
