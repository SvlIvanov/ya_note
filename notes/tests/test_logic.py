from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from .conf_test import TestBase


class TestCommentCreation(TestBase):

    def test_anonymous_user_cant_create_note(self):
        self.client.post(self.url, data=self.form_data)
        note_count = Note.objects.count()
        self.assertEqual(note_count, self.notes_count)

    def test_user_can_create_note(self):
        Note.objects.all().delete()
        response = self.author_client.post(self.url, data=self.form_data)
        self.assertRedirects(response, self.url_done)
        note_count = Note.objects.count()
        note = Note.objects.get()
        self.assertEqual(note_count, 1)
        self.assertEqual(note.title, self.form_data.get('title'))
        self.assertEqual(note.text, self.form_data.get('text'))
        self.assertEqual(note.slug, self.form_data.get('slug'))
        self.assertEqual(note.author, self.author)

    def test_slug(self):
        Note.objects.all().delete()
        self.form_data.pop('slug')
        response = self.author_client.post(self.url, data=self.form_data)
        self.assertRedirects(response, self.url_done)
        note_count = Note.objects.count()
        self.assertEqual(note_count, 1)
        expected_slug = slugify(self.form_data['title'])
        new_note = Note.objects.get()
        self.assertEqual(new_note.slug, expected_slug)


class TestNoteEditDelete(TestBase):

    def test_author_can_edit_note(self):
        response = self.author_client.post(self.edit_url, data=self.form_data)
        self.assertRedirects(response, self.url_done)
        note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(note.text, self.form_data.get('text'))
        self.assertEqual(note.title, self.form_data.get('title'))
        self.assertEqual(note.slug, self.form_data.get('slug'))
        self.assertEqual(note.author, self.note.author)

    def test_author_can_delete_note(self):
        response = self.author_client.delete(self.delete_url)
        self.assertRedirects(response, self.url_done)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, self.notes_count - 1)

    def test_user_cant_edit_note_of_another_user(self):
        response = self.reader_client.post(self.edit_url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)

    def test_user_cant_delete_note_of_another_user(self):
        response = self.reader_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, self.notes_count)

    def test_not_unique_slug(self):
        self.form_data['slug'] = self.note_slug
        response = self.author_client.post(self.url,
                                           data=self.form_data)
        self.assertEqual(Note.objects.count(), self.notes_count)
        self.assertFormError(response, 'form', 'slug',
                             errors=(self.note_slug + WARNING))
