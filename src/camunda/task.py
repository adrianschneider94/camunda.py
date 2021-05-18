from typing import List, Mapping, Optional

from camunda.context import _use_api
from camunda.models import CompleteTaskDto, TaskDto, TaskQueryDto, VariableValueDto


def get_list(query: TaskQueryDto = TaskQueryDto()) -> List[TaskDto]:
    api = _use_api()

    result = api.post("/task", data=query.dict())

    if result:
        return [TaskDto.parse_obj(task) for task in result]


def get(id: str) -> TaskDto:
    api = _use_api()
    result = api.get(f"/task/{id}")
    return TaskDto.parse_obj(result)


def complete(id: str, data: CompleteTaskDto = CompleteTaskDto()) -> Optional[Mapping[str, VariableValueDto]]:
    api = _use_api()
    result = api.post(f"/task/{id}/complete", data=data.dict())
    if result:
        return {k: VariableValueDto.parse_obj(v) for k, v in result.items()}


def get_variables(id: str):
    api = _use_api()
    result = api.get(f"/task/{id}/variables")
    return {k: VariableValueDto.parse_obj(v) for k, v in result.items()}


def claim(id: str, user_id: str):
    api = _use_api()
    api.post(f"/task/{id}/claim")


def unclaim(id: str):
    api = _use_api()
    api.post(f"/task/{id}/unclaim")


def set_assignee(id: str, user_id: str):
    api = _use_api()
    api.post(f"/task/{id}/assignee", data={"userId": user_id})
