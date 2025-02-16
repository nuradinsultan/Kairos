# backend/apps/financial_data/tasks.py
from celery import shared_task
import requests
from django.conf import settings
from .models import Stock
from datetime import datetime
import logging

# Initialize logger
logger = logging.getLogger(__name__)

@shared_task
def fetch_market_data():
    """
    Fetches the latest market data from the Ethiopian Securities Exchange (ESX)
    and updates the stock prices in the database.
    """
    try:
        # Define the API endpoint for ESX market data (you will need the actual URL)
        esx_api_url = "https://api.esx.com/market_data"  # Replace with the real API endpoint
        response = requests.get(esx_api_url)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()

            # Loop through the data and update stock prices
            for stock_data in data:
                symbol = stock_data.get('symbol')
                price = stock_data.get('price')

                # Try to get the stock object from the database
                try:
                    stock = Stock.objects.get(symbol=symbol)
                    stock.current_price = price
                    stock.save()
                    logger.info(f"Updated {symbol} with price {price}")
                except Stock.DoesNotExist:
                    # If the stock does not exist, log an error or create a new stock
                    logger.warning(f"Stock with symbol {symbol} not found in the database.")
                    # Optionally create a new stock if necessary
                    # Stock.objects.create(symbol=symbol, current_price=price)
        else:
            logger.error(f"Failed to fetch market data from ESX. Status code: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred while fetching market data: {str(e)}")


@shared_task
def fetch_and_log_market_data():
    """
    Fetches market data and logs it in the system.
    This can be used for logging historical market data for analysis or auditing.
    """
    try:
        # Example: Log current market data for later use (historical data)
        esx_api_url = "https://api.esx.com/market_data"
        response = requests.get(esx_api_url)

        if response.status_code == 200:
            data = response.json()
            for stock_data in data:
                symbol = stock_data.get('symbol')
                price = stock_data.get('price')
                timestamp = datetime.now()

                # Log the market data (you can store it in a custom model if needed)
                logger.info(f"{timestamp}: {symbol} - {price}")

        else:
            logger.error(f"Failed to fetch market data from ESX. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred while fetching market data: {str(e)}")
