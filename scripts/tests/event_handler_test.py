import unittest
from unittest.mock import MagicMock, patch
import logging
from scripts.event_handler import EventHandler

class TestEventHandler(unittest.TestCase):
    
    def setUp(self):
        # Create an EventHandler instance with a mocked RadioBuenaVida instance
        self.event_handler = EventHandler()
        self.event_handler.rbv = MagicMock()  # Mock the RadioBuenaVida instance
    
    @patch("logging.info")
    def test_handle_event_create_social_media_assets(self, mock_logging):
        # Trigger the event to create social media assets
        self.event_handler.handle_event("create social media assets")

        # Verify the method call
        self.event_handler.rbv.create_social_media_assets.assert_called_once()
        
        # Check logging output
        mock_logging.assert_any_call("Create Social Media Assets Task Started")
        mock_logging.assert_any_call("Finished Create Social Media Assets Event")

    @patch("logging.info")
    def test_handle_event_create_monthly_color_assets(self, mock_logging):
        # Trigger the event to create monthly color assets
        self.event_handler.handle_event("create monthly color assets")

        # Verify the method call
        self.event_handler.rbv.create_monthly_colors_assets.assert_called_once()
        
        # Check logging output
        mock_logging.assert_any_call("Create Monthly Assets Task Started")
        mock_logging.assert_any_call("Finished Create Monthly Color Assets Event")

    @patch("logging.info")
    def test_handle_event_unsupported_event(self, mock_logging):
        # Trigger an unsupported event
        self.event_handler.handle_event("unsupported event")
        
        # Verify no RadioBuenaVida methods were called
        self.event_handler.rbv.create_social_media_assets.assert_not_called()
        self.event_handler.rbv.create_monthly_colors_assets.assert_not_called()

        # Check logging output for the unsupported event
        mock_logging.assert_called_once_with({"statusCode": 300, "body": "Not Triggered"})

if __name__ == "__main__":
    unittest.main()
