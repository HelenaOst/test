from django.db import migrations


def create_permissions_and_assign(apps, schema_editor):
    Role = apps.get_model('users', 'Role')
    CustomPermission = apps.get_model('users', 'CustomPermission')
    RolePermissions = apps.get_model('users', 'RolePermissions')

    # 1. Створюємо всі пермішни
    permissions_data = [
        # акаунт
        ('Can view own account', 'can_view_own_account'),
        ('Can update own account', 'can_update_own_account'),
        ('Can delete own account', 'can_delete_own_account'),
        # оголошення
        ('Can create listing', 'can_create_listing'),
        ('Can edit own listing', 'can_edit_own_listing'),
        ('Can delete own listing', 'can_delete_own_listing'),
        # менеджер
        ('Can view users', 'can_view_users'),
        ('Can view user by id', 'can_view_user_by_id'),
        ('Can delete user by id', 'can_delete_user_by_id'),
        ('Can block unblock user', 'can_block_unblock_user'),
        # адмін
        ('Can create manager', 'can_create_manager'),
    ]

    perms = {}
    for name, codename in permissions_data:
        perm, _ = CustomPermission.objects.get_or_create(
            codename=codename,
            defaults={'name': name}
        )
        perms[codename] = perm

    # 2. Визначаємо які пермішни для яких ролей
    role_permissions = {
        'buyer': [
            'can_view_own_account',
            'can_update_own_account',
            'can_delete_own_account',
            'can_create_listing',
        ],
        'seller': [
            'can_view_own_account',
            'can_update_own_account',
            'can_delete_own_account',
            'can_create_listing',
            'can_edit_own_listing',
            'can_delete_own_listing',
        ],
        'manager': [
            'can_view_own_account',
            'can_update_own_account',
            'can_delete_own_account',
            'can_view_users',
            'can_view_user_by_id',
            'can_delete_user_by_id',
            'can_block_unblock_user',
        ],
        'admin': [
            'can_view_own_account',
            'can_update_own_account',
            'can_delete_own_account',
            'can_view_users',
            'can_view_user_by_id',
            'can_delete_user_by_id',
            'can_block_unblock_user',
            'can_create_manager',
        ],
    }

    # 3. Прив'язуємо пермішни до ролей
    for role_name, codenames in role_permissions.items():
        role = Role.objects.get(name=role_name)
        for codename in codenames:
            RolePermissions.objects.get_or_create(
                role=role,
                permission=perms[codename]
            )


def remove_permissions(apps, schema_editor):
    CustomPermission = apps.get_model('users', 'CustomPermission')
    CustomPermission.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_create_default_roles"),
    ]

    operations = [
        migrations.RunPython(create_permissions_and_assign, reverse_code=remove_permissions),
    ]
