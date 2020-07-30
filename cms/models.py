from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.blocks import ImageChooserBlock


class HomePage(Page):
    subpage_types = ['cms.FlatPage']


class AbstractFlatPage(Page):
    body = StreamField([
        ('text', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    class Meta:
        abstract = True


class FlatPage(AbstractFlatPage):
    parent_page_types = ['cms.HomePage']
    subpage_types = ['cms.SubPage']


class SubPage(AbstractFlatPage):
    template = 'cms/flat_page.html'

    parent_page_types = ['cms.FlatPage']
    subpage_types = []
