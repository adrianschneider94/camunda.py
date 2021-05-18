from typing import Mapping, Sequence

from camunda.context import _use_api
from camunda.models import PatchVariablesDto, ProcessInstanceDto, ProcessInstanceQueryDto, VariableValueDto

__all__ = [
    "get", "get_list"
]


def get(id: str):
    api = _use_api()
    result = api.get(f"/process-instance/{id}")
    return ProcessInstanceDto.parse_obj(result)


def get_list(data: ProcessInstanceQueryDto = ProcessInstanceQueryDto()) -> Sequence[ProcessInstanceDto]:
    api = _use_api()
    result = api.post("/process-instance", data=data.dict())
    return [ProcessInstanceDto.parse_obj(item) for item in result]


def update_variables(id: str, data: PatchVariablesDto):
    api = _use_api()
    api.post(f"/process-instance/{id}/variables", data=data.dict())


def get_variables(id: str) -> Mapping[str, VariableValueDto]:
    api = _use_api()
    result = api.get(f"/process-instance/{id}/variables")
    return {key: VariableValueDto.parse_obj(value) for key, value in result.items()}
