from litestar.router import Router

from .armor import ArmorController
from .character_class import ClassController
from .character_subclass import SubclassController
from .class_feature import ClassFeatureController
from .class_level import ClassLevelController
from .creature_size import CreatureSizeController
from .creature_type import CreatureTypeController
from .feat import FeatController
from .material import MaterialController
from .material_component import MaterialComponentController
from .race import RaceController
from .source import SourceController
from .spell import SpellController
from .subclass_feature import SubclassFeatureController

router = Router(
    path="/api/v1",
    route_handlers=[
        ArmorController,
        ClassController,
        SubclassController,
        ClassFeatureController,
        ClassLevelController,
        CreatureSizeController,
        CreatureTypeController,
        FeatController,
        MaterialController,
        MaterialComponentController,
        RaceController,
        SourceController,
        SpellController,
        SubclassFeatureController,
    ],
)
