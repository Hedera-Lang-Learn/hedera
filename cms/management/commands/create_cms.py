from django.core.management.base import BaseCommand

from wagtail.core.models import Page, Site

from cms.models import HomePage


class Command(BaseCommand):
    help = 'Create the CMS structure for Hedera.'

    def create_cms(self):
        Page.objects.last().delete()
        root = Page.get_first_root_node()
        home = root.add_child(
            instance=HomePage(**{"title": "The Hedera Project", "slug": ""})
        )

        Site.objects.all().delete()
        Site.objects.create(
            hostname='localhost',
            site_name='Hedera',
            root_page=home,
            is_default_site=True
        )

    def handle(self, *args, **options):
        self.create_cms()
        for page in Page.objects.all():
            if not page.is_root():
                page.specific.save_revision().publish()

        self.stdout.write(self.style.SUCCESS('Created Hedera'))
