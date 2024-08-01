from deephaven import ui, new_table
from deephaven.column import double_col, string_col
from .queries import query_project_items
from .util import (
    get_issue_type,
    get_repo_name,
    get_number,
    get_title,
    get_sprint,
    get_milestone,
    get_assignee,
    get_status,
    status_column_order,
)

@ui.component
def issues(project_id):
    items = query_project_items(project_id)

    number_col_values = []
    title_col_values = []
    sprint_values = []
    milestone_column_values = []
    repo_col_values = []
    issue_type_col_values = []
    status_col_values = []
    assignee_col_values = []

    for item in items:
        issue_type = get_issue_type(item)
        repo_name = get_repo_name(item) or ("[Draft]" if issue_type == 'DraftIssue' else None)

        repo_col_values.append(repo_name)
        number_col_values.append(get_number(item))
        title_col_values.append(get_title(item))
        sprint_values.append(get_sprint(item))
        milestone_column_values.append(get_milestone(item))
        issue_type_col_values.append(issue_type or 'Unknown')
        assignee_col_values.append(get_assignee(item))

        # Append a numeric sorting prefix
        status = get_status(item['fieldValues']['nodes'])
        for j, s in enumerate(status_column_order):
            if s in status:
                status = str(j + 1) + ' - ' + status

        status_col_values.append(status)

        table = new_table([
            string_col("Repo", repo_col_values),
            string_col("Sprint", sprint_values),
            string_col("Milestone", milestone_column_values),
            string_col("Status", status_col_values),
            string_col("Assignee", assignee_col_values),
            string_col("Issue_Type", issue_type_col_values),
            double_col("Issue", number_col_values),
            string_col("Title", title_col_values)
        ]).format_columns(["Issue = Decimal(`#`)"]).sort([
            "Repo", "Issue_Type", "Sprint", "Milestone", "Status" #, "Assignee"
        ])

    return table
