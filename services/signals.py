from django.db.models.signals import post_save, pre_delete, pre_save, post_delete
from django.db.models import Sum
from django.dispatch import receiver
from services.models import Service, ServiceInventary
from openai_api.client import get_service_ai_value


def service_inventary_update():
    services_count = Service.objects.count()
    services_price = Service.objects.aggregate(
        total_value=Sum('price')
    )['total_value'] or 0

    ServiceInventary.objects.create(
        services_count=services_count,
        services_value=services_price
    )


@receiver(post_save, sender=Service)
def service_post_save(sender, instance, created, **kwargs):
    if created:
        print(f"[POST SAVE] Novo serviço criado: {instance.name}")
    else:
        print(f"[POST SAVE] Serviço atualizado: {instance.name}")

    service_inventary_update()


@receiver(post_delete, sender=Service)
def service_post_delete(sender, instance, **kwargs):
    service_inventary_update()


@receiver(pre_save, sender=Service)
def service_pre_save(sender, instance, **kwargs):
    ai_value = get_service_ai_value(
        instance.name, instance.category)
    instance.bio = ai_value