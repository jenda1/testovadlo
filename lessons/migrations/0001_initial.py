# Generated by Django 4.1 on 2022-09-09 15:47

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtailmarkdown.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0076_modellogentry_revision'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassSubjectPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('note', wagtail.fields.RichTextField(blank=True)),
                ('school_year', models.IntegerField(choices=[(21, '2021/2022'), (22, '2022/2023')], default=22)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='LessonPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('lesson_date', models.DateField(blank=True, null=True)),
                ('content', wagtail.fields.StreamField([('block', wagtail.blocks.StructBlock([('type', wagtail.blocks.ChoiceBlock(choices=[('chapter', 'Chapter'), ('section', 'Section'), ('subsection', 'SubSection')])), ('heading', wagtail.blocks.CharBlock(required=True)), ('body', wagtail.blocks.StreamBlock([('paragraph', wagtail.blocks.RichTextBlock(features=['bold', 'italic', 'ol', 'ul', 'link', 'document-link', 'superscript', 'subscript', 'strikethrough'])), ('image', wagtail.images.blocks.ImageChooserBlock()), ('code', wagtail.blocks.StructBlock([('language', wagtail.blocks.ChoiceBlock(choices=[('java', 'Java'), ('bash', 'Bash/Shell'), ('python', 'Python'), ('css', 'CSS'), ('html', 'HTML'), ('javascript', 'Javascript'), ('json', 'JSON'), ('c', 'C')], help_text='Coding language', identifier='language', label='Language')), ('code', wagtail.blocks.TextBlock(identifier='code', label='Code'))]))], required=True))]))], use_json_field=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='LessonWikiPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('lesson_date', models.DateField(blank=True, null=True)),
                ('content', wagtailmarkdown.fields.MarkdownField()),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
