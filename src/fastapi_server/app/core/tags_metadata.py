"""Define metadata for tags used in OpenAPI documentation."""
from typing import Optional

from app.db.models.base import Base
from app.models.base import BaseSchema


## ===== Tags MetaData Schema ===== ##
class ExternalDocs(BaseSchema):

    description: Optional[str] = None
    ulr: str
class MetaDataTag(BaseSchema):

    name: str
    description: Optional[str] = None
    external_docs: Optional[ExternalDocs] = None

    class COnfig:

        allow_population_by_field_name = True
        fields = {"external_docs":{"alias": "externalDocs"}}


## ===== Tags Metadata Definition ===== ##
parents_tag = MetaDataTag(
    name="parents",
    description="Example description for parent endpoints."
)

children_tag = MetaDataTag(
    name="children",
    description="Stuff that you would want to know about this endpoint."
)


metadata_tags = [parents_tag, children_tag]