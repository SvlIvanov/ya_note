from http import HTTPStatus

from .conf_test import TestBase


class TestRoutes(TestBase):

    def test_pages_availability(self):
        urls = (
            self.home_url,
            self.login_url,
            self.logout_url,
            self.signup_url,
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_note_add_and_list(self):
        urls = (
            self.url,
            self.note_url,
            self.url_done,
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_note_edit_and_delete(self):
        users_statuses = (
            (self.author_client, HTTPStatus.OK),
            (self.reader_client, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            for url in (self.detail_url, self.edit_url, self.delete_url):
                with self.subTest(user=user, url=url):
                    response = user.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        urls = (
            self.detail_url,
            self.edit_url,
            self.delete_url,
            self.url,
            self.note_url,
            self.url_done,
        )
        for url in urls:
            with self.subTest(url=url):
                redirect_url = f'{self.login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
