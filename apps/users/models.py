# AbstractUser — готовий клас юзера від Django.
# Вже містить поля: username, email, password, first_name,
# last_name, is_active, date_joined, та методи логіну.
# Ми його розширюємо, а не пишемо з нуля.
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.models import BaseModel  # мій базовий клас, має created_at / updated_at


# AbstractUser — беремо всі стандартні поля юзера
# BaseModel — беремо created_at, updated_at (або що там у тебе)
class User(AbstractUser, BaseModel):

    # CharField — текстове поле, max_length обов'язковий
    # unique=True — два юзери не можуть мати однаковий номер
    phone = models.CharField(max_length=20, unique=True)

    # ImageField — як FileField але перевіряє що це картинка
    # upload_to — в яку папку зберігати файл на сервері
    # blank=True — поле необов'язкове (можна не заповнювати)
    avatar = models.ImageField(upload_to="avatars/", blank=True)

    # ForeignKey — зв'язок "багато до одного"
    # Багато юзерів можуть мати одну роль
    # 'Role' в лапках — бо клас Role оголошений нижче в файлі,
    # Python ще не знає про нього, тому пишемо рядком
    # on_delete=SET_NULL — якщо роль видалять, юзер не видаляється,
    # просто його role стане NULL
    # null=True — дозволяє NULL в базі даних
    # blank=True — дозволяє не заповнювати в формах/серіалайзерах
    role = models.ForeignKey(
        'Role',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username  # в адмінці юзер показується як username


class Permissions(models.Model):

    # Читабельна назва: "Може створювати оголошення"
    name = models.CharField(max_length=100, unique=True)

    # Короткий код для перевірок у коді: "can_create_listing"
    # Цей не чіпаєш після створення — на нього посилається логіка
    codename = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Role(models.Model):

    # 'buyer', 'seller', 'manager', 'admin'
    name = models.CharField(max_length=50, unique=True)

    # ManyToManyField — одна роль має багато дозволів,
    # один дозвіл може бути у багатьох ролях
    # through='RolePermissions' — не створюй таблицю-місток автоматично,
    # а використовуй мій клас RolePermissions
    # Навіщо свій клас? Щоб потім можна було додати поля
    # (наприклад, granted_at — коли дозвіл був виданий)
    permissions = models.ManyToManyField(Permissions, through='RolePermissions')

    def __str__(self):
        return self.name


class RolePermissions(models.Model):
    # Таблиця-місток: зберігає пари (роль, дозвіл)

    # CASCADE — якщо роль видалять, видаляться і всі її записи тут
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permissions, on_delete=models.CASCADE)

    class Meta:
        # Захист від дублів — не можна двічі додати
        # той самий дозвіл до тієї самої ролі
        unique_together = ('role', 'permission')


class AccountType(models.Model):

    # Це просто константи класу — НЕ поля таблиці
    # Використовуємо щоб не писати рядки 'basic'/'premium' вручну по всьому коду
    BASIC = 'basic'
    PREMIUM = 'premium'

    # Список пар (значення_в_базі, назва_для_людини)
    # Django використовує це щоб обмежити допустимі значення поля
    TYPE_CHOICES = [
        (BASIC, 'Basic'),
        (PREMIUM, 'Premium'),
    ]

    # OneToOneField — кожен юзер має рівно один AccountType
    # Це як ForeignKey але з unique=True
    # related_name — як дістатись від юзера:
    # user.account_type  (замість user.accounttype_set)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='account_type'
    )

    # choices обмежує значення тільки тими що в TYPE_CHOICES
    # default=BASIC — новий акаунт завжди базовий
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=BASIC)

    # Дата закінчення преміуму
    # null=True, blank=True — у базового акаунту цього поля немає
    expires_at = models.DateTimeField(null=True, blank=True)

    def is_premium_active(self):
        # Метод — не поле в базі, просто логіка
        from django.utils import timezone

        # Перевіряємо: тип = преміум І дата є І дата ще не минула
        if self.type == self.PREMIUM and self.expires_at:
            return self.expires_at > timezone.now()

        return False  # в усіх інших випадках — не активний