#Due and delivered 20251029
#Small edits added early 20251030, all commented, for better satisfaction of last Objective:
#"Ensure the app handles various scenarios (matching info, mismatched info, missing fields
# on the label, unreadable image, etc.) gracefully and clearly."

#from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt #
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import requires_csrf_token

#from PIL import image
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter
import pytesseract

from time import time

# Create your views here.
from django.http import HttpResponse
from django.http import FileResponse

def index(request):
    with open('ttbapp/pages/index.html', 'r') as file:
        content = file.read()
    return HttpResponse(content)


@csrf_exempt
def results(request):

    # get user-specfied image file data
    if "file" in request.FILES:
        file = request.FILES["file"]
        img = file.read()

        uniquifier = str(time())
        origfile = open("uploadedimagefile" + uniquifier, "wb")
        origfile.write(img)
        origfile.close()
        #origfile = open("uploadedimagefile" + uniquifier + ".jpg", "wb") #
        #origfile.write(img) #
        #origfile.close() #

        ## pre-process the image. this section is for the experimental ##
        img = Image.open("uploadedimagefile" + uniquifier)
        exif=img.info.get("exif")
        ###img = img.convert("1") # to just black, and white
        #img = img.convert("L") # to grayscale
        #enhancer = ImageEnhance.Contrast(img)
        #img = enhancer.enhance(2)
        #enhancer = ImageEnhance.Sharpness(img)
        #img = enhancer.enhance(4.0)
        #enhancer = ImageEnhance.Color(img)
        #img = enhancer.enhance(0.0)
        #img = img.filter()
        #didnt help img = img.filter(ImageFilter.CONTOUR)
        #didnt help img = img.filter(ImageFilter.FIND_EDGES)
        #img = img.filter(ImageFilter.SHARPEN)
        #img = img.convert("1") # to just black, and white
        #img = img.filter(ImageFilter.MaxFilter(size=3))
        #img = img.filter(ImageFilter.MinFilter(size=3))
        #img = img.resize((200, 200))
        ###typically helpful img = img.filter(ImageFilter.MedianFilter(size=3))
        #img = img.convert("1") # to just black, and white
        if (exif):
            img.save("workfile" + uniquifier + ".jpg", exif=exif) #2nd param prevents spurious rotates on save
        else:
            img.save("workfile" + uniquifier + ".jpg")
        #img.save("workfile" + uniquifier + ".jpg", exif=exif, quality=25) #2nd param prevents spurious rotates on save
        #img.save("workfile" + uniquifier + ".jpg", exif=exif, dpi=(10, 10)) #2nd param prevents spurious rotates on save
        ##img.save("workfile" + uniquifier + ".bmp")

        ## OCR the preprocessed image(s).  this section includes the experimental re options ##
        ocrtext = pytesseract.image_to_string("workfile" + uniquifier + ".jpg")
        #ocrtext = pytesseract.image_to_string("workfile" + uniquifier + ".jpg", config="--psm 1")
        #ocrtext = pytesseract.image_to_string("workfile" + uniquifier + ".jpg", config="--psm 12")
        #ocrtext = pytesseract.image_to_string("workfile" + uniquifier + ".jpg", config="--psm 11")
        #ocrtext = pytesseract.image_to_string"workfile" + uniquifier + ".bmp")


        # check fields
        # search for the form field's data in the OCR text, allowing for some small errors
        brand = request.POST["brand"]
        type =  request.POST["class/type"]
        pct =   request.POST["pctalcohol"]
        ml =    request.POST["ml"]
        oz =    request.POST["oz"]

        # 20251030 0630ET for more clarity to user add " ENTRY" after "MISSING"
        msgbrand = "                          "
        msgtype =  "                          "
        msgpct =   "                          "
        msgml =    "                          "
        msgoz =    "                          "
        success = True
        if not brand:
            msgbrand = "REQUIRED AND MISSING ENTRY"
            success = False
        else:
            msgbrand = check_for_brand(ocrtext, brand)
            if "NOT FOUND" in msgbrand:
                success = False
        if not type:
            msgtype  = "REQUIRED AND MISSING ENTRY"
            success = False
        else:
            msgtype = check_for_type(ocrtext, type)
            if "NOT FOUND" in msgtype:
                success = False
        if not pct:
            msgpct  =  "REQUIRED AND MISSING ENTRY"
            success = False
        else:
            msgpct = check_for_pct(ocrtext, pct)
            if "NOT FOUND" in msgpct:
                success = False
        msgml =    "missing entry             "
        msgoz =    "missing entry             "
        if ml and ml != "":
            msgml = check_for_ml(ocrtext, ml)
        if oz and oz != "":
            msgoz = check_for_oz(ocrtext, oz)
        if "NOT FOUND" in msgml or "NOT FOUND" in msgoz:
            success = False

        # report the results to user
        if success:
            msgsummary = "The label matches the form data. All required information is consistent."
        else:
            msgsummary = "The label does not match the form."
        if not ocrtext or ocrtext == "":  # 20251030 0630ET added this case
            msgsummary = "Could not read text from the label image. Please try a clearer image."
        with open('ttbapp/pages/results.html', 'r') as file:
            content = file.read()
        content = content.replace("%summaryresult%", msgsummary)
        content = content.replace("%brandresult%", msgbrand)
        content = content.replace("%brand%", brand)
        content = content.replace("%typeresult%", msgtype)
        content = content.replace("%type%", type)
        content = content.replace("%alcresult%", msgpct)
        content = content.replace("%alc%", pct)
        content = content.replace("%mlresult%", msgml)
        content = content.replace("%ml%", ml)
        content = content.replace("%ozresult%", msgoz)
        content = content.replace("%oz%", oz)
        content = content.replace("%unique%", uniquifier)
        #content = content.replace("%%", "")
        content = content.replace("%%", ocrtext)
        return HttpResponse(content)


# 20251030 0630ET added upper()s and surrounding string context to pct, ml, oz
def check_for_brand(haystack, needle):
    if needle.upper() in haystack.upper(): 
        return "FOUND               "
    else:
        return "NOT FOUND           "
def check_for_type(haystack, needle):
    if needle.upper() in haystack.upper():
        return "FOUND               "
    else:
        return "NOT FOUND           "
def check_for_pct(haystack, needle):
    if (needle + " %").upper() in haystack.upper() or (needle + "%").upper() in haystack.upper():
        return "FOUND               "
    else:
        return "NOT FOUND           "
def check_for_ml(haystack, needle):
    if (needle + " m").upper() in haystack.upper() or (needle + "m").upper() in haystack.upper():
        return "FOUND               "
    else:
        return "NOT FOUND           "
def check_for_oz(haystack, needle):
    found1 = (needle + " o").upper() in haystack.upper() or (needle + "o").upper() in haystack.upper()
    found2 = (needle + " 0").upper() in haystack.upper() or (needle + "0").upper() in haystack.upper()
    if found1 or found2:
        return "FOUND               "
    else:
        return "NOT FOUND           "
