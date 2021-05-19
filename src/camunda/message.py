from typing import Optional

from camunda.context import use_api
from camunda.models import CorrelationMessageDto, MessageCorrelationResultWithVariableDto


def correlate(data: CorrelationMessageDto = CorrelationMessageDto()) -> Optional[
    MessageCorrelationResultWithVariableDto]:
    api = use_api()
    result = api.post("/message", data=data.dict(exclude_unset=True, by_alias=True))

    if result:
        return MessageCorrelationResultWithVariableDto.parse_obj(result)
