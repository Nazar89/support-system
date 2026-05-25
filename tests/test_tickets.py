class TestCreateTicket:
    def test_create_ticket_success(self, client, user_headers):
        resp = client.post("/tickets/", json={"title": "My issue", "description": "Details here"}, headers=user_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["title"] == "My issue"
        assert data["description"] == "Details here"
        assert "id" in data
        assert "status" in data

    def test_create_ticket_no_auth(self, client):
        resp = client.post("/tickets/", json={"title": "T", "description": "D"})
        assert resp.status_code == 401

    def test_create_ticket_missing_title(self, client, user_headers):
        resp = client.post("/tickets/", json={"description": "D"}, headers=user_headers)
        assert resp.status_code == 422

    def test_create_ticket_missing_description(self, client, user_headers):
        resp = client.post("/tickets/", json={"title": "T"}, headers=user_headers)
        assert resp.status_code == 422

    def test_create_ticket_default_status(self, client, user_headers):
        resp = client.post("/tickets/", json={"title": "T", "description": "D"}, headers=user_headers)
        assert resp.json()["status"] is not None

    def test_create_ticket_sets_owner(self, client, user_headers):
        me = client.get("/users/me", headers=user_headers).json()
        resp = client.post("/tickets/", json={"title": "T", "description": "D"}, headers=user_headers)
        assert resp.json()["owner_id"] == me["id"]

    def test_create_multiple_tickets(self, client, user_headers):
        for i in range(5):
            resp = client.post("/tickets/", json={"title": f"T{i}", "description": f"D{i}"}, headers=user_headers)
            assert resp.status_code == 200

    def test_create_ticket_long_title(self, client, user_headers):
        resp = client.post("/tickets/", json={"title": "A" * 200, "description": "D"}, headers=user_headers)
        assert resp.status_code == 200

    def test_create_ticket_long_description(self, client, user_headers):
        resp = client.post("/tickets/", json={"title": "T", "description": "D" * 1000}, headers=user_headers)
        assert resp.status_code == 200

    def test_create_ticket_id_increments(self, client, user_headers):
        r1 = client.post("/tickets/", json={"title": "T1", "description": "D"}, headers=user_headers)
        r2 = client.post("/tickets/", json={"title": "T2", "description": "D"}, headers=user_headers)
        assert r2.json()["id"] > r1.json()["id"]


class TestGetMyTickets:
    def test_get_my_tickets_empty(self, client, user_headers):
        resp = client.get("/tickets/my", headers=user_headers)
        assert resp.status_code == 200
        assert resp.json() == []

    def test_get_my_tickets_after_create(self, client, user_headers):
        client.post("/tickets/", json={"title": "T", "description": "D"}, headers=user_headers)
        resp = client.get("/tickets/my", headers=user_headers)
        assert len(resp.json()) == 1

    def test_get_my_tickets_only_own(self, client, user_headers, operator_headers):
        client.post("/tickets/", json={"title": "T", "description": "D"}, headers=user_headers)
        resp = client.get("/tickets/my", headers=operator_headers)
        assert resp.json() == []

    def test_get_my_tickets_no_auth(self, client):
        resp = client.get("/tickets/my")
        assert resp.status_code == 401

    def test_get_my_tickets_multiple(self, client, user_headers):
        for i in range(3):
            client.post("/tickets/", json={"title": f"T{i}", "description": "D"}, headers=user_headers)
        resp = client.get("/tickets/my", headers=user_headers)
        assert len(resp.json()) == 3


class TestGetAllTickets:
    def test_get_all_tickets_admin(self, client, admin_headers, user_headers):
        client.post("/tickets/", json={"title": "T", "description": "D"}, headers=user_headers)
        resp = client.get("/tickets/", headers=admin_headers)
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    def test_get_all_tickets_operator(self, client, operator_headers, user_headers):
        client.post("/tickets/", json={"title": "T", "description": "D"}, headers=user_headers)
        resp = client.get("/tickets/", headers=operator_headers)
        assert resp.status_code == 200

    def test_get_all_tickets_user_forbidden(self, client, user_headers):
        resp = client.get("/tickets/", headers=user_headers)
        assert resp.status_code == 403

    def test_get_all_tickets_no_auth(self, client):
        resp = client.get("/tickets/")
        assert resp.status_code == 401


class TestGetTicketById:
    def test_get_ticket_owner(self, client, user_headers, sample_ticket):
        tid = sample_ticket["id"]
        resp = client.get(f"/tickets/{tid}", headers=user_headers)
        assert resp.status_code == 200
        assert resp.json()["id"] == tid

    def test_get_ticket_admin(self, client, admin_headers, sample_ticket):
        tid = sample_ticket["id"]
        resp = client.get(f"/tickets/{tid}", headers=admin_headers)
        assert resp.status_code == 200

    def test_get_ticket_operator(self, client, operator_headers, sample_ticket):
        tid = sample_ticket["id"]
        resp = client.get(f"/tickets/{tid}", headers=operator_headers)
        assert resp.status_code == 200

    def test_get_ticket_not_found(self, client, user_headers):
        resp = client.get("/tickets/9999", headers=user_headers)
        assert resp.status_code == 404

    def test_get_ticket_no_auth(self, client, sample_ticket):
        resp = client.get(f"/tickets/{sample_ticket['id']}")
        assert resp.status_code == 401


class TestChangeTicketStatus:
    def test_change_status_admin(self, client, admin_headers, sample_ticket):
        tid = sample_ticket["id"]
        resp = client.patch(f"/tickets/{tid}/status", json={"status": "in_progress"}, headers=admin_headers)
        assert resp.status_code == 200
        assert resp.json()["status"] == "in_progress"

    def test_change_status_operator(self, client, operator_headers, sample_ticket):
        tid = sample_ticket["id"]
        resp = client.patch(f"/tickets/{tid}/status", json={"status": "closed"}, headers=operator_headers)
        assert resp.status_code == 200

    def test_change_status_user_forbidden(self, client, user_headers, sample_ticket):
        tid = sample_ticket["id"]
        resp = client.patch(f"/tickets/{tid}/status", json={"status": "closed"}, headers=user_headers)
        assert resp.status_code == 403

    def test_change_status_invalid(self, client, admin_headers, sample_ticket):
        tid = sample_ticket["id"]
        resp = client.patch(f"/tickets/{tid}/status", json={"status": "flying"}, headers=admin_headers)
        assert resp.status_code == 400

    def test_change_status_not_found(self, client, admin_headers):
        resp = client.patch("/tickets/9999/status", json={"status": "closed"}, headers=admin_headers)
        assert resp.status_code == 404

    def test_change_status_all_valid(self, client, admin_headers, user_headers):
        for status in ("open", "in_progress", "closed"):
            t = client.post("/tickets/", json={"title": f"T-{status}", "description": "D"}, headers=user_headers).json()
            resp = client.patch(f"/tickets/{t['id']}/status", json={"status": status}, headers=admin_headers)
            assert resp.status_code == 200
            assert resp.json()["status"] == status