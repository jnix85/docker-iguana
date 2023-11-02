"""
Iguana (c) by Marc Ammon, Moritz Fickenscher, Lukas Fridolin,
Michael Gunselmann, Katrin Raab, Christian Strate

Iguana is licensed under a
Creative Commons Attribution-ShareAlike 4.0 International License.

You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.
"""
from django.test import TestCase
from django.urls import reverse

from unittest.mock import patch

from project.models import Project
from integration.models import SlackIntegration
from django.contrib.auth import get_user_model
from integration.views import SlackIntegrationOAuthView

try:
    from common.settings import SLACK_SECRET, SLACK_VERIFICATION, SLACK_ID, HOST
except ImportError:
    SLACK_ID = None


class ViewTest(TestCase):
    short = 'proj'

    @classmethod
    def setUpTestData(cls):
        # NOTE: if you modify those elements they need to be created in setUp, instead of here
        cls.user = get_user_model().objects.create_user('a', 'b', 'c')
        cls.user2 = get_user_model().objects.create_user('d', 'e', 'f')
        cls.project = Project(creator=cls.user, name_short=cls.short)
        cls.project.save()
        cls.project.developer.set((cls.user.pk,))
        cls.project.manager.set((cls.user.pk,))
        cls.project.save()

    def setUp(self):
        self.client.force_login(self.user)
        self.si = SlackIntegration(api_token="token", channel="channel")
        self.si.project = self.project
        self.si.save()

    def test_redirect_to_login_and_login_required(self):
        self.client.force_login(self.user2)

        response = self.client.post(reverse('integration:slack:update', kwargs={'pk': 1, 'project': self.short}),
                                    {'channel': 'foo'},
                                    follow=True
                                    )
        self.assertContains(response, "Your account doesn't have access to this page")
        si = SlackIntegration.objects.get(pk=self.si.pk)
        self.assertEqual(si.channel, 'channel')

        response = self.client.post(reverse('integration:slack:delete', kwargs={'pk': 1, 'project': self.short}),
                                    {'delete': True},
                                    follow=True
                                    )
        self.assertContains(response, "Your account doesn't have access to this page")
        si = SlackIntegration.objects.get(pk=self.si.pk)
        self.assertEqual(si.channel, 'channel')

        self.client.force_login(self.user)

    def test_user_passes_test_mixin(self):
        # TODO TESTCASE
        # TODO only devs are allowed to edit an integration
        # TODO how about creation of integrations?
        pass

    def test_form(self):
        response = self.client.post(
            reverse('integration:slack:update', kwargs={'pk': 1, 'project': self.short}),
            {'channel': 'foo'}
        )
        self.assertRedirects(response, reverse('project:edit', kwargs={'project': self.short}))
        si = SlackIntegration.objects.get(pk=self.si.pk)
        self.assertEqual(si.channel, "foo")

    def test_delete_slackintegration(self):
        response = self.client.post(reverse('integration:slack:delete', kwargs={'pk': 1, 'project': self.short}),
                                    {'delete': 'true'})
        self.assertRedirects(response, reverse('project:edit', kwargs={'project': self.short}))
        self.assertEqual(len(SlackIntegration.objects.all()), 0)

    def test_keep_and_dont_delete_slackintegration(self):
        response = self.client.post(reverse('integration:slack:delete', kwargs={'pk': 1, 'project': self.short}),
                                    {'keep': 'true'})
        self.assertRedirects(response, reverse('project:edit', kwargs={'project': self.short}))
        self.assertEqual(len(SlackIntegration.objects.all()), 1)

    @patch('integration.views.SlackClient')
    def test_oauth_view_not_ok(self, slackmock):
        slackmock().api_call.return_value = {'ok': False}
        response = self.client.post(reverse('integration:slack:auth', kwargs={'project': self.short}) + "?code=foo")
        self.assertRedirects(response, reverse('project:edit', kwargs={'project': self.short}))
        slackmock.assert_called_with('')
        slackmock().api_call.assert_called_with(
            "oauth.access",
            code="foo",
            client_id=SLACK_ID,
            client_secret=SLACK_SECRET,
            redirect_uri="https://" + HOST + reverse("integration:slack:auth", kwargs={'project': self.short}),
        )

    @patch('integration.views.SlackClient')
    def test_oauth_view_ok(self, slackmock):
        slackmock().api_call.return_value = {'ok': True, 'access_token': "foo"}
        response = self.client.post(reverse('integration:slack:auth', kwargs={'project': self.short}) + "?code=foo")
        self.assertRedirects(response, reverse('integration:slack:update', kwargs={'pk': 2, 'project': self.short}))
        slackmock.assert_called_with('')
        slackmock().api_call.assert_called_with(
            "oauth.access",
            code="foo",
            client_id=SLACK_ID,
            client_secret=SLACK_SECRET,
            redirect_uri="https://" + HOST + reverse("integration:slack:auth", kwargs={'project': self.short}),
        )
