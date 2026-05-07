from django.db import models


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.name

class Service(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(max_length=750, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='services_category')
    billing_model = models.CharField(max_length=255, blank=False, null=False)
    price = models.FloatField(blank=True, null=True)
    photo = models.ImageField(upload_to='service/' , blank=True, null=True)
    value_generated = models.TextField(max_length=750, blank=True, null=True)

    @property
    def formatted_price(self):
        if self.price is not None:
            return f"R$ {self.price:.2f}"
        return "N/A"
    

    def __str__(self):
        return self.name
    

class ServiceInventary(models.Model):
    services_count = models.IntegerField()
    services_value = models.FloatField()
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


    def __str__(self):
        return f'self.services_count - {self.services_count} | self.services_value - {self.services_value} '