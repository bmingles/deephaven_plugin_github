from deephaven import ui
from .queries import query_project_items

@ui.component
def issues(project_id):
    iss = query_project_items(project_id, debug=True)
    return ui.text(str(iss))