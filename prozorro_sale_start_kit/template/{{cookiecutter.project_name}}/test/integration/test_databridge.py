
class TestDataBridge:

    async def test_version(self, client_databridge):
        resp = await client_databridge.get('api')
        assert resp.status == 200
        data = await resp.json()

        assert 'api_version' in data

    async def test_ping(self, client_databridge):
        resp = await client_databridge.get('api/ping')
        assert resp.status == 200
        data = await resp.json()

        assert data['text'] == 'pong'
