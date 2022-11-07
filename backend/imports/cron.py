from buckets.utils import BucketUtils
from imports.utils import WorkBook
from imports.models import Import
from products.models import Attribute
from orders.models import OrderDetail
from datetime import datetime
from django.conf import settings
import os

def imports_job():
    objs=Import.objects.filter(status="N").order_by('create')

    
    if objs.exists():
        obj=objs[0]
        
        workbook=WorkBook()
        
        try:
            isCSV=False
            extension=obj.filename.split(".")[-1]
            if extension in ["csv","txt"]:
                isCSV=True
                obj.datasheet["sheetindex"]=0

            workbook.load_workbook_from_path(os.path.join(settings.PRIVATE_DIR,obj.path,obj.filename),isCSV)
            
            # se c'è uno sheetindex ed è in stato U
            # restituisco il foglio
            if obj.datasheet["sheetindex"]!="":
                if obj.datasheet["index"]!=obj.datasheet["sheetindex"]:
                    datasheet=workbook.datasheet(int(obj.datasheet["sheetindex"]),cut=True)
                    obj.datasheet["datasheet"]=datasheet
                    obj.datasheet["index"]=obj.datasheet["sheetindex"]
                    attributes={}
                    if obj.ftype=="products":
                        print("PRODUCTS")
                        for attrObj in Attribute.objects.filter(company=obj.company).order_by("name"):
                            attributes[attrObj.name]=attrObj.description
                    elif obj.ftype=="orders":
                        print("ORDER")
                        for attrObj in OrderDetail._meta.fields:
                            attributes[attrObj]=OrderDetail._meta.get_field(attrObj).verbose_name
                    obj.datasheet["attributes"]=attributes
                    obj.status="C"
                    obj.save()
                    

            elif obj.datasheet["sheetnames"]==[]:
                obj.datasheet["sheetnames"]=workbook.sheetnames()
                obj.status="C"
                obj.save()

        

            
            
        except:
            print("Errore")
            obj.status="E"
            obj.save()
        
        workbook.close()
    
    
    
def process_imports_job():
    
    objs=Import.objects.filter(status="W").order_by('create')
    print(datetime.now())
    if objs.exists():
        print("Eseguo")

        obj=objs[0]
        obj.status="R"
        obj.save()
        workbook=WorkBook()
        isCSV=False
        extension=obj.filename.split(".")[-1]
        if extension in ["csv","txt"]:
            isCSV=True
        try:
            workbook.load_workbook_from_path(os.path.join(settings.PRIVATE_DIR,obj.path,obj.filename),isCSV)
            jump=obj.datasheet["jump"] # 2
            columns=obj.datasheet["columns"]
            rows=obj.datasheet["rows"]
            
            fields={}
            for key,value in columns.items():
                if value not in ["",None]:
                    fields[str(key)]={}
                    fields[str(key)]["name"]=value
                    if obj.ftype=="products":
                        fields[str(key)]["type"]=Attribute.objects.get(company=obj.company,name=value).type
                    elif obj.ftype=="orders":
                        fields[str(key)]["type"]=OrderDetail.objects.get(name=value).type

            sheetindex=obj.datasheet["index"]
            if obj.ftype=="products":
                messages=workbook.importDatasheetToProducts(company=obj.company,sheetindex=sheetindex,jump=jump,columns=fields,rows=rows,marketplaces=obj.marketplace)
            elif obj.ftype=="orders":
                messages=workbook.importDatasheetToOrders(company=obj.company,sheetindex=sheetindex,jump=jump,columns=fields,rows=rows,marketplace=obj.marketplace)
            obj.messages=messages
            obj.status="D"
            obj.save()
        except Exception as exc:
            obj.status="E"
            obj.messages={0:"Errore non gestito. "+str(exc)}
            obj.save()

        workbook.close()
        
        