import urllib.parse
from pathlib import Path

from datamodel_code_generator import InputFileType, generate

generate(
    input_=urllib.parse.urlparse("https://start.camunda.com/openapi.json"),
    input_file_type=InputFileType.OpenAPI,
    output=Path("./src/camunda/models.py"),
    allow_population_by_field_name=True,
    snake_case_field=True,
    use_generic_container_types=True,
    use_schema_description=True,
    reuse_model=True
)
