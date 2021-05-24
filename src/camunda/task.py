import json
import uuid
from datetime import timedelta
from typing import List, Mapping, Optional
from uuid import UUID

from camunda.context import use_api
from camunda.models import CompleteTaskDto, IdentityLinkDto, TaskDto, TaskQueryDto, VariableValueDto

TASK_SET_UUID = uuid.UUID("3a8804d3-6111-42b3-920c-405a251c1d44")


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, timedelta):
            return obj.total_seconds()
        return json.JSONEncoder.default(self, obj)


def calculate_task_query_id(query: TaskQueryDto):
    return uuid.uuid5(TASK_SET_UUID, query.json(sort_keys=True, cls=Encoder))


def get_list(query: TaskQueryDto = TaskQueryDto()) -> List[TaskDto]:
    api = use_api()

    data = query.dict(exclude_unset=True, by_alias=True)
    result = api.post("/task", data=data)
    return [TaskDto.parse_obj(task) for task in result]


def get(id: str) -> TaskDto:
    api = use_api()
    result = api.get(f"/task/{id}")
    return TaskDto.parse_obj(result)


def complete(id: str, data: CompleteTaskDto = CompleteTaskDto()) -> Optional[Mapping[str, VariableValueDto]]:
    api = use_api()
    result = api.post(f"/task/{id}/complete", data=data.dict(exclude_unset=True, by_alias=True))
    if result:
        return {k: VariableValueDto.parse_obj(v) for k, v in result.items()}


def get_variables(id: str):
    api = use_api()
    result = api.get(f"/task/{id}/variables")
    return {k: VariableValueDto.parse_obj(v) for k, v in result.items()}


def claim(id: str, user_id: str):
    api = use_api()
    api.post(f"/task/{id}/claim", data={"userId": user_id})


def unclaim(id: str):
    api = use_api()
    api.post(f"/task/{id}/unclaim")


def set_assignee(id: str, user_id: str):
    api = use_api()
    api.post(f"/task/{id}/assignee", data={"userId": user_id})


def get_identity_links(id: str):
    api = use_api()
    result = api.get(f"/task/{id}/identity-links")
    return [IdentityLinkDto.parse_obj(item) for item in result]
