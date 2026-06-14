from django.core.management.base import BaseCommand

from accounts.models import User
from faq.models import FAQ
from tickets.models import Ticket


class Command(BaseCommand):
    help = 'Seed admin, agent accounts and sample FAQ data'

    def handle(self, *args, **options):
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@company.com',
                'first_name': 'System',
                'last_name': 'Admin',
                'role': User.Role.ADMIN,
                'is_staff': True,
                'is_superuser': True,
            },
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('Created admin (admin / admin123)'))
        else:
            self.stdout.write('Admin user already exists')

        agent, created = User.objects.get_or_create(
            username='agent1',
            defaults={
                'email': 'agent@company.com',
                'first_name': 'Support',
                'last_name': 'Agent',
                'role': User.Role.AGENT,
            },
        )
        if created:
            agent.set_password('agent123')
            agent.save()
            self.stdout.write(self.style.SUCCESS('Created agent (agent1 / agent123)'))
        else:
            self.stdout.write('Agent user already exists')

        faqs = [
            {
                'question': 'How do I create a support ticket?',
                'answer': 'Log in as an employee, go to Create Ticket, fill in the title, description, and priority, then submit.',
            },
            {
                'question': 'How long does ticket resolution take?',
                'answer': 'Response times vary by priority. High priority tickets are handled within 4 hours.',
            },
            {
                'question': 'Can I close my own ticket?',
                'answer': 'Yes. Employees can close their own tickets from the ticket detail page once the issue is resolved.',
            },
        ]
        for item in faqs:
            FAQ.objects.get_or_create(question=item['question'], defaults=item)

        self.stdout.write(self.style.SUCCESS('FAQ entries seeded'))

        employee = User.objects.filter(username='employee1').first()
        if not employee:
            employee = User.objects.create_user(
                username='employee1',
                email='employee@company.com',
                password='employee123',
                first_name='John',
                last_name='Employee',
                role=User.Role.EMPLOYEE,
            )
            self.stdout.write(
                self.style.SUCCESS('Created employee (employee1 / employee123)')
            )

        if not Ticket.objects.exists():
            ticket = Ticket.objects.create(
                title='Cannot access email',
                description='I am unable to log into my company email account since this morning.',
                priority=Ticket.Priority.HIGH,
                status=Ticket.Status.OPEN,
                created_by=employee,
                assigned_to=agent,
            )
            self.stdout.write(self.style.SUCCESS(f'Created sample ticket #{ticket.id}'))

        self.stdout.write(self.style.SUCCESS('Seed data complete!'))
