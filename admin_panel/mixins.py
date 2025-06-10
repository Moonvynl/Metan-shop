from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied

class ContentManagerRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission() 
        
        if not request.user.access == 'CM':
            raise PermissionDenied
            
        return super().dispatch(request, *args, **kwargs)


class OrderManagerRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.user.access == 'OM':
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.user.access == 'AD':
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)