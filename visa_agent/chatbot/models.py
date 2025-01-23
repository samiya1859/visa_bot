from django.db import models

class VisaSearch(models.Model):
    country = models.CharField(max_length=100)
    visa_type = models.CharField(max_length=100)
    embassy_url = models.URLField(null=True, blank=True)
    visa_information = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']