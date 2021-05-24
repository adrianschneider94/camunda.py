import camunda.models.generated as generated
import camunda.models.variables as custom

generated.VariableValueDto = custom.VariableValueDto

del generated, custom

from .generated import *
from .variables import *
