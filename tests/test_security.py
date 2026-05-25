class TestAdminStats:
    def test_stats_admin(self, client, admin_headers):
        resp = client.get("/admin/stats", headers=admin_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "users_count" in data
        assert "tickets_count" in data
        assert "messages_count" in data
        assert "tickets_by_status" in data

    def test_stats_user_forbidden(self, client, user_headers):
        resp = client.get("/admin/stats", headers=user_headers)
        assert resp.status_code == 403

    def test_stats_operator_forbidden(self, client, operator_headers):
        resp = client.get("/admin/stats", headers=operator_headers)
        assert resp.status_code == 403

    def test_stats_no_auth(self, client):
        resp = client.get("/admin/stats")
        assert resp.status_code == 401

    def test_stats_users_count_increments(self, client, admin_headers):
        before = client.get("/admin/stats", headers=admin_headers).json()["users_count"]
        client.post("/users/register", json={"username": "newone", "email": "newone@test.com", "password": "pass"})
        after = client.get("/admin/stats", headers=admin_headers).json()["users_count"]
        assert after == before + 1

    def test_stats_tickets_count_increments(self, client, admin_headers, user_headers):
        before = client.get("/admin/stats", headers=admin_headers).json()["tickets_count"]
        client.post("/tickets/", json={"title": "T", "description": "D"}, headers=user_headers)
        after = client.get("/admin/stats", headers=admin_headers).json()["tickets_count"]
        assert after == before + 1

    def test_stats_messages_count_increments(self, client, admin_headers, user_headers, sample_ticket):
        before = client.get("/admin/stats", headers=admin_headers).json()["messages_count"]
        client.post(f"/tickets/{sample_ticket['id']}/messages/", json={"text": "Hi"}, headers=user_headers)
        after = client.get("/admin/stats", headers=admin_headers).json()["messages_count"]
        assert after == before + 1

    def test_stats_tickets_by_status_is_dict(self, client, admin_headers):
        resp = client.get("/admin/stats", headers=admin_headers).json()
        assert isinstance(resp["tickets_by_status"], dict)

    def test_stats_tickets_by_status_after_create(self, client, admin_headers, user_headers):
        client.post("/tickets/", json={"title": "T", "description": "D"}, headers=user_headers)
        stats = client.get("/admin/stats", headers=admin_headers).json()
        total = sum(stats["tickets_by_status"].values())
        assert total == stats["tickets_count"]

    def test_stats_counts_are_integers(self, client, admin_headers):
        data = client.get("/admin/stats", headers=admin_headers).json()
        assert isinstance(data["users_count"], int)
        assert isinstance(data["tickets_count"], int)
        assert isinstance(data["messages_count"], int)


class TestIntegration:
    def test_full_workflow(self, client):
        client.post("/users/register", json={"username": "flow_user", "email": "flow@test.com", "password": "pass123"})
        token = client.post("/auth/login", json={"username": "flow_user", "password": "pass123"}).json()["access_token"]
        uh = {"Authorization": f"Bearer {token}"}

        client.post("/users/register", json={"username": "flow_admin", "email": "fadmin@test.com", "password": "pass123", "role": "admin"})
        at = client.post("/auth/login", json={"username": "flow_admin", "password": "pass123"}).json()["access_token"]
        ah = {"Authorization": f"Bearer {at}"}

        t = client.post("/tickets/", json={"title": "My problem", "description": "Needs help"}, headers=uh).json()
        assert t["status"] is not None

        m1 = client.post(f"/tickets/{t['id']}/messages/", json={"text": "Please help"}, headers=uh).json()
        assert m1["text"] == "Please help"

        m2 = client.post(f"/tickets/{t['id']}/messages/", json={"text": "We are on it"}, headers=ah).json()
        assert m2["text"] == "We are on it"

        resp = client.patch(f"/tickets/{t['id']}/status", json={"status": "in_progress"}, headers=ah)
        assert resp.status_code == 200

        msgs = client.get(f"/tickets/{t['id']}/messages/", headers=uh).json()
        assert len(msgs) == 2

        resp = client.patch(f"/tickets/{t['id']}/status", json={"status": "closed"}, headers=ah)
        assert resp.json()["status"] == "closed"

        stats = client.get("/admin/stats", headers=ah).json()
        assert stats["tickets_count"] >= 1
        assert stats["messages_count"] >= 2

    def test_faq_workflow(self, client, admin_headers):
        f = client.post("/faq/", json={"question": "How?", "answer": "Like this."}, headers=admin_headers).json()
        assert f["id"] is not None

        faqs = client.get("/faq/").json()
        assert any(item["id"] == f["id"] for item in faqs)

        client.delete(f"/faq/{f['id']}", headers=admin_headers)
        faqs_after = client.get("/faq/").json()
        assert not any(item["id"] == f["id"] for item in faqs_after)

    def test_role_change_workflow(self, client, admin_headers):
        reg = client.post("/users/register", json={"username": "promote_me", "email": "pm@test.com", "password": "pass"}).json()
        assert reg["role"] == "user"

        client.patch(f"/users/{reg['id']}/role", json={"role": "operator"}, headers=admin_headers)
        token = client.post("/auth/login", json={"username": "promote_me", "password": "pass"}).json()["access_token"]
        me = client.get("/users/me", headers={"Authorization": f"Bearer {token}"}).json()
        assert me["role"] == "operator"

        resp = client.get("/tickets/", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200