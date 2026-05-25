class TestLogin:
    def test_login_success(self, client):
        client.post("/users/register", json={"username": "u1", "email": "u1@test.com", "password": "pass123"})
        resp = client.post("/auth/login", json={"username": "u1", "password": "pass123"})
        assert resp.status_code == 200
        assert "access_token" in resp.json()
        assert resp.json()["token_type"] == "bearer"

    def test_login_wrong_password(self, client):
        client.post("/users/register", json={"username": "u2", "email": "u2@test.com", "password": "pass123"})
        resp = client.post("/auth/login", json={"username": "u2", "password": "wrong"})
        assert resp.status_code == 401

    def test_login_nonexistent_user(self, client):
        resp = client.post("/auth/login", json={"username": "ghost", "password": "pass"})
        assert resp.status_code == 401

    def test_login_empty_username(self, client):
        resp = client.post("/auth/login", json={"username": "", "password": "pass"})
        assert resp.status_code == 401

    def test_login_empty_password(self, client):
        client.post("/users/register", json={"username": "u3", "email": "u3@test.com", "password": "pass123"})
        resp = client.post("/auth/login", json={"username": "u3", "password": ""})
        assert resp.status_code == 401

    def test_login_returns_token_string(self, client):
        client.post("/users/register", json={"username": "u4", "email": "u4@test.com", "password": "pass123"})
        resp = client.post("/auth/login", json={"username": "u4", "password": "pass123"})
        token = resp.json()["access_token"]
        assert isinstance(token, str)
        assert len(token) > 10

    def test_login_case_sensitive_username(self, client):
        client.post("/users/register", json={"username": "CaseName", "email": "case@test.com", "password": "pass123"})
        resp = client.post("/auth/login", json={"username": "casename", "password": "pass123"})
        assert resp.status_code == 401

    def test_login_multiple_times_gives_different_tokens(self, client):
        client.post("/users/register", json={"username": "multi", "email": "multi@test.com", "password": "pass123"})
        t1 = client.post("/auth/login", json={"username": "multi", "password": "pass123"}).json()["access_token"]
        t2 = client.post("/auth/login", json={"username": "multi", "password": "pass123"}).json()["access_token"]
        assert t1 != t2

    def test_login_missing_fields(self, client):
        resp = client.post("/auth/login", json={"username": "u5"})
        assert resp.status_code == 422

    def test_login_extra_fields_ignored(self, client):
        client.post("/users/register", json={"username": "u6", "email": "u6@test.com", "password": "pass123"})
        resp = client.post("/auth/login", json={"username": "u6", "password": "pass123", "extra": "data"})
        assert resp.status_code == 200

    def test_login_admin_role(self, client, admin_headers):
        resp = client.get("/users/me", headers=admin_headers)
        assert resp.json()["role"] == "admin"

    def test_login_user_role(self, client, user_headers):
        resp = client.get("/users/me", headers=user_headers)
        assert resp.json()["role"] == "user"

    def test_login_operator_role(self, client, operator_headers):
        resp = client.get("/users/me", headers=operator_headers)
        assert resp.json()["role"] == "operator"

    def test_invalid_token_rejected(self, client):
        resp = client.get("/users/me", headers={"Authorization": "Bearer invalidtoken"})
        assert resp.status_code == 401

    def test_no_token_rejected(self, client):
        resp = client.get("/users/me")
        assert resp.status_code == 401