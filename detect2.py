import os
import sys   # Suppress TensorFlow logging (1)
import pathlib
import tensorflow as tf
import time
from object_detection.utils import label_map_util
from object_detection.utils import config_util
from object_detection.utils import visualization_utils as viz_utils
from models.research.object_detection.utils import cvisualization as vis_util
from object_detection.builders import model_builder
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import warnings
import imgtoxl

def load_image_into_numpy_array(path):
    """Load an image from file into a numpy array.

    Puts image into numpy array to feed into tensorflow graph.
    Note that by convention we put it into a numpy array with shape
    (height, width, channels), where channels=3 for RGB.

    Args:
      path: the file path to the image

    Returns:
      uint8 numpy array with shape (img_height, img_width, 3)
    """
    return np.array(Image.open(path))           # Suppress TensorFlow logging (2)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 

tf.get_logger().setLevel('ERROR')

def detectshapescs2(IMAGE_PATH):
    PATH_TO_MODEL_DIR = ''

    LABEL_FILENAME = 'label_map.pbtxt'
    PATH_TO_LABELS = 'label_map.pbtxt'

    PATH_TO_CFG = PATH_TO_MODEL_DIR + "pipeline.config"
    PATH_TO_CKPT = ""
    

    print('Loading model... ', end='')
    start_time = time.time()

    # Load pipeline config and build a detection model
    configs = config_util.get_configs_from_pipeline_file(PATH_TO_CFG)
    model_config = configs['model']
    detection_model = model_builder.build(model_config=model_config, is_training=False)

    # Restore checkpoint
    ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
    ckpt.restore(os.path.join(PATH_TO_CKPT, 'ckpt-10')).expect_partial()


    end_time = time.time()
    elapsed_time = end_time - start_time
    print('Done! Took {} seconds'.format(elapsed_time))

    category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS,use_display_name=True)

    warnings.filterwarnings('ignore')   # Suppress Matplotlib warnings



    image_path =IMAGE_PATH

    print('Running inference for {}... '.format(image_path), end='')

    image_np = np.array(Image.open(image_path))
    if(len(image_np.shape)==2):
        image_np = np.stack((image_np,)*3, axis=-1)
    print(image_path)


    input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)

    image=input_tensor
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)

    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy()
                  for key, value in detections.items()}
    detections['num_detections'] = num_detections

    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

    label_id_offset = 1
    image_np_with_detections = image_np.copy()

    viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np_with_detections,
            detections['detection_boxes'],
            detections['detection_classes']+label_id_offset,
            detections['detection_scores'],
            category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=400,
            min_score_thresh=.40,
            agnostic_mode=False)

    coordinates = vis_util.return_coordinates(
                     image_np_with_detections,
                     detections['detection_boxes'],
                     detections['detection_classes']+label_id_offset,
                     detections['detection_scores'],
                     category_index,
                     use_normalized_coordinates=True,
                     line_thickness=8,
                     min_score_thresh=0.40)

    im = Image.fromarray(image_np_with_detections)
    im.save('static/images/test4.jpg')
    print("here")
    imgtoxl.ocr_excel(coordinates,IMAGE_PATH)