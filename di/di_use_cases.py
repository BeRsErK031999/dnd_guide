from adapters.repository import sql
from application.use_case import command, query
from config import config
from domain.armor import ArmorService
from domain.character_class import ClassService
from domain.character_subclass import SubclassService
from domain.class_feature import ClassFeatureService
from domain.class_level import ClassLevelService
from domain.feat import FeatService
from domain.material import MaterialService
from domain.material_component import MaterialComponentService
from domain.race import RaceService
from domain.source import SourceService
from domain.spell import SpellService
from domain.subclass_feature import SubclassFeatureService
from domain.subrace import SubraceService
from domain.tool import ToolService
from domain.weapon import WeaponService
from domain.weapon_kind import WeaponKindService
from domain.weapon_property import WeaponPropertyService

db_helper = sql.DBHelper(config.db_url)


# Repositories

user_repo = sql.SQLUserRepository(db_helper=db_helper)
armor_repo = sql.SQLArmorRepository(db_helper=db_helper)
character_class_repo = sql.SQLClassRepository(db_helper=db_helper)
character_subclass_repo = sql.SQLSubclassRepository(db_helper=db_helper)
class_feature_repo = sql.SQLClassFeatureRepository(db_helper=db_helper)
class_level_repo = sql.SQLClassLevelRepository(db_helper=db_helper)
feat_repo = sql.SQLFeatRepository(db_helper=db_helper)
material_repo = sql.SQLMaterialRepository(db_helper=db_helper)
material_component_repo = sql.SQLMaterialComponentRepository(db_helper=db_helper)
race_repo = sql.SQLRaceRepository(db_helper=db_helper)
source_repo = sql.SQLSourceRepository(db_helper=db_helper)
spell_repo = sql.SQLSpellRepository(db_helper=db_helper)
subclass_feature_repo = sql.SQLSubclassFeatureRepository(db_helper=db_helper)
subrace_repo = sql.SQLSubraceRepository(db_helper=db_helper)
tool_repo = sql.SQLToolRepository(db_helper=db_helper)
weapon_repo = sql.SQLWeaponRepository(db_helper=db_helper)
weapon_kind_repo = sql.SQLWeaponKindRepository(db_helper=db_helper)
weapon_property_repo = sql.SQLWeaponPropertyRepository(db_helper=db_helper)


# Domain services

armor_domain_service = ArmorService(armor_repo)
character_class_domain_service = ClassService(character_class_repo)
character_subclass_domain_service = SubclassService(character_subclass_repo)
class_feature_domain_service = ClassFeatureService(class_feature_repo)
class_level_domain_service = ClassLevelService(class_level_repo)
feat_domain_service = FeatService(feat_repo)
material_domain_service = MaterialService(material_repo)
material_component_domain_service = MaterialComponentService(material_component_repo)
race_domain_service = RaceService(race_repo)
source_domain_service = SourceService(source_repo)
spell_domain_service = SpellService(spell_repo)
subclass_feature_domain_service = SubclassFeatureService(subclass_feature_repo)
subrace_domain_service = SubraceService(subrace_repo)
tool_domain_service = ToolService(tool_repo)
weapon_domain_service = WeaponService(weapon_repo)
weapon_kind_domain_service = WeaponKindService(weapon_kind_repo)
weapon_property_domain_service = WeaponPropertyService(weapon_property_repo)


class ArmorUseCases:
    def __init__(self) -> None:
        self.create = command.armor.CreateArmorUseCase(
            armor_service=armor_domain_service,
            user_repository=user_repo,
            armor_repository=armor_repo,
            material_repository=material_repo,
        )
        self.update = command.armor.UpdateArmorUseCase(
            armor_service=armor_domain_service,
            user_repository=user_repo,
            armor_repository=armor_repo,
            material_repository=material_repo,
        )
        self.delete = command.armor.DeleteArmorUseCase(
            user_repository=user_repo,
            armor_repository=armor_repo,
        )
        self.get_one = query.armor.GetArmorUseCase(
            armor_repository=armor_repo,
        )
        self.get_all = query.armor.GetArmorsUseCase(
            armor_repository=armor_repo,
        )


class ClassUseCases:
    def __init__(self) -> None:
        self.create = command.character_class.CreateClassUseCase(
            class_service=character_class_domain_service,
            user_repository=user_repo,
            class_repository=character_class_repo,
            weapon_repository=weapon_repo,
            tool_repository=tool_repo,
            source_repository=source_repo,
        )
        self.update = command.character_class.UpdateClassUseCase(
            class_service=character_class_domain_service,
            user_repository=user_repo,
            class_repository=character_class_repo,
            weapon_repository=weapon_repo,
            tool_repository=tool_repo,
            source_repository=source_repo,
        )
        self.delete = command.character_class.DeleteClassUseCase(
            user_repository=user_repo,
            class_repository=character_class_repo,
        )
        self.get_one = query.character_class.GetClassUseCase(
            class_repository=character_class_repo,
        )
        self.get_all = query.character_class.GetClassesUseCase(
            class_repository=character_class_repo,
        )


class SubclassUseCases:
    def __init__(self) -> None:
        self.create = command.character_subclass.CreateSubclassUseCase(
            subclass_service=character_subclass_domain_service,
            user_repository=user_repo,
            class_repository=character_class_repo,
            subclass_repository=character_subclass_repo,
        )
        self.update = command.character_subclass.UpdateSubclassUseCase(
            subclass_service=character_subclass_domain_service,
            user_repository=user_repo,
            class_repository=character_class_repo,
            subclass_repository=character_subclass_repo,
        )
        self.delete = command.character_subclass.DeleteSubclassUseCase(
            user_repository=user_repo,
            subclass_repository=character_subclass_repo,
        )
        self.get_one = query.character_subclass.GetSubclassUseCase(
            subclass_repository=character_subclass_repo,
        )
        self.get_all = query.character_subclass.GetSubclassesUseCase(
            subclass_repository=character_subclass_repo,
        )


class ClassFeatureUseCases:
    def __init__(self) -> None:
        self.create = command.class_feature.CreateClassFeatureUseCase(
            feature_service=class_feature_domain_service,
            user_repository=user_repo,
            class_repository=character_class_repo,
            feature_repository=class_feature_repo,
        )
        self.update = command.class_feature.UpdateClassFeatureUseCase(
            feature_service=class_feature_domain_service,
            user_repository=user_repo,
            class_repository=character_class_repo,
            feature_repository=class_feature_repo,
        )
        self.delete = command.class_feature.DeleteClassFeatureUseCase(
            user_repository=user_repo,
            feature_repository=class_feature_repo,
        )
        self.get_one = query.class_feature.GetClassFeatureUseCase(
            feature_repository=class_feature_repo,
        )
        self.get_all = query.class_feature.GetClassFeaturesUseCase(
            feature_repository=class_feature_repo,
        )


class ClassLevelUseCases:
    def __init__(self) -> None:
        self.create = command.class_level.CreateClassLevelUseCase(
            class_level_service=class_level_domain_service,
            user_repository=user_repo,
            class_level_repository=class_level_repo,
            class_repository=character_class_repo,
        )
        self.update = command.class_level.UpdateClassLevelUseCase(
            class_level_service=class_level_domain_service,
            user_repository=user_repo,
            class_level_repository=class_level_repo,
            class_repository=character_class_repo,
        )
        self.delete = command.class_level.DeleteClassLevelUseCase(
            user_repository=user_repo,
            class_level_repository=class_level_repo,
        )
        self.get_one = query.class_level.GetClassLevelUseCase(
            class_level_repository=class_level_repo,
        )
        self.get_all = query.class_level.GetClassLevelsUseCase(
            class_level_repository=class_level_repo,
        )


class FeatUseCases:
    def __init__(self) -> None:
        self.create = command.feat.CreateFeatUseCase(
            feat_service=feat_domain_service,
            user_repository=user_repo,
            feat_repository=feat_repo,
        )
        self.update = command.feat.UpdateFeatUseCase(
            feat_service=feat_domain_service,
            user_repository=user_repo,
            feat_repository=feat_repo,
        )
        self.delete = command.feat.DeleteFeatUseCase(
            user_repository=user_repo,
            feat_repository=feat_repo,
        )
        self.get_one = query.feat.GetFeatUseCase(
            feat_repository=feat_repo,
        )
        self.get_all = query.feat.GetFeatsUseCase(
            feat_repository=feat_repo,
        )


class MaterialUseCases:
    def __init__(self) -> None:
        self.create = command.material.CreateMaterialUseCase(
            material_service=material_domain_service,
            user_repository=user_repo,
            material_repository=material_repo,
        )
        self.update = command.material.UpdateMaterialUseCase(
            material_service=material_domain_service,
            user_repository=user_repo,
            material_repository=material_repo,
        )
        self.delete = command.material.DeleteMaterialUseCase(
            user_repository=user_repo,
            material_repository=material_repo,
            armor_repository=armor_repo,
            weapon_repository=weapon_repo,
        )
        self.get_one = query.material.GetMaterialUseCase(
            material_repository=material_repo,
        )
        self.get_all = query.material.GetMaterialsUseCase(
            material_repository=material_repo,
        )


class MaterialComponentUseCases:
    def __init__(self) -> None:
        self.create = command.material_component.CreateMaterialComponentUseCase(
            material_service=material_component_domain_service,
            user_repository=user_repo,
            material_repository=material_component_repo,
        )
        self.update = command.material_component.UpdateMaterialComponentUseCase(
            material_service=material_component_domain_service,
            user_repository=user_repo,
            material_repository=material_component_repo,
        )
        self.delete = command.material_component.DeleteMaterialComponentUseCase(
            user_repository=user_repo,
            material_repository=material_component_repo,
            spell_repository=spell_repo,
        )
        self.get_one = query.material_component.GetMaterialComponentUseCase(
            material_repository=material_component_repo,
        )
        self.get_all = query.material_component.GetMaterialComponentsUseCase(
            material_repository=material_component_repo,
        )


class RaceUseCases:
    def __init__(self) -> None:
        self.create = command.race.CreateRaceUseCase(
            race_service=race_domain_service,
            user_repository=user_repo,
            race_repository=race_repo,
            source_repository=source_repo,
        )
        self.update = command.race.UpdateRaceUseCase(
            race_service=race_domain_service,
            user_repository=user_repo,
            race_repository=race_repo,
            source_repository=source_repo,
        )
        self.delete = command.race.DeleteRaceUseCase(
            user_repository=user_repo,
            race_repository=race_repo,
        )
        self.get_one = query.race.GetRaceUseCase(
            race_repository=race_repo,
        )
        self.get_all = query.race.GetRacesUseCase(
            race_repository=race_repo,
        )


class SourceUseCases:
    def __init__(self) -> None:
        self.create = command.source.CreateSourceUseCase(
            source_service=source_domain_service,
            user_repository=user_repo,
            source_repository=source_repo,
        )
        self.update = command.source.UpdateSourceUseCase(
            source_service=source_domain_service,
            user_repository=user_repo,
            source_repository=source_repo,
        )
        self.delete = command.source.DeleteSourceUseCase(
            user_repository=user_repo,
            source_repository=source_repo,
            class_repository=character_class_repo,
            race_repository=race_repo,
            spell_repository=spell_repo,
        )
        self.get_one = query.source.GetSourceUseCase(
            source_repository=source_repo,
        )
        self.get_all = query.source.GetSourcesUseCase(
            source_repository=source_repo,
        )


class SpellUseCases:
    def __init__(self) -> None:
        self.create = command.spell.CreateSpellUseCase(
            spell_service=spell_domain_service,
            user_repository=user_repo,
            spell_repository=spell_repo,
            class_repository=character_class_repo,
            subclass_repository=character_subclass_repo,
            source_repository=source_repo,
            material_component_repository=material_component_repo,
        )
        self.update = command.spell.UpdateSpellUseCase(
            spell_service=spell_domain_service,
            user_repository=user_repo,
            spell_repository=spell_repo,
            class_repository=character_class_repo,
            subclass_repository=character_subclass_repo,
            source_repository=source_repo,
            material_component_repository=material_component_repo,
        )
        self.delete = command.spell.DeleteSpellUseCase(
            user_repository=user_repo,
            spell_repository=spell_repo,
        )
        self.get_one = query.spell.GetSpellUseCase(
            spell_repository=spell_repo,
        )
        self.get_all = query.spell.GetSpellsUseCase(
            spell_repository=spell_repo,
        )


class SubclassFeatureUseCases:
    def __init__(self) -> None:
        self.create = command.subclass_feature.CreateSubclassFeatureUseCase(
            feature_service=subclass_feature_domain_service,
            user_repository=user_repo,
            subclass_repository=character_subclass_repo,
            feature_repository=subclass_feature_repo,
        )
        self.update = command.subclass_feature.UpdateSubclassFeatureUseCase(
            feature_service=subclass_feature_domain_service,
            user_repository=user_repo,
            subclass_repository=character_subclass_repo,
            feature_repository=subclass_feature_repo,
        )
        self.delete = command.subclass_feature.DeleteSubclassFeatureUseCase(
            user_repository=user_repo,
            feature_repository=subclass_feature_repo,
        )
        self.get_one = query.subclass_feature.GetSubclassFeatureUseCase(
            feature_repository=subclass_feature_repo,
        )
        self.get_all = query.subclass_feature.GetSubclassFeaturesUseCase(
            feature_repository=subclass_feature_repo,
        )


class SubraceUseCases:
    def __init__(self) -> None:
        self.create = command.subrace.CreateSubraceUseCase(
            subrace_service=subrace_domain_service,
            user_repository=user_repo,
            subrace_repository=subrace_repo,
            race_repository=race_repo,
        )
        self.update = command.subrace.UpdateSubraceUseCase(
            subrace_service=subrace_domain_service,
            user_repository=user_repo,
            subrace_repository=subrace_repo,
            race_repository=race_repo,
        )
        self.delete = command.subrace.DeleteSubraceUseCase(
            user_repository=user_repo,
            subrace_repository=subrace_repo,
        )
        self.get_one = query.subrace.GetSubraceUseCase(
            subrace_repository=subrace_repo,
        )
        self.get_all = query.subrace.GetSubracesUseCase(
            subrace_repository=subrace_repo,
        )


class ToolUseCases:
    def __init__(self) -> None:
        self.create = command.tool.CreateToolUseCase(
            tool_service=tool_domain_service,
            user_repository=user_repo,
            tool_repository=tool_repo,
        )
        self.update = command.tool.UpdateToolUseCase(
            tool_service=tool_domain_service,
            user_repository=user_repo,
            tool_repository=tool_repo,
        )
        self.delete = command.tool.DeleteToolUseCase(
            user_repository=user_repo,
            tool_repository=tool_repo,
            class_repository=character_class_repo,
        )
        self.get_one = query.tool.GetToolUseCase(
            tool_repository=tool_repo,
        )
        self.get_all = query.tool.GetToolsUseCase(
            tool_repository=tool_repo,
        )


class WeaponUseCases:
    def __init__(self) -> None:
        self.create = command.weapon.CreateWeaponUseCase(
            weapon_service=weapon_domain_service,
            user_repository=user_repo,
            weapon_repository=weapon_repo,
            kind_repository=weapon_kind_repo,
            property_repository=weapon_property_repo,
            material_repository=material_repo,
        )
        self.update = command.weapon.UpdateWeaponUseCase(
            weapon_service=weapon_domain_service,
            user_repository=user_repo,
            weapon_repository=weapon_repo,
            kind_repository=weapon_kind_repo,
            property_repository=weapon_property_repo,
            material_repository=material_repo,
        )
        self.delete = command.weapon.DeleteWeaponUseCase(
            user_repository=user_repo,
            weapon_repository=weapon_repo,
            class_repository=character_class_repo,
        )
        self.get_one = query.weapon.GetWeaponUseCase(
            weapon_repository=weapon_repo,
        )
        self.get_all = query.weapon.GetWeaponsUseCase(
            weapon_repository=weapon_repo,
        )


class WeaponKindUseCases:
    def __init__(self) -> None:
        self.create = command.weapon_kind.CreateWeaponKindUseCase(
            weapon_kind_service=weapon_kind_domain_service,
            user_repository=user_repo,
            weapon_kind_repository=weapon_kind_repo,
        )
        self.update = command.weapon_kind.UpdateWeaponKindUseCase(
            weapon_kind_service=weapon_kind_domain_service,
            user_repository=user_repo,
            weapon_kind_repository=weapon_kind_repo,
        )
        self.delete = command.weapon_kind.DeleteWeaponKindUseCase(
            user_repository=user_repo,
            weapon_kind_repository=weapon_kind_repo,
            weapon_repository=weapon_repo,
        )
        self.get_one = query.weapon_kind.GetWeaponKindUseCase(
            weapon_kind_repository=weapon_kind_repo,
        )
        self.get_all = query.weapon_kind.GetWeaponKindsUseCase(
            weapon_kind_repository=weapon_kind_repo,
        )


class WeaponPropertyUseCases:
    def __init__(self) -> None:
        self.create = command.weapon_property.CreateWeaponPropertyUseCase(
            weapon_property_service=weapon_property_domain_service,
            user_repository=user_repo,
            weapon_property_repository=weapon_property_repo,
        )
        self.update = command.weapon_property.UpdateWeaponPropertyUseCase(
            weapon_property_service=weapon_property_domain_service,
            user_repository=user_repo,
            weapon_property_repository=weapon_property_repo,
        )
        self.delete = command.weapon_property.DeleteWeaponPropertyUseCase(
            user_repository=user_repo,
            weapon_property_repository=weapon_property_repo,
            weapon_repository=weapon_repo,
        )
        self.get_one = query.weapon_property.GetWeaponPropertyUseCase(
            weapon_property_repository=weapon_property_repo,
        )
        self.get_all = query.weapon_property.GetWeaponPropertiesUseCase(
            weapon_property_repository=weapon_property_repo,
        )


armor_use_cases = ArmorUseCases()
class_use_cases = ClassUseCases()
subclass_use_cases = SubclassUseCases()
class_feature_use_cases = ClassFeatureUseCases()
class_level_use_cases = ClassLevelUseCases()
feat_use_cases = FeatUseCases()
material_use_cases = MaterialUseCases()
material_component_use_cases = MaterialComponentUseCases()
race_use_cases = RaceUseCases()
source_use_cases = SourceUseCases()
spell_use_cases = SpellUseCases()
subclass_feature_use_cases = SubclassFeatureUseCases()
subrace_use_cases = SubraceUseCases()
tool_use_cases = ToolUseCases()
weapon_use_cases = WeaponUseCases()
weapon_kind_use_cases = WeaponKindUseCases()
weapon_property_use_cases = WeaponPropertyUseCases()
