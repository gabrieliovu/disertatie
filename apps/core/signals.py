from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TextComparison
from .tasks import task_preprocessing


@receiver(post_save, sender=TextComparison)
def handle_text_comparison_save(sender, instance, created, **kwargs):
    updated_fields = kwargs.get('update_fields', None)
    if created:
        task_preprocessing.delay(instance)
    elif updated_fields and ('first_text' in updated_fields or 'second_text' in updated_fields):
        print(f"TextComparison with ID {instance.id} has updated first_text or second_text")
        task_preprocessing.delay(instance)
