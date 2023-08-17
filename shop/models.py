import os

from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from accmarks.settings import MAX_LENGTH_CHAR


User = get_user_model()


class Category(models.Model):
    """Модель категорий акканутов.

    Определяет соц сете, к которой принадлежит
    тот или иной аккаунт: Вконтакте, Инстаграм, TG и тд.
    """

    name = models.CharField(
        max_length=settings.MAX_LENGTH_CHAR,
        db_index=True,
        verbose_name='Название:',
        help_text='введите название категории'
    )
    slug = models.SlugField(
        max_length=settings.MAX_LENGTH_CHAR,
        db_index=True,
        unique=True,
        verbose_name='Ссылка на категорию:',
        help_text='http://127.0.0.1:8000/',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])


class Product(models.Model):
    """Модель аккаунтов.

    Содержит основные, общие для всех типов аккаунтов, поля.
    """

    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Продавец:',
        help_text='выберите пользователя-продавца.'
    )
    category = models.ForeignKey(
        Category,
        related_name='+',
        on_delete=models.CASCADE,
        verbose_name='Соц. сеть:',
        help_text='выберите соц. сеть, к которой относится аккаунт',
    )
    country = models.CharField(
        choices=settings.COUNTRY_CHOICES,
        max_length=settings.MAX_LENGTH_CHAR,
        verbose_name='Регион регистрации аккаунта:',
        help_text='выберите регион из ниже перечисленых'
    )
    name = models.CharField(
        max_length=settings.MAX_LENGTH_CHAR,
        db_index=True,
        verbose_name='Заголовок объявления:'
    )
    slug = models.SlugField(
        max_length=settings.MAX_LENGTH_CHAR,
        db_index=True,
        verbose_name='Имя ссылки на объявление:'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание:',
        help_text='укажите краткое описание продовамеого/ых аккаунта/ов.',
        max_length=settings.MAX_LENGTH_DESC
    )
    price = models.DecimalField(
        max_digits=settings.MAX_LENGTH_INT,
        decimal_places=2,
        verbose_name='Цена:',
        help_text='укажите цену',
    )
    # stock = models.PositiveIntegerField(
    #     verbose_name='Кол-во:',
    #     help_text='укажите количество товарных единиц',
    # )
    available = models.BooleanField(
        default=True,
        verbose_name='Наличие:',
        help_text='поставьте галочку, если есть',
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    updated = models.DateTimeField(
        auto_now=True
    )
    password = models.CharField(
        max_length=settings.MAX_LENGTH_CHAR,
        verbose_name='Пароль:',
        help_text='укажите пароль от аккаунта'
    )
    login = models.CharField(
        max_length=settings.MAX_LENGTH_CHAR,
        verbose_name='Логин:',
        help_text='укажите логин или аналогичные данные для входа'
    )
    token = models.CharField(
        max_length=settings.MAX_LENGTH_CHAR,
        verbose_name='Токен авторизации:',
        help_text='укажите токен авторизации или аналогичные данные'
    )
    message_to_customer = models.TextField(
        max_length=settings.MAX_LENGTH_DESC,
        verbose_name='Сообщение покупателю после покупки:',
        help_text='это сообщение увидит покупатель после покупки'
    )

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])


class EmailDomainParam(models.Model):
    """Модель-параметр email доменов.

    Дает возможность присвоить тот или иной
    образ домена для аккаунта, используется при выборе аккаунтов
    для соц сетей: Вк, Ок и тд."""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='domain'
    )
    value = models.CharField(
        max_length=settings.MAX_LENGTH_CHAR,
        choices=settings.EMAIL_DOMAINS,
        verbose_name='Домен:',
        help_text='выберите нужный почтовый домен'
    )

    class Meta:
        verbose_name = 'Домен'
        verbose_name_plural = 'Почтовый домен'


class PhoneCountryParam(models.Model):
    """Модель-параметр регион номера.

    В ней выбирается регион номера телефона,
    который использовался при регистрации аккаунта."""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='phone_country'
    )
    value = models.CharField(
        choices=settings.COUNTRY_CHOICES,
        max_length=settings.MAX_LENGTH_CHAR,
        verbose_name='Регион:',
        help_text='выберите регион номера телефона'
    )

    class Meta:
        verbose_name = 'Регион номера'
        verbose_name_plural = 'Регион номера'


class EmailAccessModel(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='email_access'
    )
    value = models.CharField(
        max_length=settings.MAX_LENGTH_CHAR,
        choices=settings.EMAIL_ACCESS
    )

    class Meta:
        verbose_name_plural = 'Доступ к почте'


class SexParam(models.Model):
    """Модель выбора Пола.

    Выбор между Мужским и женским.
    Меню выбора нахоится в settings."""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='sex'
    )
    value = models.CharField(
        choices=settings.SEX,
        max_length=settings.MAX_LENGTH_CHAR,
        verbose_name='Пол:',
        help_text='выберите подходящее значение'
    )

    class Meta:
        verbose_name_plural = 'Пол'


class BoolParamsForProducts(models.Model):
    """ManyToOne модель Bool параметров.

    Содержит в себе названия, а также bool значения для
    параметров определенных Product
    """
    name = models.CharField(
        choices=settings.BOOL_PARAMS,
        verbose_name='Параметр:',
        help_text='выберите параметр',
        max_length=settings.MAX_LENGTH_CHAR
    )
    value = models.BooleanField(
        verbose_name='Наличие:',
        help_text='поставьте галочку, если параметр есть',
        default=False
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='bools'
    )

    class Meta:
        verbose_name = 'Есть/нет параметр'
        verbose_name_plural = 'Есть/нет параметры'
        unique_together = ['name', 'product']


class PSIFParamsForProducts(models.Model):
    """ManyToOne модель PositiveSmallIntegerField параметров.

    Содержит в себе названия, а также int значения для
    параметров определенных Product
    """
    name = models.CharField(
        choices=settings.PSIF_PARAMS,
        verbose_name='Параметр:',
        help_text='выберите параметр',
        max_length=settings.MAX_LENGTH_CHAR
    )
    value = models.PositiveSmallIntegerField(
        verbose_name='Кол-во:',
        help_text='введите значение соответствующие параметру',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='psif_params'
    )

    class Meta:
        verbose_name_plural = 'Кол-во чатов, групп - небольших значений'
        unique_together = ['name', 'product']


class PIFParamsForProducts(models.Model):
    """ManyToOne модель PositiveIntegerField параметров.

    Содержит в себе названия, а также int значения для
    параметров определенных Product
    """
    name = models.CharField(
        choices=settings.PIF_PARAMS,
        verbose_name='Параметр:',
        help_text='выберите параметр',
        max_length=settings.MAX_LENGTH_CHAR
    )
    value = models.PositiveIntegerField(
        verbose_name='Кол-во:',
        help_text='введите значение соответствующие параметру',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='pif_params'
    )

    class Meta:
        verbose_name_plural = 'Кол-во подписчиков, баланса - больших значений'
        unique_together = ['name', 'product']


@receiver(post_save, sender=Product)
def delete_product_when_stock_zero(sender, instance, **kwargs):
    if instance.stock == 0:
        instance.delete()


class AccountGroup(models.Model):
    r"""Модель группы аккаунтов ¯\_(ツ)_/¯."""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Аккаунт:',
        help_text='выберите нужный аккаунт',
    )
    account_name = models.CharField(
        max_length=settings.MAX_LENGTH_CHAR,
        verbose_name='Название аккаунта:',
        help_text='введите название аккаунта',
    )
    torrent_file = models.FileField(
        upload_to='torrents/',
        verbose_name='Данные:',
        help_text='загрузить файл с данными',
    )

    def save(self, *args, **kwargs):
        self.account_name = os.path.basename(self.torrent_file.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.account_name


class HistoryByAccountGroup(models.Model):
    r"""История групп аккаунтов ¯\_(ツ)_/¯."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    account_name = models.CharField(max_length=settings.MAX_LENGTH_CHAR)
    torrent_file = models.FileField(upload_to='torrents/')

    def save(self, *args, **kwargs):
        self.account_name = os.path.basename(self.torrent_file.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.account_name


class Game(models.Model):
    """Модель игр для стим."""

    # app_id = models.IntegerField(
    #     verbose_name='Код игры:',
    #     help_text='введите id игры из библиотеки стим',
    # )
    name = models.CharField(
        max_length=settings.MAX_LENGTH_CHAR,
        db_index=True,
        unique=True,
        verbose_name='Игра:',
        help_text='введите название игры',
    )
    slug = models.SlugField(
        max_length=settings.MAX_LENGTH_CHAR,
        db_index=True,
        unique=True,
        verbose_name='Ссылка:',
        help_text='http://127.0.0.1:8000/',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])


class GameOnSteam(models.Model):
    """Модель связи игр со стим аккаунтом.

    Сохраняет список игр, которые есть на
    определенном аккаунте, а также содержит доп поля
    такие как баланс инвенторя конкретной игры и
    наличие блокировки VAC.
    """

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='accounts',
        verbose_name='Игра:',
        help_text='выберите игру, которая есть на аккаунте.',
    )
    acc = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='games',
        verbose_name='Аккаунт:',
        help_text='выберите аккаунт, для которого хотите указать доп. данные',
    )
    balance = models.PositiveSmallIntegerField(
        verbose_name='Стоимость игрового инвентаря:',
        help_text='укажите примерную стоимость внутриигровых предметов'
    )
    block = models.BooleanField(
        default=False,
        verbose_name='Внтуриигровая блокировка(VAC):',
        help_text='поставьте галочку, если есть'
    )

    class Meta:
        ordering = ('id',)
        verbose_name_plural = 'Игры на аккаунте'
        unique_together = ['acc', 'game']

    def __str__(self):
        return self.acc.product.name
