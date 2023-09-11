import redis
from django.conf import settings
from .models import Product


# Соединение с Redis
r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
)


class Recommender:
    def get_product_key(self, id):
        return f'Товар:{id}:куплен с'

    def product_bought(self, products):
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                # Получаем другие товары, купленные
                # вмесете с каждым товаром
                if product_id != with_id:
                    # Увеличиваем балл товара, купленного вместе
                    r.zincrby(
                        self.get_product_key(product_id),
                        1,
                        with_id
                    )

    def suggest_product_for(self, products, max_results=6):
        product_ids = [int(id) for id in products]
        if len(products) == 1:
            # Если только 1 товар
            suggestions = r.zrange(
                self.get_product_key(product_ids[0]),
                0,
                -1,
                desc=True
            )[:max_results]
        else:
            # Сгенирируем временный ключ
            flat_ids = ''.join([str(id) for id in products])
            tmp_key = f'Временный ключ_{flat_ids}'
            # Несколько товаров, обьединияем баллы всех продуктов
            # Сохраняем полученное сортированное множество
            # во временном ключе
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)
            # Удаляем идентификаторы продуктов, для которых дается рекомен-я
            r.zrem(tmp_key, *product_ids)
            # Получаем идентификаторы продуктов по их кол-ву
            # сортировка по убыванию
            suggestions = r.zrange(
                tmp_key,
                0,
                -1,
                desc=True
            )[:max_results]
            # Удаляем временный ключ
            r.delete(tmp_key)
        suggested_products_ids = [int(id) for id in products]
        suggested_products = list(Product.objects.filter(
            id__in=suggested_products_ids
        ))
        suggested_products.sort(
            key=lambda x: suggested_products_ids.index(x.id)
        )
        return suggested_products

    def clear_purchases(self):
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))
