# your_app/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Gammes de Produits
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

# Site de production 
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

# Produits avec ajout du site de production et version
class Product(models.Model):
    reference = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    product_range = models.ForeignKey(ProductRange, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, blank=True)  # Ajout du site de production
    is_modified = models.BooleanField(default=False)
    version_number = models.PositiveIntegerField(default=1)  # Numéro de version pour la gestion des modifications
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
        # Générer la référence si elle n'existe pas
        if not self.reference:
            prefix = 'AG_' if self.product_range.category == 'AG' else 'PE_'
            self.reference = f"{prefix}00{'M' if self.is_modified else 'S'}{self.version_number:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference} - {self.name} (v{self.version_number})"

# Simulation de Coût pour les Produits
class CostSimulation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cost_simulations')
    raw_material_cost = models.DecimalField(max_digits=10, decimal_places=2)  # Coût des matières premières
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2)  # Coût de la main-d'œuvre
    overhead_cost = models.DecimalField(max_digits=10, decimal_places=2)  # Frais généraux (énergie, etc.)
    production_cost = models.DecimalField(max_digits=10, decimal_places=2)  # Coût total de production
    margin = models.DecimalField(max_digits=5, decimal_places=2)  # Marge bénéficiaire en pourcentage
    calculated_price = models.DecimalField(max_digits=10, decimal_places=2)  # Prix de vente calculé
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création de la simulation
    updated_at = models.DateTimeField(auto_now=True)  # Date de dernière mise à jour

    def calculate_price(self):
        # Calculer le coût total de production
        self.production_cost = self.raw_material_cost + self.labor_cost + self.overhead_cost
        # Calculer le prix de vente basé sur la marge
        self.calculated_price = self.production_cost * (1 + self.margin / 100)
        return self.calculated_price

    def save(self, *args, **kwargs):
        # Calculer le prix automatiquement avant de sauvegarder
        self.calculate_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cost Simulation for {self.product.name} - {self.created_at}"

# BOM (Bill of Materials)
class BOM(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    requirements = models.TextField()
    manufacturing_process = models.TextField()
    resources = models.TextField()

    def __str__(self):
        return f"BOM for {self.product.name}"

# Exigences Clients pour les Produits
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


# Gestion des Projets de Développement de Produits
class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, default='In Progress')  # Statut du projet (In Progress, Completed, etc.)
    products = models.ManyToManyField(Product, related_name='projects')  # Produits associés au projet
    project_manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Project: {self.name} - {self.status}"

# Gestion de l'Historique des Modifications
class ModificationHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    change_description = models.TextField()
    date_modified = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Change on {self.product.name} by {self.modified_by.username} at {self.date_modified}"
