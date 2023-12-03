from datetime import datetime

from sqlalchemy import Table, Column, String, Integer, MetaData, Boolean, TIMESTAMP

metadata = MetaData()

task = Table(
    "task",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("task_name", String, nullable=False),
    Column("status", Boolean, nullable=False, default=False),
    Column("created_at", TIMESTAMP, default=datetime.utcnow())
)
