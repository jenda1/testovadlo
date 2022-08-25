from django.db import models

from wagtail.models import Page
from django.db.models import DateField
from wagtail.fields import RichTextField
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.blocks import ImageChooserBlock

from wagtailmarkdown.fields import MarkdownField
from wagtailcodeblock.blocks import CodeBlock


class LessonContentBlock(blocks.StructBlock):
    type = blocks.ChoiceBlock(
        choices=[
            ('chapter', 'Chapter'),
            ('section', 'Section'),
            ('subsection', 'SubSection'),
        ],
        required=True
    )

    heading = blocks.CharBlock(required=True)

    body = blocks.StreamBlock([
        ('paragraph', blocks.RichTextBlock(features=["bold", "italic", "ol", "ul", "link", "document-link", "superscript", "subscript", "strikethrough"])),
        ('image', ImageChooserBlock()),
        ('code', CodeBlock()),
        ], required=True)

    class Meta:
        icon = 'user'
        template = "lessons/lesson_content_block.html"


class ClassSubjectPage(Page):
    subpage_types = ['lessons.LessonPage', 'lessons.LessonWikiPage']

    class SchoolYear(models.IntegerChoices):
        Y2021 = 21, '2021/2022'
        Y2022 = 22, '2022/2023'

    note = RichTextField(blank=True)

    school_year = models.IntegerField(
        choices=SchoolYear.choices,
        default=SchoolYear.Y2022,
    )

    content_panels = Page.content_panels + [
        FieldPanel('note'),
        FieldPanel('school_year'),
    ]

    def get_lessons(self):
        return LessonPage.objects.child_of(self).order_by('lesson_date')


class LessonPage(Page):
    page_description = "Lesson page"
    subpage_types = []

    lesson_date = DateField(null=True, blank=True)

    content = StreamField([
        ('block', LessonContentBlock()),
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('lesson_date'),
        FieldPanel('content'),
    ]


class LessonWikiPage(Page):
    subpage_types = []

    lesson_date = DateField(null=True, blank=True)
    content = MarkdownField()

    content_panels = Page.content_panels + [
        FieldPanel('lesson_date'),
        FieldPanel('content'),
    ]
