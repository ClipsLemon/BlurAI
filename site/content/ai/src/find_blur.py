import numpy as np
import cv2
import torch
import glob as glob

from .model import create_model
from .config import NUM_CLASSES, DEVICE, DETECTION_THRESHOLD, LAST_SAVE, DIR_IN_DETECTION, DIR_OUT_DETECTION


def blur_objects(test_images):
    model = create_model(num_classes=NUM_CLASSES).to(DEVICE)
    # last_save = glob.glob(LAST_SAVE)[0]
    last_save = "/home/clipslemon/neural_network/site/content/ai/outputs/model100.pth"

    model.load_state_dict(torch.load(
        last_save, map_location=DEVICE
    ))
    model.eval()

    for i in range(len(test_images)):
        image_name = test_images[i].split('/')[-1].split('.')[0]
        print(f"name:{image_name}")
        image = cv2.imread(test_images[i])
        orig_image = image.copy()

        image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB).astype(np.float32)
        image /= 255.0
        image = np.transpose(image, (2, 0, 1)).astype(np.float32)
        image = torch.tensor(image, dtype=torch.float).cpu()
        
        image = torch.unsqueeze(image, 0)
        with torch.no_grad():
            outputs = model(image)
        
        outputs = [{k: v.to('cpu') for k, v in t.items()} for t in outputs]

        if len(outputs[0]['boxes']) != 0:
            boxes = outputs[0]['boxes'].data.numpy()
            scores = outputs[0]['scores'].data.numpy()
            
            boxes = boxes[scores >= DETECTION_THRESHOLD].astype(np.int32)
            draw_boxes = boxes.copy()
            if len(draw_boxes > 0):
                for j, box in enumerate(draw_boxes):
                    center = (int(box[0]+(box[2]-box[0])/2),
                            int(box[1]+(box[3]-box[1])/2))
                    radius = int(((box[2]-box[0])**2+(box[3]-box[1])**2)**0.5/2)
                    # было 21 21, увеличил силу блюра 
                    blurred_img = cv2.GaussianBlur(orig_image, (51, 51), 0)

                    mask = np.zeros_like(blurred_img)
                    mask = cv2.circle(mask, center, radius, (255, 255, 255), -1)

                    out = np.where(mask==(255, 255, 255), blurred_img, orig_image)
                    orig_image = out
                
                cv2.imwrite(f"{DIR_OUT_DETECTION}/{image_name}.jpeg", out)
            else:
                cv2.imwrite(f"{DIR_OUT_DETECTION}/{image_name}.jpeg", orig_image)


if __name__=='__main__':
    test_images = glob.glob(f"{DIR_IN_DETECTION}/*")
    blur_objects(test_images)