from django.db import models


class SimilarityDetails(models.Model):
    similar_phrases = models.TextField()
    identic_phrases = models.TextField()

    similarity = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Similar Phrases: {self.similar_phrases} \n Identic Phrases: {self.identic_phrases} \n Similarity: {self.similarity}"


class TextComparison(models.Model):
    first_text = models.TextField()
    second_text = models.TextField()

    first_text_preprocessed = models.TextField(null=True, blank=True)
    first_text_tokens = models.JSONField(null=True, blank=True)
    second_text_preprocessed = models.TextField(null=True, blank=True)
    second_text_tokens = models.JSONField(null=True, blank=True)

    wmdistance = models.ForeignKey(SimilarityDetails, related_name='wmdistance_comparisons', null=True, blank=True,
                                   on_delete=models.SET_NULL)
    sequence_matcher = models.ForeignKey(SimilarityDetails, related_name='sequence_matcher_comparisons', null=True,
                                         blank=True, on_delete=models.SET_NULL)
    cosine_similarity = models.ForeignKey(SimilarityDetails, related_name='cosine_similarity_comparisons', null=True,
                                          blank=True, on_delete=models.SET_NULL)

    overall_similarity = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=0)

    def __str__(self):
        return f"Comparison of texts {self.id}"

    def save(self, *args, **kwargs):
        if not self.wmdistance:
            self.wmdistance = SimilarityDetails.objects.create()
        if not self.sequence_matcher:
            self.sequence_matcher = SimilarityDetails.objects.create()
        if not self.cosine_similarity:
            self.cosine_similarity = SimilarityDetails.objects.create()
        import ipdb; ipdb.set_trace()
        super(TextComparison, self).save(*args, **kwargs)
