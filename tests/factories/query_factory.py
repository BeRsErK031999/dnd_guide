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
