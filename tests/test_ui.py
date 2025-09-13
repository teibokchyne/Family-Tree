class TestCommonUI:
    def test_home_page(self, client):
        response = client.get('/')
        assert b'Home' in response.data or b'home' in response.data

    def test_login_page(self, client):
        response = client.get('/login')
        assert b'Login' in response.data or b'login' in response.data
        assert b'Email' in response.data
        assert b'Password' in response.data

    def test_register_page(self, client):
        response = client.get('/register')
        assert b'Register' in response.data or b'register' in response.data
        assert b'Username' in response.data
        assert b'Email' in response.data
        assert b'Password' in response.data

    def test_dashboard_requires_login(self, client):
        response = client.get('/dashboard', follow_redirects=True)
        # Should redirect to login or home if not authenticated
        assert b'Login' in response.data or b'login' in response.data or b'Home' in response.data
