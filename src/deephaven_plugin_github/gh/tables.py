from deephaven import new_table
from deephaven.table import Table
from deephaven.column import double_col, string_col
from .queries import (
    query_project_items,
    query_prs
)
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

def issues_table(project_id, project_title: str | None = None) -> Table:
    items = query_project_items(project_id, project_title)

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

    return new_table([
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

def assignees_table(org_id: str, project_title: str | None = None) -> Table:
    issues = issues_table(org_id, project_title)

    return issues.select_distinct(
        "Assignee"
    ).where(
        "Assignee != null"
    ).view(
        "Assignee"
    ).sort(
        "Assignee"
    )

def prs_table(query: str) -> Table:
    edges = query_prs(query)

    number_col_values = []
    title_col_values = []
    author_col_values = []
    repo_col_values = []
    created_at_col_values = []
    merged_at_col_values = []
    url_col_values = []

    for edge in edges:
        node = edge['node']

        number_col_values.append(node['number'])
        title_col_values.append(node['title'])
        author_col_values.append(node['author']['login'])
        repo_col_values.append(node['repository']['nameWithOwner'])
        created_at_col_values.append(node['createdAt'])
        merged_at_col_values.append(node['mergedAt'])
        url_col_values.append(node['url'])

    return new_table([
        string_col("Repo", repo_col_values),
        double_col("PR", number_col_values),
        string_col("Author", author_col_values),
        string_col("Title", title_col_values),
        string_col("Created", created_at_col_values),
        string_col("Merged", merged_at_col_values),
        string_col("URL", url_col_values)
    ]).format_columns(["PR = Decimal(`#`)"]).sort([
        "Repo", "PR"
    ])