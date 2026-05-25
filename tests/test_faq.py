class TestGetFaq:
    def test_get_faq_empty(self, client):
        resp = client.get("/faq/")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_get_faq_no_auth_required(self, client):
        resp = client.get("/faq/")
        assert resp.status_code == 200

    def test_get_faq_after_add(self, client, admin_headers):
        client.post("/faq/", json={"question": "Q?", "answer": "A."}, headers=admin_headers)
        resp = client.get("/faq/")
        assert len(resp.json()) == 1

    def test_get_faq_multiple(self, client, admin_headers):
        for i in range(5):
            client.post("/faq/", json={"question": f"Q{i}?", "answer": f"A{i}."}, headers=admin_headers)
        resp = client.get("/faq/")
        assert len(resp.json()) == 5

    def test_get_faq_returns_correct_fields(self, client, admin_headers):
        client.post("/faq/", json={"question": "Q?", "answer": "A."}, headers=admin_headers)
        item = client.get("/faq/").json()[0]
        assert "id" in item
        assert "question" in item
        assert "answer" in item

    def test_get_faq_content_correct(self, client, admin_headers):
        client.post("/faq/", json={"question": "What is this?", "answer": "This is a test."}, headers=admin_headers)
        item = client.get("/faq/").json()[0]
        assert item["question"] == "What is this?"
        assert item["answer"] == "This is a test."


class TestAddFaq:
    def test_add_faq_admin(self, client, admin_headers):
        resp = client.post("/faq/", json={"question": "Q?", "answer": "A."}, headers=admin_headers)
        assert resp.status_code == 200
        assert resp.json()["question"] == "Q?"

    def test_add_faq_user_forbidden(self, client, user_headers):
        resp = client.post("/faq/", json={"question": "Q?", "answer": "A."}, headers=user_headers)
        assert resp.status_code == 403

    def test_add_faq_operator_forbidden(self, client, operator_headers):
        resp = client.post("/faq/", json={"question": "Q?", "answer": "A."}, headers=operator_headers)
        assert resp.status_code == 403

    def test_add_faq_no_auth(self, client):
        resp = client.post("/faq/", json={"question": "Q?", "answer": "A."})
        assert resp.status_code == 401

    def test_add_faq_missing_question(self, client, admin_headers):
        resp = client.post("/faq/", json={"answer": "A."}, headers=admin_headers)
        assert resp.status_code == 422

    def test_add_faq_missing_answer(self, client, admin_headers):
        resp = client.post("/faq/", json={"question": "Q?"}, headers=admin_headers)
        assert resp.status_code == 422

    def test_add_faq_returns_id(self, client, admin_headers):
        resp = client.post("/faq/", json={"question": "Q?", "answer": "A."}, headers=admin_headers)
        assert isinstance(resp.json()["id"], int)

    def test_add_faq_long_content(self, client, admin_headers):
        resp = client.post("/faq/", json={"question": "Q" * 500 + "?", "answer": "A" * 2000 + "."}, headers=admin_headers)
        assert resp.status_code == 200

    def test_add_multiple_faq(self, client, admin_headers):
        for i in range(10):
            resp = client.post("/faq/", json={"question": f"Q{i}?", "answer": f"A{i}."}, headers=admin_headers)
            assert resp.status_code == 200


class TestDeleteFaq:
    def test_delete_faq_admin(self, client, admin_headers, sample_faq):
        fid = sample_faq["id"]
        resp = client.delete(f"/faq/{fid}", headers=admin_headers)
        assert resp.status_code == 200
        assert client.get("/faq/").json() == []

    def test_delete_faq_user_forbidden(self, client, user_headers, sample_faq):
        resp = client.delete(f"/faq/{sample_faq['id']}", headers=user_headers)
        assert resp.status_code == 403

    def test_delete_faq_no_auth(self, client, sample_faq):
        resp = client.delete(f"/faq/{sample_faq['id']}")
        assert resp.status_code == 401

    def test_delete_faq_not_found(self, client, admin_headers):
        resp = client.delete("/faq/9999", headers=admin_headers)
        assert resp.status_code == 404

    def test_delete_faq_removes_correct_item(self, client, admin_headers):
        f1 = client.post("/faq/", json={"question": "Q1?", "answer": "A1."}, headers=admin_headers).json()
        f2 = client.post("/faq/", json={"question": "Q2?", "answer": "A2."}, headers=admin_headers).json()
        client.delete(f"/faq/{f1['id']}", headers=admin_headers)
        remaining = client.get("/faq/").json()
        assert len(remaining) == 1
        assert remaining[0]["id"] == f2["id"]