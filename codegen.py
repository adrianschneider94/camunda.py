import json
from pathlib import Path

import jsonpatch
import requests
from datamodel_code_generator import InputFileType, generate

# Retrieve OpenAPI schema
api = json.loads(requests.get("https://start.camunda.com/openapi.json").text)

# Apply patches
patches = [
    {
        'op':   'remove',
        'path': '/components/schemas/VariableValueDto/properties/value/type',
    },
    {
        'op':   'remove',
        'path': '/components/schemas/VariableValueDto/properties/valueInfo/type',
    }
]

patch = jsonpatch.JsonPatch(patches)
patched_api = patch.apply(api)

# Generate pydantic models
generate(
    input_=json.dumps(patched_api),
    input_file_type=InputFileType.OpenAPI,
    output=Path("./src/camunda/models.py"),
    allow_population_by_field_name=True,
    snake_case_field=True,
    use_generic_container_types=True,
    use_schema_description=True,
    reuse_model=True
)
