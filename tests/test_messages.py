class TestSendMessage:
    def test_send_message_owner(self, client, user_headers, sample_ticket):
        tid = sample_ticket["id"]
        resp = client.post(f"/tickets/{tid}/messages/", json={"text": "Hello support"}, headers=user_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["text"] == "Hello support"
        assert data["ticket_id"] == tid

    def test_send_message_admin(self, client, admin_headers, sample_ticket):
        tid = sample_ticket["id"]
        resp = client.post(f"/tickets/{tid}/messages/", json={"text": "Admin reply"}, headers=admin_headers)
        assert resp.status_code == 200

    def test_send_message_operator(self, client, operator_headers, sample_ticket):
        tid = sample_ticket["id"]
        resp = client.post(f"/tickets/{tid}/messages/", json={"text": "Operator reply"}, headers=operator_headers)
        assert resp.status_code == 200

    def test_send_message_other_user_forbidden(self, client, sample_ticket):
        client.post("/users/register", json={"username": "other", "email": "other@test.com", "password": "pass"})
        token = client.post("/auth/login", json={"username": "other", "password": "pass"}).json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        tid = sample_ticket["id"]
        resp = client.post(f"/tickets/{tid}/messages/", json={"text": "Hack"}, headers=headers)
        assert resp.status_code == 403

    def test_send_message_no_auth(self, client, sample_ticket):
        resp = client.post(f"/tickets/{sample_ticket['id']}/messages/", json={"text": "Hi"})
        assert resp.status_code == 401

    def test_send_message_missing_text(self, client, user_headers, sample_ticket):
        resp = client.post(f"/tickets/{sample_ticket['id']}/messages/", json={}, headers=user_headers)
        assert resp.status_code == 422

    def test_send_message_nonexistent_ticket(self, client, user_headers):
        resp = client.post("/tickets/9999/messages/", json={"text": "Hi"}, headers=user_headers)
        assert resp.status_code == 404

    def test_send_message_returns_sender_id(self, client, user_headers, sample_ticket):
        me = client.get("/users/me", headers=user_headers).json()
        tid = sample_ticket["id"]
        resp = client.post(f"/tickets/{tid}/messages/", json={"text": "Hi"}, headers=user_headers)
        assert resp.json()["sender_id"] == me["id"]

    def test_send_multiple_messages(self, client, user_headers, sample_ticket):
        tid = sample_ticket["id"]
        for i in range(5):
            resp = client.post(f"/tickets/{tid}/messages/", json={"text": f"Msg {i}"}, headers=user_headers)
            assert resp.status_code == 200

    def test_send_message_long_text(self, client, user_headers, sample_ticket):
        tid = sample_ticket["id"]
        resp = client.post(f"/tickets/{tid}/messages/", json={"text": "A" * 5000}, headers=user_headers)
        assert resp.status_code == 200


class TestGetMessages:
    def test_get_messages_empty(self, client, user_headers, sample_ticket):
        tid = sample_ticket["id"]
        resp = client.get(f"/tickets/{tid}/messages/", headers=user_headers)
        assert resp.status_code == 200
        assert resp.json() == []

    def test_get_messages_after_send(self, client, user_headers, sample_ticket):
        tid = sample_ticket["id"]
        client.post(f"/tickets/{tid}/messages/", json={"text": "Hello"}, headers=user_headers)
        resp = client.get(f"/tickets/{tid}/messages/", headers=user_headers)
        assert len(resp.json()) == 1
        assert resp.json()[0]["text"] == "Hello"

    def test_get_messages_admin(self, client, admin_headers, user_headers, sample_ticket):
        tid = sample_ticket["id"]
        client.post(f"/tickets/{tid}/messages/", json={"text": "Hi"}, headers=user_headers)
        resp = client.get(f"/tickets/{tid}/messages/", headers=admin_headers)
        assert resp.status_code == 200
        assert len(resp.json()) == 1

    def test_get_messages_other_user_forbidden(self, client, sample_ticket):
        client.post("/users/register", json={"username": "spy", "email": "spy@test.com", "password": "pass"})
        token = client.post("/auth/login", json={"username": "spy", "password": "pass"}).json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        resp = client.get(f"/tickets/{sample_ticket['id']}/messages/", headers=headers)
        assert resp.status_code == 403

    def test_get_messages_no_auth(self, client, sample_ticket):
        resp = client.get(f"/tickets/{sample_ticket['id']}/messages/")
        assert resp.status_code == 401

    def test_get_messages_nonexistent_ticket(self, client, user_headers):
        resp = client.get("/tickets/9999/messages/", headers=user_headers)
        assert resp.status_code == 404

    def test_get_messages_order(self, client, user_headers, sample_ticket):
        tid = sample_ticket["id"]
        for i in range(3):
            client.post(f"/tickets/{tid}/messages/", json={"text": f"Msg {i}"}, headers=user_headers)
        resp = client.get(f"/tickets/{tid}/messages/", headers=user_headers)
        texts = [m["text"] for m in resp.json()]
        assert texts == ["Msg 0", "Msg 1", "Msg 2"]

    def test_get_messages_multiple_senders(self, client, user_headers, admin_headers, sample_ticket):
        tid = sample_ticket["id"]
        client.post(f"/tickets/{tid}/messages/", json={"text": "User msg"}, headers=user_headers)
        client.post(f"/tickets/{tid}/messages/", json={"text": "Admin msg"}, headers=admin_headers)
        resp = client.get(f"/tickets/{tid}/messages/", headers=user_headers)
        assert len(resp.json()) == 2