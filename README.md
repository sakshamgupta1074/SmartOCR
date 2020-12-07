# HACKPIONS – EY GDS Hackathon
## Theme- Image to Text
## Team Name – Trinity
## Idea Name – Smart OCR for Organizational Chart

![LOGO](https://user-images.githubusercontent.com/39915573/101400762-5f302380-38f7-11eb-8957-371e926faa92.png | width=500)

### Technology Stack – 
    • TensorFlow
    • Hough lines
    • Microsoft Azure OCR
    • OpenCV
    • Python
    • Pandas library
    • Azure Docker
    • Flask RESTful Services
    • GitHub
    • Pillow
    • Wand
    • Azure Docker Registry
    • Azure Web Services

![Copy of TECHNOLOGY STACK (1)](https://user-images.githubusercontent.com/39915573/101400861-81c23c80-38f7-11eb-8888-c8fed1420850.png)

***Our objective was to create an algorithm which will work for two different case studies.***

***Case Study 1*** - Convert any non editable document of any format into an editable doc format which can be used for any purposes.<br>
***Case Study 2*** - Convert organisational chart into editable excel sheet with all entities and functions.

Our algorithm also detect the different types of shapes in organisational chart using TensorFlow and detec text present in it using Microsoft Azure OCR

### Approach to the Cases:

***Case 1: - File formats to Editable Format***
#### Steps followed: -
    (1) Convert the different formats (ppt, docx, pdf, jpeg, png) to jpg. 
    (2) Apply Microsoft Azure OCR to the converted jpg and extract the text.
    (3) Extracted Text is saved in the editable document ( .doc).

***Case 2: - Organizational Chart to MS-Excel***
#### Steps followed:-
    (1) Training of TensorFlow model to detect the shapes in the org chart.
    (2) Extraction of coordinates of entities.
    (3) Applying OCR on the extracted coordinates.
    (4) Saving the extracted text to excel (.xls format)
    (5) Applying delimiter to the extracted text for extraction of percentage and country/city.

### For child-parent relationship: -
Mid-point of each entity is calculated (using coordinates) and nearest neighbour is found and then the relation between the both is check using Hough lines transformation (line detection) and then the excel is updated.

Whole process is dockerized so it can easily deployable in any Operating system according to Organizations’ Requirement and on any Cloud Services like Microsoft Azure Cloud.

***Youtube Link for the Demonstration Video*** - https://youtu.be/y8ORcCOSLec

***Docker Container*** - https://hub.docker.com/r/sakshamgupta1074/trinity

***Drive Link for the models*** - https://drive.google.com/drive/folders/1KBHge89XX0oQ3nW-dNPmbl3dq1ZT26cn?usp=sharing
