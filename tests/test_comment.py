from app.models import User,Comment,Pitch
from app import db
import unittest

class CommentModelTest(unittest.TestCase):

    def setUp(self):
        self.user_Ruth = User(
            username='Ruth', password='2603@ruth', email='ruthjomo19@gmail.com')
        self.new_comment = Comment(
            comment='laugh now,cry later', user=self.user_Ruth, pitch_id=12)

    def tearDown(self):
        Comment.query.delete()
        User.query.delete()

    def test_check_instance_variable(self):
        self.assertEquals(self.new_comment.comment, Great)
        self.assertEquals(self.new_comment.user, self.user_Ruth)
        self.assertEquals(self.new_comment.pitch_id, 12)

    def test_save_comment(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all()) > 0)

    def test_get_comment_by_id(self):

        self.new_comment.save_comment()
        got_comments = Comment.get_comments(12)
        self.assertTrue(len(got_comments) == 1)