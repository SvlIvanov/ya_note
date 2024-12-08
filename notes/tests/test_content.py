from notes.forms import NoteForm
from notes.models import Note
from .conf_test import TestBase


class TestDetailPage(TestBase):

    def test_notes_for_reader(self):
        response = self.reader_client.get(self.note_url)
        notes = response.context['object_list']
        self.assertNotIn(self.notes, notes)

    def test_authorized_client_has_note(self):
        response = self.author_client.get(self.detail_url)
        self.assertIn('note', response.context)
        self.assertIsInstance(response.context['note'], Note)

    def test_authorized_client_has_form(self):
        response = self.author_client.get(self.edit_url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)

    def test_reader_not_has_note(self):
        response_reader = self.reader_client.get(self.note_url)
        object_list_reader = response_reader.context['object_list']
        response_author = self.author_client.get(self.note_url)
        object_list_author = response_author.context['object_list']
        self.assertNotIn(object_list_reader, object_list_author)
