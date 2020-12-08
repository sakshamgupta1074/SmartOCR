def ocr(image_path):
	import json
	import os
	import sys
	import requests
	import time
	# If you are using a Jupyter notebook, uncomment the following line.
	# %matplotlib inline
	import matplotlib.pyplot as plt
	from matplotlib.patches import Polygon
	from PIL import Image
	from io import BytesIO

	missing_env = False
	# Add your Computer Vision subscription key and endpoint to your environment variables.
	if 'COMPUTER_VISION_ENDPOINT' in os.environ:
	    endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
	else:
	    print("From Azure Cognitive Service, retrieve your endpoint and subscription key.")
	    print("\nSet the COMPUTER_VISION_ENDPOINT environment variable, such as \"https://westus2.api.cognitive.microsoft.com\".\n")
	    missing_env = True

	if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
	    subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
	else:
	    print("From Azure Cognitive Service, retrieve your endpoint and subscription key.")
	    print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable, such as \"1234567890abcdef1234567890abcdef\".\n")
	    missing_env = True

	if missing_env:
	    print("**Restart your shell or IDE for changes to take effect.**")
	    sys.exit()

	text_recognition_url = endpoint + "/vision/v3.1/read/analyze"

	image_data = open(image_path, "rb").read()

	headers = {'Ocp-Apim-Subscription-Key': subscription_key,'Content-Type': 'application/octet-stream'}
	response = requests.post(
	    text_recognition_url, headers=headers, data=image_data)
	response.raise_for_status()
	# Holds the URI used to retrieve the recognized text.
	operation_url = response.headers["Operation-Location"]

	# The recognized text isn't immediately available, so poll to wait for completion.
	analysis = {}
	poll = True
	while (poll):
	    response_final = requests.get(
	        response.headers["Operation-Location"], headers=headers)
	    analysis = response_final.json()

	    time.sleep(1)
	    if ("analyzeResult" in analysis):
	        poll = False
	    if ("status" in analysis and analysis['status'] == 'failed'):
	        poll = False

	open('file.doc', "w").close()
	if ("analyzeResult" in analysis):

	    polygons = ((line['text'])
	                for line in analysis["analyzeResult"]["readResults"][0]["lines"])
	    for line in polygons:
	        result = line.split("\n")
	        res= ""
	        for i in result:
	            res+=i
	        with open('file.doc', 'a') as f:
	            print(res, file=f)
	return




def alltojpg(name):
    import ntpath
    ntpath.basename("a/b/c")
    head, tail = ntpath.split(name)
    print(tail)
    print(head)
    if name.endswith('.pdf'):
        from pdf2image import convert_from_path
        pages = convert_from_path(tail, 500)
        for idx,page in enumerate(pages):
            page.save('page'+str(idx)+'.jpg', 'JPEG')
            pdfname = 'page'+str(idx)+'.jpg'
            # print(head+'/'+pdfname)
            ocr(head+'/'+pdfname)
        return pages
    elif name.endswith('.ppt'):
        print("File cannot be converted")
    elif name.endswith('.doc'):
        print("File cannot be converted")
    elif name.endswith('.png'):
        from PIL import Image
        im = Image.open(name)
        rgb_im = im.convert('RGB')
        rgb_im.save('tail.jpg')
    elif name.endswith('.jpg'):
        return 
    elif name.endswith('.jpeg'):
        return

alltojpg("/home/phantom/Downloads/EY/Sample-Image to text conversionde7492d (2)10a420a/image_extraction/Org_chart-Sample-2-input-pdf-format.pdf")



