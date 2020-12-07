# HACKPIONS – EY GDS Hackathon
## Theme- Image to Text
## Team Name – Trinity
## Idea Name – Smart OCR for Organizational Chart
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

![image](https://user-images.githubusercontent.com/39915573/101396827-e11d4e00-38f1-11eb-8d40-4e9158a40807.png)

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

***Drive Link for the models*** - https://drive.google.com/drive/folders/1KBHge89XX0oQ3nW-dNPmbl3dq1ZT26cn?usp=sharing


