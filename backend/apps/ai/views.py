# backend/apps/ai/views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import AIModel, AIAnalysis, TradingSignal, MarketSentiment, RiskAssessment
from django.core.serializers import serialize
import json
import logging

logger = logging.getLogger(__name__)

# --- API for AI-Powered Trading Recommendations ---

class TradingSignalView(View):
    """
    API to fetch AI-generated trading signals.
    """

    def get(self, request, stock_symbol):
        """
        Retrieve the latest AI trading signal for a specific stock.
        """
        try:
            signal = TradingSignal.objects.filter(stock_symbol=stock_symbol).order_by('-generated_at').first()
            if not signal:
                return JsonResponse({"error": "No trading signals available for this stock."}, status=404)
            
            response_data = {
                "stock_symbol": signal.stock_symbol,
                "signal": signal.signal,
                "confidence": signal.confidence,
                "generated_at": signal.generated_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            return JsonResponse(response_data, status=200)
        except Exception as e:
            logger.error(f"Error fetching trading signal: {str(e)}")
            return JsonResponse({"error": "An error occurred while fetching trading signals."}, status=500)


class MarketSentimentView(View):
    """
    API to fetch AI-driven market sentiment analysis.
    """

    def get(self, request, asset):
        """
        Retrieve market sentiment analysis for a given asset (stock, index, or currency).
        """
        try:
            sentiment = MarketSentiment.objects.filter(asset=asset).order_by('-created_at').first()
            if not sentiment:
                return JsonResponse({"error": "No sentiment data available for this asset."}, status=404)

            response_data = {
                "asset": sentiment.asset,
                "sentiment_score": sentiment.sentiment_score,
                "summary": sentiment.summary,
                "created_at": sentiment.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            return JsonResponse(response_data, status=200)
        except Exception as e:
            logger.error(f"Error fetching market sentiment: {str(e)}")
            return JsonResponse({"error": "An error occurred while fetching market sentiment data."}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class PricePredictionView(View):
    """
    API to retrieve AI-powered price predictions.
    """

    def post(self, request):
        """
        Predict future prices based on historical data input (JSON format).
        """
        try:
            data = json.loads(request.body)
            stock_symbol = data.get("stock_symbol")
            input_data = data.get("input_data")

            if not stock_symbol or not input_data:
                return JsonResponse({"error": "Stock symbol and input data are required."}, status=400)

            # Simulating AI model prediction (replace this with actual model inference)
            predicted_price = float(input_data[-1]) * 1.05  # Example: Predict 5% increase

            # Save AI analysis result
            ai_model, _ = AIModel.objects.get_or_create(name="Price Predictor AI", version="1.0")
            analysis = AIAnalysis.objects.create(
                model=ai_model,
                input_data=input_data,
                output_data={"predicted_price": predicted_price},
                confidence_score=0.85,  # Example confidence
                analysis_type="Price Prediction"
            )

            response_data = {
                "stock_symbol": stock_symbol,
                "predicted_price": predicted_price,
                "confidence": analysis.confidence_score,
                "created_at": analysis.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            return JsonResponse(response_data, status=200)
        except Exception as e:
            logger.error(f"Error processing price prediction: {str(e)}")
            return JsonResponse({"error": "An error occurred while processing the prediction."}, status=500)


@login_required
def user_risk_assessment(request):
    """
    API to fetch AI-driven risk assessment for the user's trading strategies.
    """
    try:
        assessments = RiskAssessment.objects.filter(user=request.user).order_by('-created_at')
        if not assessments.exists():
            return JsonResponse({"error": "No risk assessment data found."}, status=404)

        assessments_data = serialize("json", assessments)
        return JsonResponse({"risk_assessments": json.loads(assessments_data)}, status=200)
    except Exception as e:
        logger.error(f"Error fetching risk assessments: {str(e)}")
        return JsonResponse({"error": "An error occurred while fetching risk assessment data."}, status=500)
