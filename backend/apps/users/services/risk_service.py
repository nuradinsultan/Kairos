from ..models import User

class RiskService:
    @classmethod
    def evaluate_user_risk(cls, user):
        """
        Comprehensive risk assessment for Ethiopian users
        """
        risk_score = 0
        
        # Basic risk factors
        if user.role in ['retail_investor', 'trader']:
            risk_score += 10
        elif user.role == 'institutional_investor':
            risk_score += 30
            
        # Onboarding completeness
        if not user.is_verified:
            risk_score += 20
            
        # Document verification
        if not user.kyc_documents.filter(status='APPROVED').exists():
            risk_score += 25
            
        return {
            'risk_score': risk_score,
            'risk_level': cls._determine_risk_level(risk_score),
            'factors': cls._get_risk_factors(user)
        }

    @staticmethod
    def _determine_risk_level(score):
        if score > 50:
            return 'high'
        elif score > 25:
            return 'medium'
        return 'low'

    @staticmethod
    def _get_risk_factors(user):
        factors = []
        if not user.is_verified:
            factors.append('unverified_user')
        if not user.kyc_documents.filter(status='APPROVED').exists():
            factors.append('missing_kyc')
        return factors
