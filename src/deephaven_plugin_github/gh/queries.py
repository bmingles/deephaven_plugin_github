import os
import requests
from .debug import debug_json_dump

def create_project_items_query(project_id: str) -> str:
  prefix = """
query{
    node(id: \""""

  suffix = """\") {
        ... on ProjectV2 {
          items(first: 100) {
            nodes{
              id
              fieldValues(first: 8) {
                nodes{                
                  ... on ProjectV2ItemFieldTextValue {
                    text
                    field {
                      ... on ProjectV2FieldCommon {
                        name
                      }
                    }
                  }
                  ... on ProjectV2ItemFieldDateValue {
                    date
                    field {
                      ... on ProjectV2FieldCommon {
                        name
                      }
                    }
                  }
                  ... on ProjectV2ItemFieldSingleSelectValue {
                    name
                    field {
                      ... on ProjectV2FieldCommon {
                        name
                      }
                    }
                  }
                  ... on ProjectV2ItemFieldIterationValue {
                    __typename
                    title
                    field {
                      ... on ProjectV2IterationField {
                        __typename
                        id
                        name
                      }
                    }
                  }
                }              
              }
              content{              
                ... on DraftIssue {
                  __typename
                  title
                  body
                  assignees(first: 10) {
                    nodes{
                      login
                    }
                  }
                }
                ...on Issue {
                  __typename
                  number
                  title
                  repository {
                    name
                    nameWithOwner
                  }
                  milestone {
                    title
                  }
                  assignees(first: 10) {
                    nodes{
                      login
                    }
                  }
                }
                ...on PullRequest {
                  __typename
                  number
                  title
                  repository {
                    name
                    nameWithOwner
                  }
                  assignees(first: 10) {
                    nodes{
                      login
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
"""
  return prefix + project_id + suffix

query_project_items_template = """
query{
    node(id: "{0}") {
        ... on ProjectV2 {
          items(first: 100) {
            nodes{
              id
              fieldValues(first: 8) {
                nodes{                
                  ... on ProjectV2ItemFieldTextValue {
                    text
                    field {
                      ... on ProjectV2FieldCommon {
                        name
                      }
                    }
                  }
                  ... on ProjectV2ItemFieldDateValue {
                    date
                    field {
                      ... on ProjectV2FieldCommon {
                        name
                      }
                    }
                  }
                  ... on ProjectV2ItemFieldSingleSelectValue {
                    name
                    field {
                      ... on ProjectV2FieldCommon {
                        name
                      }
                    }
                  }
                  ... on ProjectV2ItemFieldIterationValue {
                    __typename
                    title
                    field {
                      ... on ProjectV2IterationField {
                        __typename
                        id
                        name
                      }
                    }
                  }
                }              
              }
              content{              
                ... on DraftIssue {
                  __typename
                  title
                  body
                  assignees(first: 10) {
                    nodes{
                      login
                    }
                  }
                }
                ...on Issue {
                  __typename
                  number
                  title
                  repository {
                    name
                    nameWithOwner
                  }
                  milestone {
                    title
                  }
                  assignees(first: 10) {
                    nodes{
                      login
                    }
                  }
                }
                ...on PullRequest {
                  __typename
                  number
                  title
                  repository {
                    name
                    nameWithOwner
                  }
                  assignees(first: 10) {
                    nodes{
                      login
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
"""

def get_token():
    return os.environ["GH_PROJECT_TOKEN"]

def query_project_items(project_id: str) -> str:
    # query = query_project_items_template.format(project_id)
    query = create_project_items_query(project_id)

    gh_project_token = get_token()
    gh_headers = {"Authorization": f"BEARER {gh_project_token}"}
    gh_response = requests.post('https://api.github.com/graphql', json={'query': query}, headers=gh_headers)

    items = []
    if gh_response.status_code == 200:
        items = gh_response.json()['data']['node']['items']['nodes']

    debug_json_dump("project_items.json", items)

    return items