class TestRegister:
    def test_register_success(self, client):
        resp = client.post("/users/register", json={"username": "newuser", "email": "new@test.com", "password": "pass123"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["username"] == "newuser"
        assert data["email"] == "new@test.com"
        assert data["role"] == "user"
        assert "id" in data

    def test_register_duplicate_username(self, client):
        client.post("/users/register", json={"username": "dup", "email": "dup1@test.com", "password": "pass"})
        resp = client.post("/users/register", json={"username": "dup", "email": "dup2@test.com", "password": "pass"})
        assert resp.status_code == 400

    def test_register_duplicate_email(self, client):
        client.post("/users/register", json={"username": "u1", "email": "same@test.com", "password": "pass"})
        resp = client.post("/users/register", json={"username": "u2", "email": "same@test.com", "password": "pass"})
        assert resp.status_code == 400

    def test_register_default_role_is_user(self, client):
        resp = client.post("/users/register", json={"username": "roletest", "email": "role@test.com", "password": "pass"})
        assert resp.json()["role"] == "user"

    def test_register_with_explicit_role(self, client):
        resp = client.post("/users/register", json={"username": "op", "email": "op@test.com", "password": "pass", "role": "operator"})
        assert resp.json()["role"] == "operator"

    def test_register_missing_username(self, client):
        resp = client.post("/users/register", json={"email": "x@test.com", "password": "pass"})
        assert resp.status_code == 422

    def test_register_missing_email(self, client):
        resp = client.post("/users/register", json={"username": "x", "password": "pass"})
        assert resp.status_code == 422

    def test_register_missing_password(self, client):
        resp = client.post("/users/register", json={"username": "x", "email": "x@test.com"})
        assert resp.status_code == 422

    def test_register_password_not_returned(self, client):
        resp = client.post("/users/register", json={"username": "safe", "email": "safe@test.com", "password": "secret"})
        assert "password" not in resp.json()
        assert "password_hash" not in resp.json()

    def test_register_id_is_integer(self, client):
        resp = client.post("/users/register", json={"username": "idtest", "email": "id@test.com", "password": "pass"})
        assert isinstance(resp.json()["id"], int)


class TestGetMe:
    def test_get_me_success(self, client, user_headers):
        resp = client.get("/users/me", headers=user_headers)
        assert resp.status_code == 200
        assert resp.json()["username"] == "user_test"

    def test_get_me_no_auth(self, client):
        resp = client.get("/users/me")
        assert resp.status_code == 401

    def test_get_me_invalid_token(self, client):
        resp = client.get("/users/me", headers={"Authorization": "Bearer fake"})
        assert resp.status_code == 401

    def test_get_me_returns_correct_fields(self, client, user_headers):
        resp = client.get("/users/me", headers=user_headers)
        data = resp.json()
        assert "id" in data
        assert "username" in data
        assert "email" in data
        assert "role" in data


class TestListUsers:
    def test_list_users_admin(self, client, admin_headers):
        resp = client.get("/users/", headers=admin_headers)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_list_users_user_forbidden(self, client, user_headers):
        resp = client.get("/users/", headers=user_headers)
        assert resp.status_code == 403

    def test_list_users_no_auth(self, client):
        resp = client.get("/users/")
        assert resp.status_code == 401

    def test_list_users_contains_registered(self, client, admin_headers):
        client.post("/users/register", json={"username": "listed", "email": "listed@test.com", "password": "pass"})
        resp = client.get("/users/", headers=admin_headers)
        usernames = [u["username"] for u in resp.json()]
        assert "listed" in usernames


class TestChangeRole:
    def test_change_role_admin(self, client, admin_headers):
        reg = client.post("/users/register", json={"username": "target", "email": "target@test.com", "password": "pass"})
        uid = reg.json()["id"]
        resp = client.patch(f"/users/{uid}/role", json={"role": "operator"}, headers=admin_headers)
        assert resp.status_code == 200
        assert resp.json()["role"] == "operator"

    def test_change_role_user_forbidden(self, client, user_headers):
        reg = client.post("/users/register", json={"username": "target2", "email": "t2@test.com", "password": "pass"})
        uid = reg.json()["id"]
        resp = client.patch(f"/users/{uid}/role", json={"role": "admin"}, headers=user_headers)
        assert resp.status_code == 403

    def test_change_role_nonexistent_user(self, client, admin_headers):
        resp = client.patch("/users/9999/role", json={"role": "operator"}, headers=admin_headers)
        assert resp.status_code == 404

    def test_change_role_to_admin(self, client, admin_headers):
        reg = client.post("/users/register", json={"username": "toadmin", "email": "ta@test.com", "password": "pass"})
        uid = reg.json()["id"]
        resp = client.patch(f"/users/{uid}/role", json={"role": "admin"}, headers=admin_headers)
        assert resp.json()["role"] == "admin"

    def test_change_role_to_user(self, client, admin_headers):
        reg = client.post("/users/register", json={"username": "touser", "email": "tu@test.com", "password": "pass", "role": "operator"})
        uid = reg.json()["id"]
        resp = client.patch(f"/users/{uid}/role", json={"role": "user"}, headers=admin_headers)
        assert resp.json()["role"] == "user"