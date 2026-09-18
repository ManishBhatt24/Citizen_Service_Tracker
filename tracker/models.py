from django.db import models

CATEGORIES = ["Water", "Electricity", "Road", "Sanitation"]
STATUS_CHOICES = ["Pending", "In Progress", "Resolved"]

class Complaint(models.Model):
    CATEGORY_CHOICES = [(cat, cat) for cat in CATEGORIES]
    STATUS_CHOICES_TUPLES = [(st, st) for st in STATUS_CHOICES]

    citizen_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES_TUPLES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"Complaint #{self.pk} - {self.category} ({self.status})"
