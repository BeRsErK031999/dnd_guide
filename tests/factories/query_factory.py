from uuid import UUID, uuid4

from application.dto.query import (
    armor,
    character_class,
    character_subclass,
    class_feature,
    class_level,
    feat,
    material,
    material_component,
    race,
    source,
    spell,
    subclass_feature,
    subrace,
    tool,
    weapon,
    weapon_kind,
    weapon_property,
)


class ArmorQueryFactory:
    @staticmethod
    def query(armor_id: UUID = uuid4()) -> armor.ArmorQuery:
        return armor.ArmorQuery(armor_id=armor_id)

    @staticmethod
    def queries(
        search_by_name: str | None = None,
        filter_by_armor_types: list[str] | None = None,
        filter_by_material_ids: list[UUID] | None = None,
    ) -> armor.ArmorsQuery:
        return armor.ArmorsQuery(
            search_by_name=search_by_name,
            filter_by_armor_types=filter_by_armor_types,
            filter_by_material_ids=filter_by_material_ids,
        )


class ClassQueryFactory:
    @staticmethod
    def query(class_id: UUID = uuid4()) -> character_class.ClassQuery:
        return character_class.ClassQuery(class_id=class_id)

    @staticmethod
    def queries(search_by_name: str | None = None) -> character_class.ClassesQuery:
        return character_class.ClassesQuery(search_by_name=search_by_name)


class SubclassQueryFactory:
    @staticmethod
    def query(subclass_id: UUID = uuid4()) -> character_subclass.SubclassQuery:
        return character_subclass.SubclassQuery(subclass_id=subclass_id)

    @staticmethod
    def queries(
        filter_by_class_id: UUID | None = None,
    ) -> character_subclass.SubclassesQuery:
        return character_subclass.SubclassesQuery(filter_by_class_id=filter_by_class_id)


class ClassFeatureQueryFactory:
    @staticmethod
    def query(feature_id: UUID = uuid4()) -> class_feature.ClassFeatureQuery:
        return class_feature.ClassFeatureQuery(feature_id=feature_id)

    @staticmethod
    def queries(
        filter_by_class_id: UUID | None = None,
    ) -> class_feature.ClassFeaturesQuery:
        return class_feature.ClassFeaturesQuery(filter_by_class_id=filter_by_class_id)


class ClassLevelQueryFactory:
    @staticmethod
    def query(level_id: UUID = uuid4()) -> class_level.ClassLevelQuery:
        return class_level.ClassLevelQuery(class_level_id=level_id)

    @staticmethod
    def queries(filter_by_class_id: UUID | None = None) -> class_level.ClassLevelsQuery:
        return class_level.ClassLevelsQuery(filter_by_class_id=filter_by_class_id)


class FeatQueryFactory:
    @staticmethod
    def query(feat_id: UUID = uuid4()) -> feat.FeatQuery:
        return feat.FeatQuery(feat_id=feat_id)

    @staticmethod
    def queries(search_by_name: str | None = None) -> feat.FeatsQuery:
        return feat.FeatsQuery(search_by_name=search_by_name)


class MaterialQueryFactory:
    @staticmethod
    def query(material_id: UUID = uuid4()) -> material.MaterialQuery:
        return material.MaterialQuery(material_id=material_id)

    @staticmethod
    def queries(search_by_name: str | None = None) -> material.MaterialsQuery:
        return material.MaterialsQuery(search_by_name=search_by_name)


class MaterialComponentQueryFactory:
    @staticmethod
    def query(material_id: UUID = uuid4()) -> material_component.MaterialComponentQuery:
        return material_component.MaterialComponentQuery(material_id=material_id)

    @staticmethod
    def queries(
        search_by_name: str | None = None,
    ) -> material_component.MaterialComponentsQuery:
        return material_component.MaterialComponentsQuery()


class RaceQueryFactory:
    @staticmethod
    def query(race_id: UUID = uuid4()) -> race.RaceQuery:
        return race.RaceQuery(race_id=race_id)

    @staticmethod
    def queries(search_by_name: str | None = None) -> race.RacesQuery:
        return race.RacesQuery(search_by_name=search_by_name)


class SourceQueryFactory:
    @staticmethod
    def query(source_id: UUID = uuid4()) -> source.SourceQuery:
        return source.SourceQuery(source_id=source_id)

    @staticmethod
    def queries(search_by_name: str | None = None) -> source.SourcesQuery:
        return source.SourcesQuery(search_by_name=search_by_name)


class SpellQueryFactory:
    @staticmethod
    def query(spell_id: UUID = uuid4()) -> spell.SpellQuery:
        return spell.SpellQuery(spell_id=spell_id)

    @staticmethod
    def queries(
        search_by_name: str | None = None,
        filter_by_class_ids: list[UUID] | None = None,
        filter_by_subclass_ids: list[UUID] | None = None,
        filter_by_schools: list[str] | None = None,
        filter_by_damage_types: list[str] | None = None,
        filter_by_durations: list[str] | None = None,
        filter_by_casting_times: list[str] | None = None,
        filter_by_verbal_component: bool | None = None,
        filter_by_symbolic_component: bool | None = None,
        filter_by_material_component: bool | None = None,
        filter_by_concentration: bool | None = None,
        filter_by_ritual: bool | None = None,
        filter_by_source_ids: list[UUID] | None = None,
    ) -> spell.SpellsQuery:
        return spell.SpellsQuery(
            search_by_name=search_by_name,
            filter_by_class_ids=filter_by_class_ids,
            filter_by_subclass_ids=filter_by_subclass_ids,
            filter_by_schools=filter_by_schools,
            filter_by_damage_types=filter_by_damage_types,
            filter_by_durations=filter_by_durations,
            filter_by_casting_times=filter_by_casting_times,
            filter_by_verbal_component=filter_by_verbal_component,
            filter_by_symbolic_component=filter_by_symbolic_component,
            filter_by_material_component=filter_by_material_component,
            filter_by_concentration=filter_by_concentration,
            filter_by_ritual=filter_by_ritual,
            filter_by_source_ids=filter_by_source_ids,
        )


class SubclassFeatureQueryFactory:
    @staticmethod
    def query(feature_id: UUID = uuid4()) -> subclass_feature.SubclassFeatureQuery:
        return subclass_feature.SubclassFeatureQuery(
            feature_id=feature_id,
        )

    @staticmethod
    def queries(
        filter_by_subclass_id: UUID | None = None,
    ) -> subclass_feature.SubclassFeaturesQuery:
        return subclass_feature.SubclassFeaturesQuery(
            filter_by_subclass_id=filter_by_subclass_id
        )


class SubraceQueryFactory:
    @staticmethod
    def query(subrace_id: UUID = uuid4()) -> subrace.SubraceQuery:
        return subrace.SubraceQuery(subrace_id=subrace_id)

    @staticmethod
    def queries(search_by_name: str | None = None) -> subrace.SubracesQuery:
        return subrace.SubracesQuery(search_by_name=search_by_name)


class ToolQueryFactory:
    @staticmethod
    def query(tool_id: UUID = uuid4()) -> tool.ToolQuery:
        return tool.ToolQuery(tool_id=tool_id)

    @staticmethod
    def queries(search_by_name: str | None = None) -> tool.ToolsQuery:
        return tool.ToolsQuery(search_by_name=search_by_name)


class WeaponQueryFactory:
    @staticmethod
    def query(weapon_id: UUID = uuid4()) -> weapon.WeaponQuery:
        return weapon.WeaponQuery(
            weapon_id=weapon_id,
        )

    @staticmethod
    def queries(
        search_by_name: str | None = None,
        filter_by_kind_ids: list[UUID] | None = None,
        filter_by_damage_types: list[str] | None = None,
        filter_by_property_ids: list[UUID] | None = None,
        filter_by_material_ids: list[UUID] | None = None,
    ) -> weapon.WeaponsQuery:
        return weapon.WeaponsQuery(
            search_by_name=search_by_name,
            filter_by_kind_ids=filter_by_kind_ids,
            filter_by_damage_types=filter_by_damage_types,
            filter_by_property_ids=filter_by_property_ids,
            filter_by_material_ids=filter_by_material_ids,
        )


class WeaponKindQueryFactory:
    @staticmethod
    def query(kind_id: UUID = uuid4()) -> weapon_kind.WeaponKindQuery:
        return weapon_kind.WeaponKindQuery(weapon_kind_id=kind_id)

    @staticmethod
    def queries(
        search_by_name: str | None = None, filter_by_types: list[str] | None = None
    ) -> weapon_kind.WeaponKindsQuery:
        return weapon_kind.WeaponKindsQuery(
            search_by_name=search_by_name, filter_by_types=filter_by_types
        )


class WeaponPropertyQueryFactory:
    @staticmethod
    def query(property_id: UUID = uuid4()) -> weapon_property.WeaponPropertyQuery:
        return weapon_property.WeaponPropertyQuery(
            weapon_property_id=property_id,
        )

    @staticmethod
    def queries(
        search_by_name: str | None = None,
    ) -> weapon_property.WeaponPropertiesQuery:
        return weapon_property.WeaponPropertiesQuery(search_by_name=search_by_name)
