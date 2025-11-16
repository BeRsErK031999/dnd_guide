from litestar.router import Router

from .armor import ArmorController
from .character_class import ClassController
from .character_subclass import SubclassController
from .class_feature import ClassFeatureController
from .class_level import ClassLevelController
from .coin import get_piece_types
from .creature_size import CreatureSizeController
from .creature_type import CreatureTypeController
from .damage_type import get_damage_types
from .dice import get_dice_types
from .feat import FeatController
from .game_time import get_game_time_units
from .length import get_length_units
from .material import MaterialController
from .material_component import MaterialComponentController
from .modifier import get_modifiers
from .race import RaceController
from .skill import get_skills
from .source import SourceController
from .spell import SpellController
from .subclass_feature import SubclassFeatureController
from .subrace import SubraceController
from .tool import ToolController
from .weapon import WeaponController
from .weapon_kind import WeaponKindController
from .weapon_property import WeaponPropertyController
from .weight import get_weight_units

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
        SubraceController,
        ToolController,
        WeaponKindController,
        WeaponPropertyController,
        WeaponController,
        get_piece_types,
        get_dice_types,
        get_game_time_units,
        get_length_units,
        get_weight_units,
        get_damage_types,
        get_modifiers,
        get_skills,
    ],
)
