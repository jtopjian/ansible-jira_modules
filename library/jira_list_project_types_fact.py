#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.jira_common import JiraModuleBase

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
module: jira_list_project_types_fact
version_added: "0.0.1"
short_description: list project types in Jira
description:
  - List project types in Jira

extends_documentation_fragment:
  - jira_modules_common

author: "Joe Topjian <joe@topjian.net>"
"""

RETURN = """
ansible_facts:
  description: facts to add to ansible_facts
  returned: always
  type: complex
  contains:
    jira_project_types:
      type: list
      description:
        - Maps Jira project types to a non-empty list of dicts with
          project types information.
        - See
          https://docs.atlassian.com/software/jira/docs/api/REST/8.6.0/#api/2/project/type-getAllProjectTypes
          for the schema.
      returned: When Jira project types are detected.
"""

EXAMPLES = """
- name: List Project Types
  jira_list_project_types_fact:
"""

REST_ENDPOINT = "rest/api/2/project/type"


class JiraListProjectTypes(JiraModuleBase):
    """Utility class to get list of Jira project types as facts"""

    def __init__(self):
        self.module_args = dict()

        self.results = dict(
            ansible_facts=dict(
                jira_project_types=[],
            ),
            changed=False,
        )

        super(JiraListProjectTypes, self).__init__(
            derived_arg_spec=self.module_args,
            facts_module=True,
            rest_endpoint=REST_ENDPOINT,
        )

    def exec_module(self, **kwargs):
        try:
            v = self.get()
            if v is False:
                del(self.results['ansible_facts']['jira_project_types'])
            else:
                self.results['ansible_facts']['jira_project_types'] = v
        except Exception as e:
            self.fail(msg=e.message)


if __name__ == '__main__':
    JiraListProjectTypes()
