from camunda.context import use_api
from camunda.models import ProcessDefinitionDiagramDto, ProcessDefinitionDto


def get(id: str) -> ProcessDefinitionDto:
    api = use_api()
    result = api.get(f"/process-definition/{id}")
    return ProcessDefinitionDto.parse_obj(result)


def get_xml(id: str = None, key: str = None, tenant_id: str = None) -> ProcessDefinitionDiagramDto:
    if not id or key:
        raise ValueError("You need to provide either id or key")

    api = use_api()

    if id:
        path = f"/process-definition/{id}/xml"
    elif key and tenant_id:
        path = f"/process-definition/key/{key}/tenant-id/{tenant_id}/xml"
    else:
        path = f"/process-definition/key/{key}/xml"

    result = api.get(path)
    return ProcessDefinitionDiagramDto.parse_obj(result)
