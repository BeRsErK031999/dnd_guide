import pytest
from adapters.repository import inmemory

repositories: dict = {
    "armor": inmemory.InMemoryArmorRepository(),
    "class": inmemory.InMemoryClassRepository(),
    "subclass": inmemory.InMemorySubclassRepository(),
    "class_feature": inmemory.InMemoryClassFeatureRepository(),
    "class_level": inmemory.InMemoryClassLevelRepository(),
    "feat": inmemory.InMemoryFeatRepository(),
    "material_component": inmemory.InMemoryMaterialComponentRepository(),
    "material": inmemory.InMemoryMaterialRepository(),
    "race": inmemory.InMemoryRaceRepository(),
    "source": inmemory.InMemorySourceRepository(),
    "spell": inmemory.InMemorySpellRepository(),
    "subclass_feature": inmemory.InMemorySubclassFeatureRepository(),
    "subrace": inmemory.InMemorySubraceRepository(),
    "tool": inmemory.InMemoryToolRepository(),
    "weapon": inmemory.InMemoryWeaponRepository(),
    "weapon_kind": inmemory.InMemoryWeaponKindRepository(),
    "weapon_property": inmemory.InMemoryWeaponPropertyRepository(),
    "user": inmemory.InMemoryUserRepository(),
}


@pytest.fixture(autouse=True)
def clear_repositories():
    for repository in repositories.values():
        repository._store = dict()


@pytest.fixture
def armor_repository():
    return repositories["armor"]


@pytest.fixture
def class_repository():
    return repositories["class"]


@pytest.fixture
def subclass_repository():
    return repositories["subclass"]


@pytest.fixture
def class_feature_repository():
    return repositories["class_feature"]


@pytest.fixture
def class_level_repository():
    return repositories["class_level"]


@pytest.fixture
def feat_repository():
    return repositories["feat"]


@pytest.fixture
def material_component_repository():
    return repositories["material_component"]


@pytest.fixture
def material_repository():
    return repositories["material"]


@pytest.fixture
def race_repository():
    return repositories["race"]


@pytest.fixture
def source_repository():
    return repositories["source"]


@pytest.fixture
def spell_repository():
    return repositories["spell"]


@pytest.fixture
def subclass_feature_repository():
    return repositories["subclass_feature"]


@pytest.fixture
def subrace_repository():
    return repositories["subrace"]


@pytest.fixture
def tool_repository():
    return repositories["tool"]


@pytest.fixture
def weapon_repository():
    return repositories["weapon"]


@pytest.fixture
def weapon_kind_repository():
    return repositories["weapon_kind"]


@pytest.fixture
def weapon_property_repository():
    return repositories["weapon_property"]


@pytest.fixture
def user_repository():
    return repositories["user"]
