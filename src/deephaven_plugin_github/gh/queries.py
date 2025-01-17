import os
import requests
from .debug import debug_json_dump

def create_projects_query(org_id: str) -> str:
  prefix = """query {
    organization(login: \""""
    
  suffix = """\"){
      projectV2(number: 1) {
        id
        title
      }
      projectsV2(first: 10){
        nodes {
          id
          title
        }
      }
    }
  }"""

  return prefix + org_id + suffix

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

def create_issue_search_query(query: str, count=100) -> str:
  # TODO: GH caps search api at 100. Will need to paginate if we want more
  if count > 100:
    count = 100

  prefix = "query { search("

  params = f"query: \"{query}\", type: ISSUE, first: {count}"

  suffix = """){
    issueCount
    edges {
      node {
        ... on Issue {
          __typename
          number
          title
          author {
            login
          }
          assignees(first: 5) {
            nodes {
              login
            }
          }
          repository {
            nameWithOwner
          }
          createdAt
          url
        }
        ... on PullRequest {
          __typename
          number
          title
          author {
            login
          }
          repository {
            nameWithOwner
          }
          createdAt
          mergedAt
          url
          changedFiles
          additions
          deletions
        }
      }
    }
  }
}
"""
  return prefix + params + suffix

def get_token():
    return os.environ["GH_PROJECT_TOKEN"]

def query_graphql_api(query: str):
  gh_project_token = get_token()
  gh_headers = {"Authorization": f"BEARER {gh_project_token}"}
  return requests.post('https://api.github.com/graphql', json={'query': query}, headers=gh_headers)

def query_project(org_id: str, project_title: str | None = None):
    query = create_projects_query(org_id)
    gh_response = query_graphql_api(query)

    project = None
    if gh_response.status_code == 200:
        org = gh_response.json()['data']['organization']

        if project_title is None:
          project = org['projectV2']
        else:
          projects = org['projectsV2']['nodes']
          for p in projects:
              if p['title'] == project_title:
                  project = p
                  break

    debug_json_dump("projects.json", project)

    return project

def query_project_items(org_id: str, project_title: str | None = None):
    project = query_project(org_id, project_title)

    items = []
    if not project:
        return items

    # query = query_project_items_template.format(project_id)
    query = create_project_items_query(project['id'])
    gh_response = query_graphql_api(query)

    if gh_response.status_code == 200:
        items = gh_response.json()['data']['node']['items']['nodes']

    debug_json_dump("project_items.json", items)

    return items

def query_issues(query: str, count=100):
    query = create_issue_search_query(query, count)
    gh_response = query_graphql_api(query)

    prs = []
    if gh_response.status_code == 200:
        prs = gh_response.json()['data']['search']['edges']

    debug_json_dump("issues.json", prs)

    return prs