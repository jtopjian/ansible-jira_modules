#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.jira_common import JiraModuleBase
from ansible.module_utils.six.moves.urllib.parse import quote, urlencode

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
module: jira_get_project_fact
version_added: "0.0.1"
short_description: get a project in Jira
description:
  - Get a project in Jira

extends_documentation_fragment:
  - jira_modules_common

options:
  id:
    required: false
    description:
      - Query for a project by its ID.
      - This parameter is mutually exclusive with C(key).

  key:
    required: false
    description:
      - Query for a project by its Jira Key.
      - This parameter is mutually exclusive with C(id).

author: "Joe Topjian <joe@topjian.net>"
"""

RETURN = """
ansible_facts:
  description: facts to add to ansible_facts
  returned: always
  type: complex
  contains:
    jira_project:
      type: dict
      description:
        - A Jira project.
        - See
          https://docs.atlassian.com/software/jira/docs/api/REST/8.6.0/#api/2/project-getProject
          for the schema.
      returned: When a Jira project was detected.
"""

EXAMPLES = """
- name: Get a project
  jira_get_project_fact:
    jira_url: '{{ server }}'
    jira_username: '{{ user }}'
    jira_password: '{{ pass }}'
    key: 'PROJ'
"""

REST_ENDPOINT = "rest/api/2/project"


class JiraGetProject(JiraModuleBase):
    """Utility class to get a Jira project as facts"""

    def __init__(self):
        self.module_args = dict(
            id=dict(),
            key=dict(),
        )

        self.results = dict(
            ansible_facts=dict(
                jira_project=dict()
            ),
            changed=False,
        )

        super(JiraGetProject, self).__init__(
            derived_arg_spec=self.module_args,
            facts_module=True,
            mutually_exclusive=[['id', 'key']],
            required_one_of=[['id', 'key']],
            rest_endpoint=REST_ENDPOINT,
        )

    def exec_module(self, **kwargs):
        v = self.param('id')
        if v is not None:
            self.rest_endpoint = "%s/%s" % (self.rest_endpoint, quote(v))

        v = self.param('key')
        if v is not None:
            self.rest_endpoint = "%s/%s" % (self.rest_endpoint, quote(v))

        q = {
            'expand': ','.join(['description', 'lead', 'url', 'projectKeys'])
        }
        query = urlencode(q)

        try:
            v = self.get(query)
            if v is False:
                del(self.results['ansible_facts']['jira_project'])
            else:
                self.results['ansible_facts']['jira_project'] = v
        except Exception as e:
            self.fail(msg=e.message)


if __name__ == '__main__':
    JiraGetProject()
