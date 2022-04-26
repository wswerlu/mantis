from model.project import Project


def test_add_project(app, data_projects):
    project = data_projects
    old_projects = app.soap.get_project_list()
    if project in old_projects:
        app.project.delete_project_by_name(project.name)
        old_projects.remove(project)
    app.project.create(project)
    new_projects = app.soap.get_project_list()
    assert len(old_projects) + 1 == len(new_projects)
    old_projects.append(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
