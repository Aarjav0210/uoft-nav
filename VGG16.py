import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
import splitfolders
import matplotlib.pyplot as plt
import torch.multiprocessing as mp

mp.set_start_method("spawn", force=True)

class VGG16(object):
    def __init__(self, SEED=42):
        self.seed = SEED
        torch.manual_seed(self.seed)

    def run(self):
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

        EPOCHS = 50

        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        base_model = models.vgg16(pretrained=False)
        num_ftrs = base_model.fc.in_features

        base_model = nn.Sequential(*(list(base_model.children())[:-1]))
        base_model.to(device)

        for param in base_model.parameters():
            param.requires_grad = False

        classifier = nn.Sequential(
            nn.Linear(num_ftrs, 1024),
            nn.ReLU(),
            nn.Linear(1024, len(image_datasets["train"].classes)),
            nn.Softmax(dim=1)
        ).to(device)

        model = nn.Sequential(base_model, nn.Flatten(), classifier)
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(classifier.parameters(), lr=0.0001)

        for epoch in range(EPOCHS):
            print(f"Epoch {epoch+1}/{EPOCHS}")
            for phase in ["train", "val"]:
                if phase == "train":
                    model.train()
                else:
                    model.eval()

                running_loss = 0.0
                running_corrects = 0

                for inputs, labels in dataloaders[phase]:
                    inputs = inputs.to(device)
                    labels = labels.to(device)

                    optimizer.zero_grad()

                    with torch.set_grad_enabled(phase == "train"):
                        outputs = model(inputs)
                        _, preds = torch.max(outputs, 1)
                        loss = criterion(outputs, labels)

                        if phase == "train":
                            loss.backward()
                            optimizer.step()

                    running_loss += loss.item() * inputs.size(0)
                    running_corrects += torch.sum(preds == labels.data)

                epoch_loss = running_loss / len(image_datasets[phase])
                epoch_acc = running_corrects.double() / len(image_datasets[phase])

                print(f"{phase.capitalize()} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}")
            saved_model_folder = os.path.join(os.getcwd(), 'saved_model')
        os.makedirs(saved_model_folder, exist_ok=True)
        new_model = os.path.join(saved_model_folder, 'VGG16.pt')
        torch.save(model.state_dict(), new_model)

        test_loss = 0.0
        test_corrects = 0
        model.eval()

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
        print('\nTest accuracy:', test_acc.item())

VGGNet = VGG16()
VGGNet.run()
