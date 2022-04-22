def test_login(app, config):
    app.session.ensure_logout()
    app.session.login(username=config["webadmin"]["username"], password=config["webadmin"]["password"])
    assert app.session.is_logged_in_as(config["webadmin"]["username"])
