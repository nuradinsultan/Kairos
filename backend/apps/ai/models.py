# backend/apps/ai/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class AIModel(models.Model):
    """
    Stores information about AI models used for trading analysis, predictions, or recommendations.
    """
    name = models.CharField(max_length=255, unique=True)  # AI Model name (e.g., 'Stock Price Predictor')
    description = models.TextField(blank=True, null=True)  # Details about the model's functionality
    version = models.CharField(max_length=50, default="1.0")  # Version of the AI model
    model_file = models.FileField(upload_to='ai_models/', blank=True, null=True)  # Optional model file upload
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (v{self.version})"


class AIAnalysis(models.Model):
    """
    Stores AI-generated analysis, predictions, and insights.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # AI analysis can be user-specific or system-wide
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE)  # AI model used for analysis
    input_data = models.JSONField()  # Raw input data fed into the AI model
    output_data = models.JSONField()  # AI model's predictions or analysis results
    confidence_score = models.FloatField(default=0.0)  # AI model's confidence in its prediction (0-1)
    analysis_type = models.CharField(
        max_length=100,
        choices=[
            ('Price Prediction', 'Price Prediction'),
            ('Market Sentiment', 'Market Sentiment'),
            ('Risk Assessment', 'Risk Assessment'),
            ('Trading Signal', 'Trading Signal')
        ],
        default='Price Prediction'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.analysis_type} - {self.model.name} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


class TradingSignal(models.Model):
    """
    AI-generated trading signals, such as Buy, Sell, or Hold recommendations.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # If personalized signals
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE)  # AI model that generated the signal
    stock_symbol = models.CharField(max_length=20)  # Stock or asset symbol (e.g., 'AAPL')
    signal = models.CharField(
        max_length=10,
        choices=[
            ('Buy', 'Buy'),
            ('Sell', 'Sell'),
            ('Hold', 'Hold'),
            ('Strong Buy', 'Strong Buy'),
            ('Strong Sell', 'Strong Sell')
        ]
    )
    confidence = models.FloatField(default=0.5)  # AI model's confidence score in the signal (0-1)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stock_symbol} - {self.signal} ({self.confidence*100:.1f}%)"


class MarketSentiment(models.Model):
    """
    AI-driven market sentiment analysis based on news, social media, and other sources.
    """
    asset = models.CharField(max_length=50)  # Stock, index, or asset being analyzed (e.g., 'BTC', 'ESX')
    sentiment_score = models.FloatField(default=0.0)  # Sentiment score (-1 = bearish, 1 = bullish)
    summary = models.TextField(blank=True, null=True)  # Summary of AI sentiment analysis
    source_data = models.JSONField()  # Raw data (e.g., news articles, social media posts)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.asset} Sentiment: {self.sentiment_score:.2f}"


class RiskAssessment(models.Model):
    """
    AI-driven risk assessment for trading strategies.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    strategy_name = models.CharField(max_length=255)  # Name of the trading strategy being assessed
    risk_score = models.FloatField(default=0.0)  # AI-generated risk score (0 = low risk, 1 = high risk)
    risk_factors = models.JSONField()  # Key risk factors identified
    recommendations = models.TextField(blank=True, null=True)  # AI-generated recommendations
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.strategy_name} Risk: {self.risk_score:.2f}"
