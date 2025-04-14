import requests
from django.conf import settings
from django.utils import timezone
from ..models import KYCDocument, User
from ..enums import KYCStatus

class KYCService:
    @classmethod
    def process_document_async(cls, document_id):
        """
        Trigger async KYC document processing
        """
        from ..tasks import process_kyc_document
        process_kyc_document.delay(document_id)

    @classmethod
    def process_document(cls, document_id):
        """
        Process KYC document with AML checks
        """
        document = KYCDocument.objects.get(id=document_id)
        
        # Step 1: Document verification
        verification_result = cls._verify_document(document)
        
        # Step 2: AML check
        aml_result = cls._aml_check(document)
        
        # Update document status
        document.metadata = {
            'verification': verification_result,
            'aml': aml_result,
            'processed_at': str(timezone.now())
        }
        
        if verification_result['valid'] and aml_result['risk_level'] == 'low':
            document.status = KYCStatus.APPROVED.value
            cls._approve_user(document.user)
        else:
            document.status = KYCStatus.REVIEW_REQUIRED.value
        
        document.reviewed_at = timezone.now()
        document.save()
        return document

    @classmethod
    def _verify_document(cls, document):
        """
        Integrate with document verification service
        """
        if settings.DEBUG:
            return {'valid': True, 'reason': 'DEV_MODE'}
            
        response = requests.post(
            settings.DOC_VERIFICATION_URL,
            files={'document': document.document_front.file},
            headers={'Authorization': f'Bearer {settings.DOC_VERIFICATION_KEY}'}
        )
        return response.json()

    @classmethod
    def _aml_check(cls, document):
        """
        Perform AML screening
        """
        if settings.DEBUG:
            return {'risk_level': 'low', 'score': 10}
            
        response = requests.post(
            settings.AML_SERVICE_URL,
            json={
                'user_id': str(document.user.id),
                'document_type': document.document_type
            },
            headers={'Authorization': f'Bearer {settings.AML_SERVICE_KEY}'}
        )
        return response.json()

    @classmethod
    def _approve_user(cls, user):
        """
        Approve user after successful KYC
        """
        user.is_verified = True
        user.save()
