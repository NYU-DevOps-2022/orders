import unittest

from service.error_handlers import request_validation_error, not_found, method_not_supported, mediatype_not_supported, internal_server_error


class TestErrorHandlers(unittest.TestCase):

    def test_request_validation_error(self):
        self.assertEqual(tuple, type(request_validation_error("blah")))

    def test_not_found(self):
        self.assertEqual(tuple, type(not_found("blah")))

    def test_method_not_supported(self):
        self.assertEqual(tuple, type(method_not_supported("blah")))

    def test_mediatype_not_supported(self):
        self.assertEqual(tuple, type(mediatype_not_supported("blah")))

    def test_internal_server_error(self):
        self.assertEqual(tuple, type(internal_server_error("blah")))
