"""
Iguana (c) by Marc Ammon, Moritz Fickenscher, Lukas Fridolin,
Michael Gunselmann, Katrin Raab, Christian Strate

Iguana is licensed under a
Creative Commons Attribution-ShareAlike 4.0 International License.

You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.
"""
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import Http404

from issue.models import Issue
from lib.custom_model import get_r_object_or_404
from tag.models import Tag
from project.models import Project
import bleach
from common.views import AutoCompleteView
from kanbancol.models import KanbanColumn
from django.utils.translation import ugettext_lazy as _


class UserAutocompleteView(AutoCompleteView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return get_user_model().objects.none()

        if not self.kwargs or not self.kwargs.get('project'):
            qs = get_user_model().objects.all()
        else:
            project = self.kwargs.get('project')
            try:
                proj = get_r_object_or_404(self.request.user, Project, name_short=project)
            except Http404:
                return get_user_model().objects.none()

            qs = proj.get_members()

        if self.q:
            qs = qs.filter(username__startswith=self.q)
        return qs

    def get_result_label_clean(self, result):
        return result.username

    def get_result_label_html(self, result):
        return '<img src="{}" width="25"><span style="padding-left: .5em">{}</span></img>'.format(result.avatar.url,
                                                                                                  result.username)


class IssueAutocompleteView(AutoCompleteView):
    def get_queryset(self):
        if not self.request.user.is_authenticated or not self.kwargs or not self.kwargs.get('project'):
            return Issue.objects.none()

        project = self.kwargs.get('project')
        try:
            proj = get_r_object_or_404(self.request.user, Project, name_short=project)
        except Http404:
            return Issue.objects.none()

        # get all issues of the project
        # first list the not-archived ones
        qs = proj.issue.all().order_by("archived")

        if self.kwargs.get('issue') is not None:
            # this happens in the issue edit view
            # the issue should not refer to itself, so exclude it
            issue = self.kwargs.get('issue')
            qs = qs.exclude(project__name_short=project, number=issue)

        if self.q:
            qs = qs.filter(Q(title__icontains=self.q) | Q(number__icontains=self.q))
        return qs

    def get_result_label_clean(self, result):
        return "{} {}".format(bleach.clean(result.get_ticket_identifier()), bleach.clean(result.title))

    def get_result_label_html(self, result):
        standard_html = '<strong>%s </strong>%s' % (
            bleach.clean(result.get_ticket_identifier()),
            bleach.clean(result.title)
        )

        # mark 'Done' issues
        if result.kanbancol.type == "Done":
            standard_html = '<del>%s</del><small style="padding-left: 1em">[%s]</small>' % (
                standard_html,
                result.kanbancol.get_type_display()
            )
        # mark archived issues
        if result.archived:
            standard_html = '<em class="text-muted">%s</em><small style="padding-left: 1em">[%s]</small>' % (
                standard_html,
                _("Archived")
            )

        return standard_html


class TagAutocompleteView(AutoCompleteView):
    def get_queryset(self):
        if not self.request.user.is_authenticated or not self.kwargs or not self.kwargs.get('project'):
            return Tag.objects.none()

        project = self.kwargs.get('project')
        try:
            proj = get_r_object_or_404(self.request.user, Project, name_short=project)
        except Http404:
            return Tag.objects.none()

        qs = Tag.objects.filter(project=proj)

        if self.q:
            qs = qs.filter(tag_text__icontains=self.q)
        return qs

    def get_result_label_clean(self, result):
        return bleach.clean(result.tag_text)

    def get_result_label_html(self, result):
        return """<div class="issue-tag" style="background: #{}; color: #{};" title="{}">
                  {}</div>""".format(bleach.clean(result.color),
                                     result.font_color,
                                     bleach.clean(result.tag_text),
                                     bleach.clean(result.tag_text))


class KanbanAutocompleteView(AutoCompleteView):
    def get_queryset(self):
        if not self.request.user.is_authenticated or not self.kwargs or not self.kwargs.get('project'):
            return KanbanColumn.objects.none()

        project = self.kwargs.get('project')
        try:
            proj = get_r_object_or_404(self.request.user, Project, name_short=project)
        except Http404:
            return KanbanColumn.objects.none()

        qs = KanbanColumn.objects.filter(project=proj)

        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

    def get_result_label(self, result):
        return result.name
