# -*- coding: utf-8 -*-

import unittest
import tempfile
import os
import hydrus.app as views
from hydrus.data.generator import gen_random_object


class ViewsTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, views.app.config['DATABASE'] = tempfile.mkstemp()
        views.app.config['TESTING'] = True
        self.app = views.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(views.app.config['DATABASE'])

    def test_Index(self):
        response_get = self.app.get("/api")
        response_post = self.app.post("/api", data={})
        response_delete = self.app.delete("/api")
        assert response_get.status_code == 200
        assert response_post.status_code == 405
        assert response_delete.status_code == 405

    def test_EntryPoint(self):
        response_get = self.app.get("/api/contexts/EntryPoint.jsonld")
        response_post = self.app.post(
            "/api/contexts/EntryPoint.jsonld", data={})
        response_delete = self.app.delete("/api/contexts/EntryPoint.jsonld")
        assert response_get.status_code == 200
        assert response_post.status_code == 405
        assert response_delete.status_code == 405

    def test_Vocab(self):
        response_get = self.app.get("/api/vocab#")
        response_post = self.app.post("/api/vocab#", data={})
        response_delete = self.app.delete("/api/vocab#")
        assert response_get.status_code == 200
        assert response_post.status_code == 405
        assert response_delete.status_code == 405

    def test_CotsContext(self):
        response_get = self.app.get("/api/contexts/Cots.jsonld")
        response_post = self.app.post("/api/contexts/Cots.jsonld", data={})
        response_delete = self.app.delete("/api/contexts/Cots.jsonld")
        assert response_get.status_code == 200
        assert response_post.status_code == 405
        assert response_delete.status_code == 405

    def test_Cots(self):
        response_get = self.app.get("/api/cots/1")
        response_post = self.app.post(
            "/api/cots/1", object_=gen_random_object())
        response_patch = self.app.patch(
            "/api/cots/1", object_=gen_random_object())
        response_delete = self.app.delete("/api/cots/1")

        # TO BE IMPLEMENTED


if __name__ == '__main__':
    unittest.main()
