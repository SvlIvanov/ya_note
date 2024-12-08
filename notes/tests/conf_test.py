from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestBase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Простой читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.notes = Note.objects.bulk_create(
            Note(
                title=f'Заметка {index}',
                text='Просто текст.',
                slug=f'metka{index}',
                author=cls.author,
            )
            for index in range(1, 50)
        )
        cls.note_reader = Note.objects.create(
            title='Тестовая заметка',
            text='Просто текст.',
            slug='zametka',
            author=cls.reader,
        )
        cls.notes_count = Note.objects.count()
        cls.note_author_count = Note.objects.filter(author=cls.author).count()
        cls.note_reader_count = Note.objects.filter(author=cls.reader).count()
        cls.note_slug = cls.notes[0].slug
        cls.note = Note.objects.get(slug=cls.note_slug)
        cls.url = reverse('notes:add')
        cls.home_url = reverse('notes:home')
        cls.login_url = reverse('users:login')
        cls.logout_url = reverse('users:logout')
        cls.signup_url = reverse('users:signup')
        cls.detail_url = reverse('notes:detail', args=(cls.note_slug,))
        cls.edit_url = reverse('notes:edit', args=(cls.note_slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note_slug,))
        cls.url_done = reverse('notes:success')
        cls.note_url = reverse('notes:list')
        cls.form_data = {'text': 'Текст заметки', 'title': 'Текст заголовка',
                         'slug': 'newproch', 'author': cls.author_client}
