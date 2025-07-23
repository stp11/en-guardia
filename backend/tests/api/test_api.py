from models import Episode


class TestEpisodes:
    def test_get_episodes_empty(self, client):
        response = client.get("/api/episodes")
        assert response.status_code == 200
        assert response.json()["items"] == []

    def test_get_episodes(self, client, db_session):
        episode = Episode(id=1, title="Test Episode")
        db_session.add(episode)
        db_session.commit()

        response = client.get("/api/episodes")
        assert response.status_code == 200
        assert response.json()["total"] == 1
        assert response.json()["items"][0]["title"] == "Test Episode"
