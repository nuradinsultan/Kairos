from django.conf import settings
from ..models import Agreement

class DocumentService:
    @classmethod
    def generate_agreement(cls, agreement_type, version):
        """
        Retrieve agreement template from storage
        """
        # In production, fetch from document management system
        templates = {
            'TERMS': "This is the terms and conditions agreement...",
            'PRIVACY': "This is the privacy policy agreement..."
        }
        return templates.get(agreement_type, "")

    @classmethod
    def record_signature(cls, user, agreement_type, version, ip, user_agent):
        """
        Record e-signature with audit trail
        """
        content = cls.generate_agreement(agreement_type, version)
        
        agreement = Agreement.objects.create(
            user=user,
            agreement_type=agreement_type,
            version=version,
            content=content,
            ip_address=ip,
            user_agent=user_agent
        )
        
        # Audit trail
        from .audit_service import AuditService
        AuditService.log_action(
            user=user,
            action=f"SIGNED_{agreement_type}",
            metadata={'version': version}
        )
        
        return agreement
