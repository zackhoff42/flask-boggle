from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config["TESTING"] = True


class FlaskTests(TestCase):

    def setUp(self):
        """Runs before every test."""

        self.client = app.test_client()

    def test_homepage(self):
        """Test the homepage and initial session."""

        with self.client:
            res = self.client.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<p>Times played:", html)
            self.assertIn("game_board", session)
            self.assertIsNone(session.get("highscore"))
            self.assertIsNone(session.get("times_played"))

    def test_check_validity(self):
        """Changes the game_board in the session and tests check_validity()"""

        with self.client as client:
            with client.session_transaction() as change_session:
                change_session["game_board"] = [
                    ["V", "A", "L", "I", "D"],
                    ["V", "A", "L", "I", "D"],
                    ["V", "A", "L", "I", "D"],
                    ["V", "A", "L", "I", "D"],
                    ["V", "A", "L", "I", "D"],
                ]

            res = self.client.get("/check?guess=valid")
            self.assertEqual(res.json["result"], "ok")

            res_not_on_board = self.client.get("/check?guess=invalid")
            self.assertEqual(res_not_on_board.json["result"], "not-on-board")

            res_not_word = self.client.get("/check?guess=asdfjkl")
            self.assertEqual(res_not_word.json["result"], "not-word")
