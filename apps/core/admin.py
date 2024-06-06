from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import TextComparison, SimilarityDetails

from django_celery_results.models import TaskResult, GroupResult
from django_celery_results.admin import TaskResultAdmin

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(TaskResult)
admin.site.unregister(GroupResult)


@admin.register(SimilarityDetails)
class SimilarityDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'similar_phrases', 'identic_phrases', 'similarity')
    search_fields = ('similar_phrases', 'identic_phrases')
    list_filter = ('similarity',)


@admin.register(TextComparison)
class TextComparisonAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_first_text_snippet', 'get_second_text_snippet', 'overall_similarity')
    search_fields = ('first_text', 'second_text')
    list_filter = ('overall_similarity',)

    def get_first_text_snippet(self, obj):
        return obj.first_text[:50] + '...'

    get_first_text_snippet.short_description = 'First Text'

    def get_second_text_snippet(self, obj):
        return obj.second_text[:50] + '...'

    get_second_text_snippet.short_description = 'Second Text'

    def get_readonly_fields(self, request, obj=None):
        if obj:  # obj is None when creating a new object, so set fields as read-only only when editing
            return ['first_text_preprocessed', 'first_text_tokens', 'second_text_preprocessed', 'second_text_tokens',
                    'wmdistance', 'sequence_matcher', 'cosine_similarity', 'overall_similarity']
        return []

    fieldsets = (
        (None, {
            'fields': ('first_text', 'second_text')
        }),
        ('Read-Only Fields', {
            'classes': ('collapse',),
            'fields': ('first_text_preprocessed', 'first_text_tokens', 'second_text_preprocessed', 'second_text_tokens',
                       'wmdistance', 'sequence_matcher', 'cosine_similarity', 'overall_similarity'),
        }),
    )
