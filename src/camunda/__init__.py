import camunda.message
import camunda.process_definition
import camunda.process_instance
import camunda.task
from camunda.context import _use_api


def version() -> str:
    api = _use_api()
    result = api.get("/version")
    return result['version']
