# define the status column order explicitly
status_column_order = [
  'No Status',
  'New',
  'Ready',
  'In progress',
  'In review',
  'Done'
]

def get_nested(obj, *keys):
  result = obj

  for k in keys:
    if result is None or k not in result:
      return None

    result = result[k]

  return result

def get_assignee(item):
  assignees = get_nested(item, 'content', 'assignees', 'nodes') or []

  if len(assignees) == 0:
    return None

  return assignees[0]['login']

def get_issue_type(item):
  return get_nested(item, 'content', '__typename') or print(item)

def get_milestone(item):
  return get_nested(item, 'content', 'milestone', 'title') or 'None'

def get_number(item):
  return get_nested(item, 'content', 'number') or None

def get_repo_name(item):
  return get_nested(item, 'content', 'repository', 'name')

def get_sprint(item):
  for field_value in item["fieldValues"]["nodes"]:
    if 'field' in field_value and field_value['field']['name'] == 'Sprint':
      return field_value['title']

def get_status(field_values):
  for field_value in field_values:
    if 'field' in field_value and field_value['field']['name'] == 'Status':
      return field_value['name']

  return 'No Status'

def get_title(item):
  # TODO: look for title in fieldValues if not in content
  title = get_nested(item, 'content', 'title')

  if title:
    return title
  
  field_values = get_nested(item, 'fieldValues', 'nodes')
  for field_value in field_values:
    if 'field' in field_value and field_value['field']['name'] == 'Title':
      return field_value['text']

  return None