from domain.armor_type import ArmorType
from domain.character_class.class_id import ClassID
from domain.character_class.description import ClassDescription
from domain.character_class.hit import ClassHit
from domain.character_class.name import ClassName
from domain.character_class.proficiency import ClassProficiency
from domain.character_class.skill import ClassSkill
from domain.dice import Dice
from domain.modifier import Modifier
from domain.tool_type import ToolType
from domain.weapon_type import WeaponType


class CharacterClass:
    def __init__(
        self,
        class_id: ClassID,
        name: ClassName,
        description: ClassDescription,
    ) -> None:
        self.__class_id = class_id
        self.__name = name
        self.__description = description
        match name:
            case ClassName.BARD:
                self.__init_bard()
            case ClassName.BARBARIAN:
                self.__init_barbarian()
            case ClassName.FIGHTER:
                self.__init_fighter()
            case ClassName.WIZARD:
                self.__init_wizard()
            case ClassName.DRUID:
                self.__init_druid()
            case ClassName.CLERIC:
                self.__init_cleric()
            case ClassName.WARLOCK:
                self.__init_warlock()
            case ClassName.MONK:
                self.__init_monk()
            case ClassName.PALADIN:
                self.__init_paladin()
            case ClassName.ROGUE:
                self.__init_rogue()
            case ClassName.RANGER:
                self.__init_ranger()
            case ClassName.SORCERER:
                self.__init_sorcerer()

    def __init_bard(self) -> None:
        self.__primary_modifier = [Modifier.CHARISMA]
        self.__hits = ClassHit(
            hit_dice=Dice.D8,
            starting_hits=8,
            hit_modifier=Modifier.CONSTITUTION,
            next_level_hits=5,
        )
        self.__proficiency = ClassProficiency(
            armors=[ArmorType.LIGHT_ARMOR],
            weapon=[WeaponType.SIMPLE],
            tools=[ToolType.MUSICAL_INSTRUMENTS],
            number_tools=3,
            saving_throws=[Modifier.CHARISMA, Modifier.DEXTERITY],
            skills=[
                ClassSkill.ACROBATICS,
                ClassSkill.ATHLETICS,
                ClassSkill.PERCEPTION,
                ClassSkill.SURVIVAL,
                ClassSkill.ANIMAL_HANDLING,
                ClassSkill.INTIMIDATION,
                ClassSkill.PERFORMANCE,
                ClassSkill.HISTORY,
                ClassSkill.SLEIGHT_OF_HAND,
                ClassSkill.ARCANA,
                ClassSkill.MEDICINE,
                ClassSkill.DECEPTION,
                ClassSkill.NATURE,
                ClassSkill.INSIGHT,
                ClassSkill.INVESTIGATION,
                ClassSkill.RELIGION,
                ClassSkill.STEALTH,
                ClassSkill.PERSUASION,
            ],
            number_skills=3,
        )

    def __init_barbarian(self) -> None:
        self.__primary_modifier = [Modifier.STRENGTH]
        self.__hits = ClassHit(
            hit_dice=Dice.D12,
            starting_hits=12,
            hit_modifier=Modifier.CONSTITUTION,
            next_level_hits=7,
        )
        self.__proficiency = ClassProficiency(
            armors=[ArmorType.LIGHT_ARMOR, ArmorType.MEDIUM_ARMOR, ArmorType.SHIELD],
            weapon=[WeaponType.SIMPLE, WeaponType.MARTIAL],
            tools=[],
            saving_throws=[Modifier.STRENGTH, Modifier.CONSTITUTION],
            skills=[
                ClassSkill.ANIMAL_HANDLING,
                ClassSkill.ATHLETICS,
                ClassSkill.INTIMIDATION,
                ClassSkill.NATURE,
                ClassSkill.PERCEPTION,
                ClassSkill.SURVIVAL,
            ],
            number_skills=2,
        )

    def __init_fighter(self) -> None:
        self.__primary_modifier = [Modifier.STRENGTH]
        self.__hits = ClassHit(
            hit_dice=Dice.D10,
            starting_hits=10,
            hit_modifier=Modifier.CONSTITUTION,
            next_level_hits=6,
        )
        self.__proficiency = ClassProficiency(
            armors=[
                ArmorType.LIGHT_ARMOR,
                ArmorType.MEDIUM_ARMOR,
                ArmorType.HEAVY_ARMOR,
                ArmorType.SHIELD,
            ],
            weapon=[WeaponType.SIMPLE, WeaponType.MARTIAL],
            tools=[],
            saving_throws=[Modifier.STRENGTH, Modifier.CONSTITUTION],
            skills=[
                ClassSkill.ACROBATICS,
                ClassSkill.ANIMAL_HANDLING,
                ClassSkill.ATHLETICS,
                ClassSkill.HISTORY,
                ClassSkill.INSIGHT,
                ClassSkill.INTIMIDATION,
                ClassSkill.PERSUASION,
                ClassSkill.PERCEPTION,
                ClassSkill.SURVIVAL,
            ],
            number_skills=2,
        )

    def __init_wizard(self) -> None:
        self.__primary_modifier = [Modifier.INTELLIGENT]
        self.__hits = ClassHit(
            hit_dice=Dice.D6,
            starting_hits=6,
            hit_modifier=Modifier.CONSTITUTION,
            next_level_hits=4,
        )
        self.__proficiency = ClassProficiency(
            armors=[],
            weapon=[WeaponType.SIMPLE],
            tools=[],
            saving_throws=[Modifier.INTELLIGENT, Modifier.WISDOM],
            skills=[
                ClassSkill.ARCANA,
                ClassSkill.HISTORY,
                ClassSkill.INSIGHT,
                ClassSkill.INVESTIGATION,
                ClassSkill.MEDICINE,
                ClassSkill.NATURE,
                ClassSkill.RELIGION,
            ],
            number_skills=2,
        )

    def __init_druid(self) -> None:
        self.__primary_modifier = [Modifier.WISDOM]
        self.__hits = ClassHit(
            hit_dice=Dice.D8,
            starting_hits=8,
            hit_modifier=Modifier.CONSTITUTION,
            next_level_hits=5,
        )
        self.__proficiency = ClassProficiency(
            armors=[ArmorType.LIGHT_ARMOR, ArmorType.MEDIUM_ARMOR, ArmorType.SHIELD],
            weapon=[WeaponType.SIMPLE],
            tools=[ToolType.HERBALISM_KIT],
            saving_throws=[Modifier.INTELLIGENT, Modifier.WISDOM],
            skills=[
                ClassSkill.ANIMAL_HANDLING,
                ClassSkill.ARCANA,
                ClassSkill.INSIGHT,
                ClassSkill.MEDICINE,
                ClassSkill.NATURE,
                ClassSkill.PERCEPTION,
                ClassSkill.RELIGION,
                ClassSkill.RELIGION,
            ],
            number_skills=2,
        )

    def __init_cleric(self) -> None:
        self.__primary_modifier = [Modifier.WISDOM]
        self.__hits = ClassHit(
            hit_dice=Dice.D8,
            starting_hits=8,
            hit_modifier=Modifier.CONSTITUTION,
            next_level_hits=5,
        )
        self.__proficiency = ClassProficiency(
            armors=[ArmorType.LIGHT_ARMOR, ArmorType.MEDIUM_ARMOR, ArmorType.SHIELD],
            weapon=[WeaponType.SIMPLE],
            tools=[],
            saving_throws=[Modifier.CHARISMA, Modifier.WISDOM],
            skills=[
                ClassSkill.HISTORY,
                ClassSkill.INSIGHT,
                ClassSkill.MEDICINE,
                ClassSkill.PERSUASION,
                ClassSkill.RELIGION,
            ],
            number_skills=2,
        )

    def __init_warlock(self) -> None:
        self.__primary_modifier = [Modifier.WISDOM]
        self.__hits = ClassHit(
            hit_dice=Dice.D8,
            starting_hits=8,
            hit_modifier=Modifier.CONSTITUTION,
            next_level_hits=5,
        )
        self.__proficiency = ClassProficiency(
            armors=[ArmorType.LIGHT_ARMOR],
            weapon=[WeaponType.SIMPLE],
            tools=[],
            saving_throws=[Modifier.CHARISMA, Modifier.WISDOM],
            skills=[
                ClassSkill.ARCANA,
                ClassSkill.DECEPTION,
                ClassSkill.HISTORY,
                ClassSkill.INTIMIDATION,
                ClassSkill.INVESTIGATION,
                ClassSkill.NATURE,
                ClassSkill.RELIGION,
            ],
            number_skills=2,
        )

    def __init_monk(self) -> None:
        self.__primary_modifier = [Modifier.WISDOM, Modifier.DEXTERITY]
        self.__hits = ClassHit(
            hit_dice=Dice.D8,
            starting_hits=8,
            hit_modifier=Modifier.CONSTITUTION,
            next_level_hits=5,
        )
        self.__proficiency = ClassProficiency(
            armors=[],
            weapon=[WeaponType.SIMPLE, WeaponType.MARTIAL],
            tools=[ToolType.ARTISANS_TOOLS, ToolType.MUSICAL_INSTRUMENTS],
            saving_throws=[Modifier.STRENGTH, Modifier.DEXTERITY],
            skills=[
                ClassSkill.ACROBATICS,
                ClassSkill.ATHLETICS,
                ClassSkill.HISTORY,
                ClassSkill.INSIGHT,
                ClassSkill.RELIGION,
                ClassSkill.STEALTH,
            ],
            number_skills=2,
        )

    def __init_paladin(self) -> None:
        self.__primary_modifier = [Modifier.STRENGTH, Modifier.CHARISMA]
        self.__hits = ClassHit(
            hit_dice=Dice.D10,
            starting_hits=10,
            hit_modifier=Modifier.CONSTITUTION,
            next_level_hits=6,
        )
        self.__proficiency = ClassProficiency(
            armors=[
                ArmorType.LIGHT_ARMOR,
                ArmorType.MEDIUM_ARMOR,
                ArmorType.HEAVY_ARMOR,
                ArmorType.SHIELD,
            ],
            weapon=[WeaponType.SIMPLE, WeaponType.MARTIAL],
            tools=[],
            saving_throws=[Modifier.CHARISMA, Modifier.WISDOM],
            skills=[
                ClassSkill.ATHLETICS,
                ClassSkill.INSIGHT,
                ClassSkill.INTIMIDATION,
                ClassSkill.MEDICINE,
                ClassSkill.PERSUASION,
                ClassSkill.RELIGION,
            ],
            number_skills=2,
        )

    def __init_rogue(self) -> None:
        self.__primary_modifier = [Modifier.DEXTERITY]
        self.__hits = ClassHit(
            hit_dice=Dice.D8,
            starting_hits=8,
            hit_modifier=Modifier.CONSTITUTION,
            next_level_hits=5,
        )
        self.__proficiency = ClassProficiency(
            armors=[ArmorType.LIGHT_ARMOR],
            weapon=[WeaponType.SIMPLE, WeaponType.MARTIAL],
            tools=[ToolType.THIEVES_TOOLS],
            saving_throws=[Modifier.INTELLIGENT, Modifier.DEXTERITY],
            skills=[
                ClassSkill.ACROBATICS,
                ClassSkill.ATHLETICS,
                ClassSkill.DECEPTION,
                ClassSkill.INSIGHT,
                ClassSkill.INTIMIDATION,
                ClassSkill.INVESTIGATION,
                ClassSkill.PERCEPTION,
                ClassSkill.PERSUASION,
                ClassSkill.SLEIGHT_OF_HAND,
                ClassSkill.STEALTH,
            ],
            number_skills=4,
        )

    def __init_ranger(self) -> None:
        self.__primary_modifier = [Modifier.DEXTERITY, Modifier.WISDOM]
        self.__hits = ClassHit(
            hit_dice=Dice.D10,
            starting_hits=10,
            hit_modifier=Modifier.CONSTITUTION,
            next_level_hits=6,
        )
        self.__proficiency = ClassProficiency(
            armors=[
                ArmorType.LIGHT_ARMOR,
                ArmorType.MEDIUM_ARMOR,
                ArmorType.SHIELD,
            ],
            weapon=[WeaponType.SIMPLE, WeaponType.MARTIAL],
            tools=[],
            saving_throws=[Modifier.STRENGTH, Modifier.DEXTERITY],
            skills=[
                ClassSkill.ANIMAL_HANDLING,
                ClassSkill.ATHLETICS,
                ClassSkill.INSIGHT,
                ClassSkill.INVESTIGATION,
                ClassSkill.NATURE,
                ClassSkill.PERCEPTION,
                ClassSkill.STEALTH,
                ClassSkill.SURVIVAL,
            ],
            number_skills=3,
        )

    def __init_sorcerer(self) -> None:
        self.__primary_modifier = [Modifier.CHARISMA]
        self.__hits = ClassHit(
            hit_dice=Dice.D6,
            starting_hits=6,
            hit_modifier=Modifier.CONSTITUTION,
            next_level_hits=4,
        )
        self.__proficiency = ClassProficiency(
            armors=[],
            weapon=[WeaponType.SIMPLE],
            tools=[],
            saving_throws=[Modifier.CONSTITUTION, Modifier.CHARISMA],
            skills=[
                ClassSkill.ARCANA,
                ClassSkill.DECEPTION,
                ClassSkill.INSIGHT,
                ClassSkill.INTIMIDATION,
                ClassSkill.PERSUASION,
                ClassSkill.RELIGION,
            ],
            number_skills=2,
        )

    def class_id(self) -> ClassID:
        return self.__class_id

    def name(self) -> ClassName:
        return self.__name

    def description(self) -> ClassDescription:
        return self.__description

    def primary_modifier(self) -> list[Modifier]:
        return self.__primary_modifier

    def hits(self) -> ClassHit:
        return self.__hits

    def proficiency(self) -> ClassProficiency:
        return self.__proficiency

    def new_description(self, description: ClassDescription) -> None:
        self.__description = description

    def __str__(self) -> str:
        return f"название: {self.__name}"
