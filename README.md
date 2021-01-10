# HACKPIONS – EY GDS Hackathon
## Theme- Image to Text
## Team Name – Trinity
## Idea Name – Smart OCR for Organizational Chart

![DOCUMENT](https://user-images.githubusercontent.com/54718939/104107213-99b72280-52e0-11eb-9f8a-61eca1ca4fd7.png)

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
    • SKNW
    • Wand
    • Azure Docker Registry
    • Azure Web Services

![techstack](https://user-images.githubusercontent.com/54718939/104107221-b05d7980-52e0-11eb-87ad-178542077f93.png)

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

![Copy of Line Detection](https://user-images.githubusercontent.com/54718939/104107234-c9fec100-52e0-11eb-9eff-6351016a04b4.png)


Whole process is dockerized so it can easily deployable in any Operating system according to Organizations’ Requirement and on any Cloud Services like Microsoft Azure Cloud.

### Process Flow Diagram

![IMAGE PROCESSING](https://user-images.githubusercontent.com/54718939/101524088-7df1f100-39af-11eb-8a32-30f1a2a9bdfe.jpg)

***Youtube Link for the Demonstration Video*** - https://youtu.be/y8ORcCOSLec

***Drive Link for the models*** - https://drive.google.com/drive/folders/1t0C4ydQTBpQxl31-u61fuoJL_jvAGkv5?usp=sharing

## Steps to run the website:
    1. Source code is available in the zip file attached.
    2. Download the model from the drive link https://drive.google.com/drive/folders/1t0C4ydQTBpQxl31-u61fuoJL_jvAGkv5?usp=sharing
    3. Put all the codes and model in the same working directory.
    4. Run the following command on your terminal- pip install requirements.txt.
    5. Now run- python3 app.py.
    6. There you go, you have the website running on your local machine and can test for both the case studies.
