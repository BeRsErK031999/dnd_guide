from adapters.repository import sql
from application.use_case import command, query
from config import config
from domain.armor import ArmorService
from domain.material import MaterialService


class Repositories:
    def __init__(self) -> None:
        db_helper = sql.DBHelper(config.db_url)
        self.user = sql.SQLUserRepository(db_helper)
        self.armor = sql.SQLArmorRepository(db_helper)
        self.material = sql.SQLMaterialRepository(db_helper)


class DomainServices:
    def __init__(self, repositories: Repositories) -> None:
        self.armor = ArmorService(repositories.armor)
        self.material = MaterialService(repositories.material)


class UseCases:
    def __init__(self) -> None:
        self._repositories = Repositories()
        self._domain_services = DomainServices(self._repositories)
        self.create_armor = command.armor.CreateArmorUseCase(
            armor_service=self._domain_services.armor,
            user_repository=self._repositories.user,
            armor_repository=self._repositories.armor,
            material_repository=self._repositories.material,
        )
        self.update_armor = command.armor.UpdateArmorUseCase(
            armor_service=self._domain_services.armor,
            user_repository=self._repositories.user,
            armor_repository=self._repositories.armor,
            material_repository=self._repositories.material,
        )
        self.delete_armor = command.armor.DeleteArmorUseCase(
            user_repository=self._repositories.user,
            armor_repository=self._repositories.armor,
        )
        self.get_armor = query.armor.GetArmorUseCase(
            armor_repository=self._repositories.armor,
        )
        self.get_armors = query.armor.GetArmorsUseCase(
            armor_repository=self._repositories.armor,
        )
        self.create_material = command.material.CreateMaterialUseCase(
            material_service=self._domain_services.material,
            user_repository=self._repositories.user,
            material_repository=self._repositories.material,
        )
        self.update_material = command.material.UpdateMaterialUseCase(
            material_service=self._domain_services.material,
            user_repository=self._repositories.user,
            material_repository=self._repositories.material,
        )
        self.delete_material = command.material.DeleteMaterialUseCase(
            user_repository=self._repositories.user,
            material_repository=self._repositories.material,
        )
        self.get_material = query.material.GetMaterialUseCase(
            material_repository=self._repositories.material
        )
        self.get_materials = query.material.GetMaterialsUseCase(
            material_repository=self._repositories.material
        )


class Container:
    def __init__(self) -> None:
        self.use_cases = UseCases()


container = Container()
