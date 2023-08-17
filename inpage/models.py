from django.db import models
from django.conf import settings


class Advertisement(models.Model):
    """Модель рекламы.

    Хранит в себе рекламные баннеры, которые
    показываются на страницах сайта
    """
    name = models.CharField(
        max_length=settings.MAX_LENGTH_CHAR,
        verbose_name='Название:',
        help_text='укажите название компании/заказчика'
    )
    banner = models.ImageField(
        verbose_name='Баннер:',
        help_text='выберите рекламный баннер',
        upload_to='media/adv/'
    )
    link = models.CharField(
        verbose_name='Реферальная ссылка:',
        help_text='вставьте ссылку для рекламной компании',
        max_length=settings.MAX_LENGTH_ADV
    )
    active = models.BooleanField(
        verbose_name='Показывать рекламу:',
        help_text=(
            'выберите, чтобы сделать ее активной. '
            'Изменения применятся, если нет другой активной '
            'рекламы'
        ),
        unique=True
    )

    class Meta:
        ordering = ('-active',)
        verbose_name = 'Реклама'
        verbose_name_plural = 'Рекламы'

    def __str__(self):
        return self.name
