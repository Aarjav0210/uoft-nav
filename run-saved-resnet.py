import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
import matplotlib.pyplot as plt
import torch.multiprocessing as mp



def load_saved_model(model_path, num_classes):
    # Create the same resnet model architecture
    base_model = models.resnet18(pretrained=False)
    num_ftrs = base_model.fc.in_features

    classifier = nn.Sequential(
        nn.Linear(num_ftrs, 1024),
        nn.ReLU(),
        nn.Linear(1024, num_classes),
        nn.Softmax(dim=1)
    )

    model = nn.Sequential(*(list(base_model.children())[:-1]))

    # Load the saved model state_dict
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))

    return model

def test_saved_model(model, dataloaders, device):
    criterion = nn.CrossEntropyLoss()
    test_loss = 0.0
    test_corrects = 0
    model.eval()
    model.to(device)

    for inputs, labels in dataloaders["test"]:
        inputs = inputs.to(device)
        labels = labels.to(device)

        with torch.no_grad():
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            loss = criterion(outputs, labels)

        test_loss += loss.item() * inputs.size(0)
        test_corrects += torch.sum(preds == labels.data)

    test_loss = test_loss / len(image_datasets["test"])
    test_acc = test_corrects.double() / len(image_datasets["test"])
    print('Test accuracy:', test_acc.item())

TRAIN_R = 0.6  # Train ratio
VAL_R = 0.2
TEST_R = 0.2

IMG_HEIGHT, IMG_WIDTH = (224, 224)
BATCH_SIZE = 16

DATA_DIR_PATH = "images"
OUTPUT_DIR = "split_images"

        #splitfolders.ratio(DATA_DIR_PATH, OUTPUT_DIR, seed=self.seed, ratio=(TRAIN_R, VAL_R, TEST_R))

train_data_dir = f"{OUTPUT_DIR}/train"
valid_data_dir = f"{OUTPUT_DIR}/val"
test_data_dir = f"{OUTPUT_DIR}/test"
data_transforms = {
    "train": transforms.Compose([
        transforms.Resize((IMG_HEIGHT, IMG_WIDTH)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.RandomAffine(degrees=0, shear=0.2, scale=(0.8, 1.2)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
    "val": transforms.Compose([
        transforms.Resize((IMG_HEIGHT, IMG_WIDTH)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
    "test": transforms.Compose([
        transforms.Resize((IMG_HEIGHT, IMG_WIDTH)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
}

image_datasets = {
            x: datasets.ImageFolder(os.path.join(OUTPUT_DIR, x), data_transforms[x])
            for x in ["train", "val", "test"]
        }

dataloaders = {
            x: DataLoader(image_datasets[x], batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
            for x in ["train", "val", "test"]
        }


# Load the saved model
num_classes = len(image_datasets["train"])
saved_model_path = "saved_model/resnet.pt"
loaded_model = load_saved_model(saved_model_path, num_classes)

# Test the loaded model
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
test_saved_model(loaded_model, dataloaders, device)