from datetime import datetime 
import pandas as pd

class AssetManager:
    def __init__(self):
        self.month = datetime.now().strftime("%B")

    def get_font(self):
        # Load and return font file for the current month
        pass

    def get_month_color(self):
        # Fetch color from monthly assets
        pass