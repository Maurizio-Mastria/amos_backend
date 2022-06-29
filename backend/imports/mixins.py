from pprint import PrettyPrinter
from buckets.utils import BucketUtils
from buckets.models import Bucket
from .models import Import

from rest_framework.exceptions import APIException,PermissionDenied
from companies.models import Company
from django.db.utils import IntegrityError
from rest_framework.response import Response
from marketplaces.models import Marketplace
from datetime import datetime
import os
from django.conf import settings
import shutil
from django.http import HttpResponse,HttpResponseNotFound

class ImportMixin(object):
    def get_queryset(self):
        queryset=super().get_queryset()
        for key in self.request.GET:
            queryset=queryset.filter(**{key:self.request.GET.get(key)})
        return queryset

    

    def create(self,request):
        try:
            inRunningObj=Import.objects.filter(company=Company.objects.get(id=self.request.data["company"]))
            inRunningObj=inRunningObj.filter(status="C")|inRunningObj.filter(status="N")
            if inRunningObj.exists():
                raise PermissionDenied(detail="Puoi effettuare un solo import per volta.")
            for marketID in self.request.data["marketplace"].split(","):
                if not Marketplace.objects.filter(id=marketID,company=self.request.data["company"]).exists():
                    raise PermissionDenied(detail="Marketplace non valido/i")
            
            if "file" not in self.request.FILES or self.request.FILES["file"] in [None,""]:
                raise APIException(detail="File non valido o inesistente!")
            extension=str(self.request.FILES["file"].name).split(".")[-1]
            
            if extension not in ["csv",'odt','txt','xlsm','xls','xlsx']:
                raise PermissionDenied(detail="Formato file non supportato!")
            now=datetime.now()
            if self.request.data["ftype"] not in ["products","orders","prices","qty"]:
                raise APIException(detail="Tipo di import non valido!")
            filename=now.strftime("%Y%m%d%H%M%S")+"_import_"+self.request.data["ftype"]+"."+extension
            relative_path=os.path.join(Company.objects.get(id=self.request.data["company"]).vid,"import",self.request.data["ftype"])
            path=os.path.join(settings.PRIVATE_DIR,relative_path)
            datasheet={}
            datasheet["datasheet"]={}
            datasheet["index"]=""
            datasheet["sheetindex"]=""
            datasheet["sheetnames"]=[]
            datasheet["availablesFields"]=[]
                
            if not os.path.exists(path):
                os.makedirs(path,exist_ok=True)
            shutil.move(self.request.FILES["file"].temporary_file_path(), os.path.join(path,filename))
            
            importObj=Import()
            importObj.path=relative_path
            importObj.ftype=self.request.data["ftype"]
            importObj.company=Company(id=self.request.data["company"])
            importObj.filename=filename
            importObj.datasheet=datasheet
            try:
                importObj.save()
            except:
                os.remove(os.path.join(path,filename))
            for marketID in self.request.data["marketplace"].split(","):
                importObj.marketplace.add(Marketplace.objects.get(id=marketID,company=Company(id=self.request.data["company"])))
            importObj.save()
                
            return Response({"detail":"File caricato","id":importObj.id})
                    
            
        except IntegrityError:
            raise PermissionDenied(detail="%s già esistente" % (self.model._meta.verbose_name))
        
        
    
    def update(self,request,pk):
        if Import.objects.filter(id=pk,company=Company.objects.get(id=self.request.data["company"]),status="N").exists():
            raise PermissionDenied(detail="Attendi il controllo del file.")
        importObj=Import.objects.get(id=pk,company=Company.objects.get(id=self.request.data["company"]),status="C")
        importObj.datasheet["sheetindex"]=int(request.data["sheetindex"])
        if "columns" in request.data and "jump" in request.data and "rows" in request.data:
            try:
                importObj.datasheet["columns"]=request.data["columns"]
                importObj.datasheet["jump"]=int(request.data["jump"])
                importObj.datasheet["rows"]=request.data["rows"]
                importObj.status="W"
                importObj.save()
            except:
                pass
        else:
            importObj.status="N"
            importObj.save()
        return Response({"detail":"Richiesta inviata"})
       
        

  

class ImportFileMixin(object):
    def retrieve(self,request,pk):
        
        try:
            importObj=Import.objects.get(id=pk,company=Company.objects.get(id=self.request.GET.get("company")))
                  
            if os.path.exists(os.path.join(settings.PRIVATE_DIR,importObj.path,importObj.filename)):
                print("exists")
                with open(os.path.join(settings.PRIVATE_DIR,importObj.path,importObj.filename), 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                    response['Content-Disposition'] = 'inline; filename=' + importObj.filename
                    return response
            return HttpResponseNotFound(str(os.path.join(settings.PRIVATE_DIR,importObj.path,importObj.filename)))
        except:
            return HttpResponseNotFound(str(os.path.join(settings.PRIVATE_DIR,importObj.path,importObj.filename)))


        

        
    

