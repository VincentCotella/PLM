# products/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone

class ProductRange(models.Model):
    CATEGORY_CHOICES = [
        ('AG', 'Agrifood'),
        ('PE', 'Perfumery'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.get_category_display()} - {self.name}"

class Site(models.Model):
    LOCATION_CHOICES = [
        ('FR', 'France'),
        ('BE', 'Belgium'),
        ('AS', 'Asia'),
        ('AF', 'Africa'),
    ]

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=2, choices=LOCATION_CHOICES)
    capacity = models.PositiveIntegerField(help_text="Production capacity in units")
    is_active = models.BooleanField(default=True)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Latitude for mapping (e.g., 48.8566)"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Longitude for mapping (e.g., 2.3522)"
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Production Site'
        verbose_name_plural = 'Production Sites'

    def __str__(self):
        return f"{self.name} ({self.get_location_display()})"

    def clean(self):
        if self.capacity <= 0:
            raise ValidationError({'capacity': 'Capacity must be greater than 0'})
        if (self.latitude and not self.longitude) or (self.longitude and not self.latitude):
            raise ValidationError('Both latitude and longitude must be provided together.')

    def can_be_deleted(self):
        return self.product_set.count() == 0

class Equipment(models.Model):
    STATUS_CHOICES = [
        ('Operational', 'Operational'),
        ('Under Maintenance', 'Under Maintenance'),
        ('Out of Service', 'Out of Service'),
    ]

    site = models.ForeignKey(Site, related_name='equipment', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    equipment_type = models.CharField(max_length=100)
    maintenance_due = models.DateField(null=True, blank=True, help_text="Next maintenance date")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Operational')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Equipment'
        verbose_name_plural = 'Equipment'

    def __str__(self):
        return f"{self.name} ({self.equipment_type}) - {self.site.name}"

    def clean(self):
        super().clean()
        if self.maintenance_due:
            reference_date = self.created_at.date() if self.created_at else timezone.now().date()
            if self.maintenance_due < reference_date:
                raise ValidationError({'maintenance_due': 'Maintenance due date cannot be in the past.'})

class Product(models.Model):
    reference = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    product_range = models.ForeignKey(ProductRange, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, blank=True)

    is_modified = models.BooleanField(default=False)
    version_number = models.PositiveIntegerField(default=1)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stl_file = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Google Drive file ID for the STL file"
    )
    
    def save(self, *args, **kwargs):
        if not self.reference:
            prefix = 'AG_' if self.product_range.category == 'AG' else 'PE_'
            self.reference = f"{prefix}00{'M' if self.is_modified else 'S'}{self.version_number:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference} - {self.name} (v{self.version_number})"

class CostSimulation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cost_simulations')
    raw_material_cost = models.DecimalField(max_digits=10, decimal_places=2)
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2)
    overhead_cost = models.DecimalField(max_digits=10, decimal_places=2)
    production_cost = models.DecimalField(max_digits=10, decimal_places=2)
    margin = models.DecimalField(max_digits=5, decimal_places=2)
    calculated_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_price(self):
        self.production_cost = self.raw_material_cost + self.labor_cost + self.overhead_cost
        self.calculated_price = self.production_cost * (1 + self.margin / 100)
        return self.calculated_price

    def save(self, *args, **kwargs):
        self.calculate_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cost Simulation for {self.product.name} - {self.created_at}"

class BOM(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    requirements = models.TextField()
    manufacturing_process = models.TextField()
    resources = models.TextField()

    def __str__(self):
        return f"BOM for {self.product.name}"

class CustomerRequirement(models.Model):
    PRIORITY_CHOICES = [
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.TextField()
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')
    
    def __str__(self):
        return f"Requirement for {self.product.name}: {self.description[:50]} ({self.get_priority_display()})"

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, default='In Progress')
    products = models.ManyToManyField(Product, related_name='projects')
    project_manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Project: {self.name} - {self.status}"

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory')
    quantity = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Inventory of {self.product.name}: {self.quantity}"

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')
    quantity = models.PositiveIntegerField(default=0)
    sale_date = models.DateTimeField(auto_now_add=True)
    customer = models.CharField(max_length=100, null=True, blank=True)
    salesperson = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Sale of {self.product.name}: {self.quantity} units on {self.sale_date}"

# Nouveau modèle de log générique pour suivre toutes les modifications
class ChangeLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    change_description = models.TextField()
    date_modified = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_modified']

    def __str__(self):
        return f"Change by {self.user or 'N/A'} on {self.content_type} (ID: {self.object_id}) at {self.date_modified}"
