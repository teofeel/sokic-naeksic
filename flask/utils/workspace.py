from core.sokic.core.use_cases.WorkspaceManager import WorkspaceManager

def create_default_workspace(workspace_manager: WorkspaceManager):
    workspaces = workspace_manager.get_all_workspaces_metadata()
    if not workspaces:
        workspace_manager.create_workspace('Workspace 1', None, 'yaml', 'block')