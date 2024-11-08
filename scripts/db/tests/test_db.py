import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from scripts.db import DatabaseHandler

class TestDatabaseHandler(unittest.TestCase):

    def setUp(self):
        # Initialize the DatabaseHandler instance for testing
        self.db_handler = DatabaseHandler()

    @patch("root.scripts.db_handler.psycopg2.connect")
    def test_connect_success(self, mock_connect):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        
        self.db_handler.connect()
        
        self.assertIsNotNone(self.db_handler.connection)
        self.assertIsNotNone(self.db_handler.cursor)
        mock_connect.assert_called_once()
        mock_connection.cursor.assert_called_once()
    
    @patch("root.scripts.db_handler.psycopg2.connect", side_effect=Exception("Connection error"))
    def test_connect_failure(self, mock_connect):
        with self.assertLogs(level='ERROR') as log:
            self.db_handler.connect()
            self.assertIn("Error connecting to the database: Connection error", log.output[0])

    @patch("root.scripts.db_handler.DatabaseHandler.connect")
    def test_execute_query_success(self, mock_connect):
        mock_cursor = MagicMock()
        self.db_handler.cursor = mock_cursor
        mock_cursor.fetchall.return_value = [("row1",), ("row2",)]
        
        result = self.db_handler.execute_query("SELECT * FROM test_table")
        self.assertEqual(result, [("row1",), ("row2",)])
        mock_cursor.execute.assert_called_once_with("SELECT * FROM test_table", None)
        mock_cursor.fetchall.assert_called_once()

    @patch("root.scripts.db_handler.DatabaseHandler.connect")
    def test_execute_query_failure(self, mock_connect):
        mock_cursor = MagicMock()
        self.db_handler.cursor = mock_cursor
        mock_cursor.execute.side_effect = Exception("Query error")
        
        with self.assertLogs(level='ERROR') as log:
            result = self.db_handler.execute_query("SELECT * FROM test_table")
            self.assertIsNone(result)
            self.assertIn("Error executing query: Query error", log.output[0])

    @patch("root.scripts.db_handler.DatabaseHandler.connect")
    def test_get_current_radio_shows_success(self, mock_connect):
        # Mock cursor and sample data
        mock_cursor = MagicMock()
        self.db_handler.cursor = mock_cursor
        mock_cursor.fetchall.return_value = [
            (1, "Show1", "2024-01-01", "2024-01-02"),
            (2, "Show2", "2024-01-05", "2024-01-06")
        ]
        mock_cursor.description = [("id",), ("name",), ("created_at",), ("show_date",)]
        
        result = self.db_handler.get_current_radio_shows()
        
        # Check if result is a DataFrame with expected data
        expected_df = pd.DataFrame(
            [
                (1, "Show1", "2024-01-01", "2024-01-02"),
                (2, "Show2", "2024-01-05", "2024-01-06")
            ],
            columns=["id", "name", "created_at", "show_date"]
        )
        pd.testing.assert_frame_equal(result, expected_df)

    @patch("root.scripts.db_handler.DatabaseHandler.connect")
    def test_get_current_radio_shows_failure(self, mock_connect):
        # Mock a failing scenario where cursor throws an exception
        mock_cursor = MagicMock()
        self.db_handler.cursor = mock_cursor
        mock_cursor.execute.side_effect = Exception("Query error")
        
        with self.assertLogs(level='ERROR') as log:
            result = self.db_handler.get_current_radio_shows()
            self.assertIsNone(result)
            self.assertIn("Error executing get_current_radio_show query: Query error", log.output[0])

    @patch("root.scripts.db_handler.DatabaseHandler.connect")
    def test_close_connection(self, mock_connect):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        self.db_handler.connection = mock_connection
        self.db_handler.cursor = mock_cursor
        
        self.db_handler.close()
        
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

if __name__ == "__main__":
    unittest.main()
