from litestar.router import Router

from .armor import ArmorController
from .character_class import ClassController
from .character_subclass import SubclassController
from .class_feature import ClassFeatureController
from .material import MaterialController

router = Router(
    path="/api/v1",
    route_handlers=[
        ArmorController,
        ClassController,
        SubclassController,
        ClassFeatureController,
        MaterialController,
    ],
)
