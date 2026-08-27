from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from bookings.models import Booking, Quote
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
        coordinates = [
            (Decimal('27.488600'), Decimal('95.355800')), (Decimal('27.492000'), Decimal('95.346500')),
            (Decimal('27.481500'), Decimal('95.364000')), (Decimal('27.500400'), Decimal('95.352000')),
            (Decimal('27.474900'), Decimal('95.358200')), (Decimal('27.496800'), Decimal('95.371100')),
            (Decimal('27.486100'), Decimal('95.337900')), (Decimal('27.509000'), Decimal('95.362600')),
            (Decimal('27.469800'), Decimal('95.347200')), (Decimal('27.503200'), Decimal('95.382500')),
            (Decimal('27.477700'), Decimal('95.374700')), (Decimal('27.515100'), Decimal('95.351200')),
            (Decimal('27.490700'), Decimal('95.390000')), (Decimal('27.461900'), Decimal('95.360200')),
            (Decimal('27.521300'), Decimal('95.369400')), (Decimal('27.484400'), Decimal('95.326700')),
            (Decimal('27.472800'), Decimal('95.387600')), (Decimal('27.508600'), Decimal('95.333300')),
            (Decimal('27.456700'), Decimal('95.342200')), (Decimal('27.518800'), Decimal('95.392200')),
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
                    'latitude': coordinates[index][0],
                    'longitude': coordinates[index][1],
                    'verification_status': ProviderProfile.APPROVED,
                    'emergency_available': index % 3 == 0,
                    'response_rate': 75 + (index % 20),
                    'cancellation_rate': index % 8,
                    'completed_jobs': 15 + index * 6,
                    'average_rating': Decimal('4.10') + Decimal(index % 8) / Decimal('10'),
                    'trust_score': min(98, 72 + index),
                },
            )
            provider.latitude = coordinates[index][0]
            provider.longitude = coordinates[index][1]
            provider.save(update_fields=['latitude', 'longitude'])
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
        demo_services = ProviderService.objects.select_related('provider')[:6]
        for index, service in enumerate(demo_services):
            booking, _ = Booking.objects.get_or_create(
                customer=customer,
                provider=service.provider,
                provider_service=service,
                defaults={
                    'scheduled_for': timezone.now() + timezone.timedelta(days=index + 1),
                    'address': 'AT Road, Tinsukia',
                    'problem_description': f'Demo booking for {service.title}.',
                    'contact_preference': 'phone',
                    'status': Booking.CONFIRMED if index % 2 == 0 else Booking.PENDING,
                    'estimated_amount': service.starting_price,
                },
            )
            Quote.objects.get_or_create(
                booking=booking,
                provider=service.provider,
                defaults={
                    'estimated_price': service.starting_price + Decimal('150.00'),
                    'service_description': f'Inspection and service for {service.title}.',
                    'expected_completion_time': 'Same day',
                    'notes': 'Final amount may vary after inspection.',
                    'expires_at': timezone.now() + timezone.timedelta(days=2),
                },
            )
        self.stdout.write(self.style.SUCCESS('Seeded categories, 20 providers, and demo users.'))
