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
    def query(
        armor_id: UUID = uuid4(),
    ) -> armor.ArmorQuery:
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
