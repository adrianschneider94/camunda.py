from typing import Optional

from camunda.context import _use_api
from camunda.models import CorrelationMessageDto, MessageCorrelationResultWithVariableDto


def correlate(data: CorrelationMessageDto = CorrelationMessageDto()) -> Optional[
    MessageCorrelationResultWithVariableDto]:
    api = _use_api()
    result = api.post("/message", data=data.dict())

    if result:
        return MessageCorrelationResultWithVariableDto.parse_obj(result)
