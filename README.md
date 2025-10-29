# TTB

Web app to replace manual inspection of liquor labels.

Key Objectives:
- Build a web UI for inputting form data (some key fields from a TTB label application) and uploading an
 image of an alcohol label. DONE.
- Implement a backend service that uses basic AI (e.g. OCR or image analysis) to extract information from
 the label image. DONE.
- Compare the extracted label information with the form inputs and determine if they match (just like a TTB
 agent would verify a label). DONE.
- Display clear results to the user indicating success (if everything matches) or failure (if discrepancies are
 found), along with details on what was verified. DONE.
- Ensure the app handles various scenarios (matching info, mismatched info, missing fields on the label,
 unreadable image, etc.) gracefully and clearly. BASICS.

Front end is html and back end is python. Backend uses pytesseract and, experimentally,
 PIL.  This was all to "Keep it as simple as possible."  I also prioritized in the time 
available correct data ops and logic first starting from primitive UI as "this is not
 primarily a design test"
 (so, too, as should be in the real world; among other things burns off risk early).  Anything
 rapidly and readily usable and working is better than manual or mainframe, especially for
the taxpayer.

https://github.com/ksipfle/TTB
tns_999_999_999@yahoo.com
TTBexercise99!

Did development on Xubuntu linux on WSL and the webserver is on linux Centos 8.

"Deployment: We’d like to see the app deployed live."
Running at http://142.11.238.224 on django web server on a server I have for website 
tinkering. Ran it on nginx in the past but "The app doesn’t need to handle heavy traffic" 

"This project is intended to be completed in about one day, so scope your solution 
accordingly."
"Feel free to note how you would extend it if given more time"
Exercise it more and make it robust and make it prettier, to the degree the ROI and 
opportunity cost are good.

"Feel free to mention any bonus features you implement (or attempted) in your documentation 
so we don’t overlook them."
I spent time trying trying to get any decent recognition of real labels from tesseract 
with preprocessing help from PIL.  My conclusion is that for various (many) photographs from
 bottles these tools are too weak and flaky.  Would need to try on submitted fresh flat 
actual labels or images thereof.

-ksipfle@umich.edu
