from schemas.users import Role as UserRole
from fastapi import HTTPException
from database.models.users import User

class UserPermissions:
    @staticmethod
    def has_role(user_role: UserRole, allowed_roles: list) -> bool:
        return user_role in allowed_roles

    @staticmethod
    def has_permission(user_role: UserRole, user_id: int, current_user: User, action: str) -> bool:
        if action == "read":
            return UserPermissions.has_role(user_role, [UserRole.admin, UserRole.user, UserRole.userManager])
        elif action == "create":
            return UserPermissions.has_role(user_role, [UserRole.admin, UserRole.user, UserRole.userManager])
        elif action == "update":
            return UserPermissions.has_role(user_role, [UserRole.admin, UserRole.user, UserRole.userManager]) or user_id == current_user.id
        elif action == "delete":
            return UserPermissions.has_role(user_role, [UserRole.admin, UserRole.user, UserRole.userManager]) or user_id == current_user.id
        elif action == "read_user_manager":
            return UserPermissions.has_role(user_role, [UserRole.admin, UserRole.userManager])
        elif action == "create_user_manager":
            return UserPermissions.has_role(user_role, [UserRole.admin, UserRole.userManager])
        elif action == "update_user_manager":
            return UserPermissions.has_role(user_role, [UserRole.admin, UserRole.userManager]) or user_id == current_user.id
        elif action == "delete_user_manager":
            return UserPermissions.has_role(user_role, [UserRole.admin, UserRole.userManager]) or user_id == current_user.id
        elif action == "read_admin":
            return UserPermissions.has_role(user_role, [UserRole.admin])
        elif action == "create_admin":
            return UserPermissions.has_role(user_role, [UserRole.admin])
        elif action == "update_admin":
            return UserPermissions.has_role(user_role, [UserRole.admin]) and user_id == current_user.id
        elif action == "delete_admin":
            return UserPermissions.has_role(user_role, [UserRole.admin]) and user_id == current_user.id
        elif action == "read_all_users":
            return UserPermissions.has_role(user_role, [UserRole.admin, UserRole.userManager])
        elif action == "read_all_user_managers":
            return UserPermissions.has_role(user_role, [UserRole.admin])
        else:
            return False

def check_permission(user_role: UserRole, user_id: int, current_user: User, action: str):
    if not UserPermissions.has_permission(user_role, user_id, current_user, action):
        raise HTTPException(status_code=403, detail="Not enough permissions")
