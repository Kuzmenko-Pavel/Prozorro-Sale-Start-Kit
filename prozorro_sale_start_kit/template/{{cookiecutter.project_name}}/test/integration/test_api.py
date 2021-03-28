
class TestApi:

    async def test_version(self, client):
        resp = await client.get('api')
        assert resp.status == 200
        data = await resp.json()

        assert 'api_version' in data

    async def test_ping(self, client):
        resp = await client.get('api/ping')
        assert resp.status == 200
        data = await resp.json()

        assert data['text'] == 'pong'
