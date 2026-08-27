from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from providers.models import ProviderProfile, ProviderService
from services.models import ServiceCategory
from accounts.models import CustomerProfile


class Command(BaseCommand):
    help = 'Seed Servora with realistic demo categories and providers.'

    def handle(self, *args, **options):
        User = get_user_model()
        categories = [
            ('Electrician', 'Wiring, fixtures, panels, and urgent electrical repairs.'),
            ('Plumber', 'Leak repairs, pipe work, bathrooms, and water systems.'),
            ('Mechanic', 'Two-wheeler and car diagnostics, repair, and servicing.'),
            ('AC Repair', 'Installation, gas refill, cleaning, and AC troubleshooting.'),
            ('Computer Repair', 'Laptop, desktop, printer, network, and data support.'),
            ('Mobile Repair', 'Screen, battery, charging, software, and diagnostics.'),
            ('Tutor', 'Home tutoring for school, college, and competitive exams.'),
            ('Cleaner', 'Home deep cleaning, kitchen, bathroom, and office cleaning.'),
            ('Carpenter', 'Furniture repair, custom shelves, doors, and fittings.'),
            ('Painter', 'Interior, exterior, waterproofing, and texture painting.'),
            ('Appliance Repair', 'Fridge, washing machine, microwave, and appliance service.'),
            ('Home Maintenance', 'General repairs and preventive maintenance packages.'),
        ]
        category_objs = []
        for name, description in categories:
            obj, _ = ServiceCategory.objects.get_or_create(
                slug=slugify(name),
                defaults={'name': name, 'description': description, 'icon': name[:3].upper()},
            )
            category_objs.append(obj)

        names = [
            'PrimeFix Electricals', 'BluePipe Plumbing', 'NorthEast Auto Care', 'CoolAir Experts',
            'ByteCare Computers', 'QuickMobile Repair', 'BrightPath Tutors', 'Sparkle Home Clean',
            'CraftLine Carpentry', 'ColorNest Painters', 'AppliancePro', 'Urban HomeCare',
            'SafeWire Services', 'AquaRoot Plumbers', 'GearBox Garage', 'FrostPoint AC',
            'TechNest Support', 'PhoneRescue', 'ScholarPoint', 'CleanSwift',
        ]
        for index, business_name in enumerate(names):
            user, _ = User.objects.get_or_create(
                username=f'provider{index + 1}',
                defaults={'email': f'provider{index + 1}@servora.local', 'role': User.PROVIDER},
            )
            user.set_password('Provider@123')
            user.save()
            category = category_objs[index % len(category_objs)]
            provider, _ = ProviderProfile.objects.get_or_create(
                user=user,
                defaults={
                    'business_name': business_name,
                    'bio': f'{business_name} provides reliable {category.name.lower()} services with transparent pricing and prompt local support.',
                    'experience_years': 2 + (index % 12),
                    'service_area': 'Tinsukia and nearby areas',
                    'base_location': 'Tinsukia',
                    'verification_status': ProviderProfile.APPROVED,
                    'emergency_available': index % 3 == 0,
                    'response_rate': 75 + (index % 20),
                    'cancellation_rate': index % 8,
                    'completed_jobs': 15 + index * 6,
                    'average_rating': Decimal('4.10') + Decimal(index % 8) / Decimal('10'),
                    'trust_score': min(98, 72 + index),
                },
            )
            ProviderService.objects.get_or_create(
                provider=provider,
                category=category,
                title=f'{category.name} Service',
                defaults={'description': category.description, 'starting_price': Decimal(299 + index * 25)},
            )

        customer, _ = User.objects.get_or_create(
            username='customer1',
            defaults={'email': 'customer1@servora.local', 'role': User.CUSTOMER, 'first_name': 'Demo'},
        )
        customer.set_password('Customer@123')
        customer.save()
        CustomerProfile.objects.get_or_create(
            user=customer,
            defaults={'city': 'Tinsukia', 'address': 'AT Road, Tinsukia'},
        )
        self.stdout.write(self.style.SUCCESS('Seeded categories, 20 providers, and demo users.'))
