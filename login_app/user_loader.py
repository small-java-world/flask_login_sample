def setup_auth(login_manager):
    @login_manager.user_loader
    def load_user(user_id):
        from login_app.models.users import User

        return User(user_id)
