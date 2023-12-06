from sqlalchemy import ResultProxy


def get_task_dict(result: ResultProxy):
    task_dict = [{
        "id": result[0],
        "task_name": result[1],
        "status": result[2],
        "created_at": result[3]
    }]