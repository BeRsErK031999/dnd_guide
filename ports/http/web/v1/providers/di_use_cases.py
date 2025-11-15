import di
from di import (
    ArmorUseCases,
    ClassFeatureUseCases,
    ClassLevelUseCases,
    ClassUseCases,
    CreatureSizeUseCases,
    CreatureTypeUseCases,
    FeatUseCases,
    MaterialComponentUseCases,
    MaterialUseCases,
    RaceUseCases,
    SourceUseCases,
    SpellUseCases,
    SubclassFeatureUseCases,
    SubclassUseCases,
    SubraceUseCases,
    ToolUseCases,
    WeaponKindUseCases,
    WeaponPropertyUseCases,
    WeaponUseCases,
)

__all__ = [
    "ArmorUseCases",
    "ClassFeatureUseCases",
    "ClassLevelUseCases",
    "ClassUseCases",
    "CreatureSizeUseCases",
    "CreatureTypeUseCases",
    "FeatUseCases",
    "MaterialComponentUseCases",
    "MaterialUseCases",
    "RaceUseCases",
    "SourceUseCases",
    "SpellUseCases",
    "SubclassFeatureUseCases",
    "SubclassUseCases",
    "SubraceUseCases",
    "ToolUseCases",
    "WeaponKindUseCases",
    "WeaponPropertyUseCases",
    "WeaponUseCases",
    "di_armor_use_cases",
    "di_class_use_cases",
    "di_subclass_use_cases",
    "di_class_feature_use_cases",
    "di_class_level_use_cases",
    "di_creature_size_use_cases",
    "di_creature_type_use_cases",
    "di_feat_use_cases",
    "di_material_use_cases",
    "di_material_component_use_cases",
    "di_race_use_cases",
    "di_source_use_cases",
    "di_spell_use_cases",
    "di_subclass_feature_use_cases",
    "di_subrace_use_cases",
    "di_tool_use_cases",
    "di_weapon_use_cases",
    "di_weapon_kind_use_cases",
    "di_weapon_property_use_cases",
]


def di_armor_use_cases() -> di.ArmorUseCases:
    return di.armor_use_cases


def di_class_use_cases() -> di.ClassUseCases:
    return di.class_use_cases


def di_subclass_use_cases() -> di.SubclassUseCases:
    return di.subclass_use_cases


def di_class_feature_use_cases() -> di.ClassFeatureUseCases:
    return di.class_feature_use_cases


def di_class_level_use_cases() -> di.ClassLevelUseCases:
    return di.class_level_use_cases


def di_creature_size_use_cases() -> di.CreatureSizeUseCases:
    return di.creature_size_use_cases


def di_creature_type_use_cases() -> di.CreatureTypeUseCases:
    return di.creature_type_use_cases


def di_feat_use_cases() -> di.FeatUseCases:
    return di.feat_use_cases


def di_material_use_cases() -> di.MaterialUseCases:
    return di.material_use_cases


def di_material_component_use_cases() -> di.MaterialComponentUseCases:
    return di.material_component_use_cases


def di_race_use_cases() -> di.RaceUseCases:
    return di.race_use_cases


def di_source_use_cases() -> di.SourceUseCases:
    return di.source_use_cases


def di_spell_use_cases() -> di.SpellUseCases:
    return di.spell_use_cases


def di_subclass_feature_use_cases() -> di.SubclassFeatureUseCases:
    return di.subclass_feature_use_cases


def di_subrace_use_cases() -> di.SubraceUseCases:
    return di.subrace_use_cases


def di_tool_use_cases() -> di.ToolUseCases:
    return di.tool_use_cases


def di_weapon_use_cases() -> di.WeaponUseCases:
    return di.weapon_use_cases


def di_weapon_kind_use_cases() -> di.WeaponKindUseCases:
    return di.weapon_kind_use_cases


def di_weapon_property_use_cases() -> di.WeaponPropertyUseCases:
    return di.weapon_property_use_cases
