import json
import unittest
from app import app, boggle_game, session

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        """Setup test client"""
        app.testing = True
        self.client = app.test_client()

    def tearDown(self):
        with app.test_request_context():
            session.clear()

    def test_home_page(self):
        """Test home page route"""
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<h1 class="home_title">Boggle!</h1>', response.data)
            self.assertIn(b'<button>Start Game!</button>', response.data)

    def test_boggle_route(self):
        """Test boggle route"""
        with self.client:
            response = self.client.get('/boggle')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<h1>Boggle!</h1>', response.data)
            self.assertIn(b'<table>', response.data)
            self.assertTrue(session.get("game"))

    def test_make_guess_route(self):
        """Test make guess route"""
        with self.client:
            # This line needs to be inside a request context. Instead, you can initialize a game by calling the /boggle route.
            # session["game"] = boggle_game.make_board()
            self.client.get('/boggle')  # This will initialize the game and set the session["game"]
            response = self.client.post('/guess', json={'guess': 'test'})
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn("status", data)
            self.assertEqual(data["status"], "success")

            # Test an already guessed word
            response = self.client.post('/guess', data=json.dumps({"guess": "test"}), content_type='application/json')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data["status"], "failure")
            self.assertEqual(data["message"], "Word already guessed")
            self.assertEqual(data["guess"], "test")

    def test_game_over_route(self):
        """Test game over route"""
        with self.client:
            # Send POST request without a prior score
            response = self.client.post('/gameover', data=json.dumps({"score": "5"}), content_type='application/json')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data["status"], "success")
            self.assertEqual(data["message"], "Score recieved")
            self.assertEqual(data["score"], "5")
            self.assertEqual(session.get('times_played'), 1)

            # Set up a game session with a prior score

        with app.test_request_context():
            session['score'] = 3
            session['times_played'] = 1


            response = self.client.post('/gameover', data=json.dumps({"score": "7"}), content_type='application/json')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data["score"], "7")
            self.assertEqual(session.get('highscore'), 7)
            self.assertEqual(session.get('times_played'), 2)

if __name__ == '__main__':
    unittest.main()
