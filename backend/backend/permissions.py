from pprint import PrettyPrinter
import profiles.views
from rest_framework.permissions import BasePermission,SAFE_METHODS
from companies.models import Company
# Super user 
class IsSuperUser(BasePermission):
    def has_permission(self,request,view):
        if request.user.is_superuser:
            return True
        return False


class IsSuperUserReadOnly(BasePermission):
    def has_permission(self,request,view):
        if request.user.is_superuser and request.method in SAFE_METHODS:
            return True
        return False


class IsStaff(BasePermission):
    def has_permission(self,request,view):
        if request.user.is_staff:
            return True
        return False

class IsStaffReadOnly(BasePermission):
    def has_permission(self,request,view):
        if request.user.is_staff and request.method in SAFE_METHODS:
            return True
        return False

class IsVendor(BasePermission):
    def has_permission(self,request,view):
        company=Company.objects.filter(vendors=request.user)
        if company.exists():
            return True
        return False
    
class IsVendorReadOnly(BasePermission):
    def has_permission(self,request,view):
        if Company.objects.filter(vendors=request.user).exists() and request.method in SAFE_METHODS:
            return True
        return False

class IsVendorObject(BasePermission):
    def has_permission(self,request,view):
        if request.method in SAFE_METHODS and Company.objects.filter(vendors=request.user,id=request.GET.get("company")).exists():
            return True
        elif request.method in ["POST","PUT","DELETE"] and Company.objects.filter(vendors=request.user,id=request.data["company"]).exists():
            return True
        return False

class IsVendorObjectReadOnly(BasePermission):
    def has_permission(self,request,view):
        if request.method in SAFE_METHODS and Company.objects.filter(vendors=request.user,id=request.GET.get("company")).exists():
            return True
        return False

class IsVendorStaff(BasePermission):
    def has_permission(self,request,view):
        company=Company.objects.filter(staff=request.user)
        if company.exists():
            return True
        return False
    
class IsVendorStaffReadOnly(BasePermission):
    def has_permission(self,request,view):
        if Company.objects.filter(staff=request.user).exists() and request.method in SAFE_METHODS:
            return True
        return False

class IsVendorStaffObject(BasePermission):
    def has_permission(self,request,view):
        if request.method in SAFE_METHODS and Company.objects.filter(staff=request.user,id=request.GET.get("company")).exists():
            return True
        elif request.method in ["POST","PUT","DELETE"] and Company.objects.filter(staff=request.user,id=request.data["company"]).exists():
            return True
        return False

class IsVendorStaffObjectReadOnly(BasePermission):
    def has_permission(self,request,view):
        if request.method in SAFE_METHODS and Company.objects.filter(staff=request.user,id=request.GET.get("company")).exists():
            return True
        return False

class IsVendorCollaborator(BasePermission):
    def has_permission(self,request,view):
        company=Company.objects.filter(collaborators=request.user)
        if company.exists():
            return True
        return False
    
class IsVendorCollaboratorReadOnly(BasePermission):
    def has_permission(self,request,view):
        if Company.objects.filter(collaborators=request.user).exists() and request.method in SAFE_METHODS:
            return True
        return False

class IsVendorCollaboratorObject(BasePermission):
    def has_permission(self,request,view):
        if request.method in SAFE_METHODS and Company.objects.filter(collaborators=request.user,id=request.GET.get("company")).exists():
            return True
        elif request.method in ["POST","PUT","DELETE"] and Company.objects.filter(collaborators=request.user,id=request.data["company"]).exists():
            return True
        return False

class IsVendorCollaboratorObjectReadOnly(BasePermission):
    def has_permission(self,request,view):
        if request.method in SAFE_METHODS and Company.objects.filter(collaborators=request.user,id=request.GET.get("company")).exists():
            return True
        return False