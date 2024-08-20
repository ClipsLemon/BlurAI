import torch

BATCH_SIZE = 4
RESIZE_TO = 512
NUM_EPOCHS = 32

DEVICE = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

TRAIN_DIR = '../detection_dataset/train'
VALID_DIR = '../detection_dataset/test'

CLASSES = ['background', 'cigarette']
NUM_CLASSES = 2

VISUALIZE_TRANSFORMED_IMAGES = False

OUT_DIR = '../outputs'
SAVE_PLOTS_EPOCH = 5
SAVE_MODEL_EPOCH = 5
LAST_SAVE = "/home/clipslemon/neural_network/site/content/ai/outputs/model100.pth"

DETECTION_THRESHOLD = 0.8
DIR_IN_DETECTION = '/home/clipslemon/neural_network/in_predictions'
DIR_OUT_DETECTION = '/home/clipslemon/neural_network/out_predictions'