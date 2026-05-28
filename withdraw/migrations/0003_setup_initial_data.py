from django.db import migrations
from django.contrib.auth.models import User
from decimal import Decimal

def create_superuser(apps, schema_editor):
    # Use the User model directly as it's a standard Django model
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')

def create_starlink_packages(apps, schema_editor):
    StarlinkPackage = apps.get_model('withdraw', 'StarlinkPackage')
    
    packages = [
        {
            'name': 'Basic',
            'description': 'Basic Starlink Plan',
            'price': Decimal('15.00'),
            'data_limit': 'Basic'
        },
        {
            'name': 'Standard',
            'description': 'Standard Starlink Plan',
            'price': Decimal('25.00'),
            'data_limit': 'Standard'
        },
        {
            'name': 'Premium Plan',
            'description': 'Premium Starlink Plan',
            'price': Decimal('45.00'),
            'data_limit': 'Premium'
        },
        {
            'name': 'Unlimited Plan',
            'description': 'Unlimited Starlink Plan',
            'price': Decimal('95.00'),
            'data_limit': 'Unlimited'
        },
    ]
    
    for pkg_data in packages:
        StarlinkPackage.objects.get_or_create(
            name=pkg_data['name'],
            defaults={
                'description': pkg_data['description'],
                'price': pkg_data['price'],
                'data_limit': pkg_data['data_limit'],
                'is_active': True
            }
        )

class Migration(migrations.Migration):

    dependencies = [
        ('withdraw', '0002_rename_link_count_starlinkorder_otp_count_and_more'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
        migrations.RunPython(create_starlink_packages),
    ]
