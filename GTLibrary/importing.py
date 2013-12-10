from GTLibrary import app, db, user_datastore, Model

def basic_users():
    # create users
    admin_user = user_datastore.create_user(email="admin", password="aaa")
    guest_user = user_datastore.create_user(email="guest", password="guest")

    # create roles
    admin_role = user_datastore.find_or_create_role("Admin")
    user_role = user_datastore.find_or_create_role("User")

    # assign roles
    user_datastore.add_role_to_user(admin_user, admin_role)
    user_datastore.add_role_to_user(admin_user, user_role)
    user_datastore.add_role_to_user(guest_user, user_role)
    db.session.commit()

    return guest_user

def typical_workflow():
    user = user_datastore.get_user("guest")
    a = Model.Asset.create(name="Some asset", owner=user)