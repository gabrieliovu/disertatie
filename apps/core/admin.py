from django.contrib import admin
from django.contrib.auth.models import User, Group

from django_celery_results.models import TaskResult, GroupResult
from django_celery_results.admin import TaskResultAdmin

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(TaskResult)
admin.site.unregister(GroupResult)
