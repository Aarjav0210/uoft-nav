import re 
import matplotlib.pyplot as plt

# Read data from the txt file
with open('loss-data/resnet18results.txt', 'r') as f:
    content_18 = f.read()

with open('loss-data/resnet34 loss.txt', 'r') as f:
    content_34 = f.read()

with open('loss-data/VGG16 loss.txt', 'r') as f:
    content_16 = f.read()

# Extract train and validation loss values
train_losses_18 = re.findall(r'Train Loss: (\d+\.\d+)', content_18)
train_losses_34 = re.findall(r'\[\d+\] loss: (\d+\.\d+)', content_34)
train_losses_16 = re.findall(r'\[\d+\] loss: (\d+\.\d+)', content_16)

# Convert the loss values from strings to floats
train_losses_18 = [float(loss) for loss in train_losses_18]
train_losses_34 = [float(loss) for loss in train_losses_34]
train_losses_16 = [float(loss) for loss in train_losses_16]

# Plot the data
# Create separate epochs lists for each ResNet model
epochs_18 = range(1, len(train_losses_18) + 1)
epochs_34 = range(1, len(train_losses_34) + 1)
epochs_16 = range(1, len(train_losses_16) + 1)

# Plot the data
plt.plot(epochs_18, train_losses_18, 'r', label='ResNet18')
plt.plot(epochs_34, train_losses_34, 'b', label='ResNet34')
plt.plot(epochs_16, train_losses_16, 'g', label='VGG16')
plt.title('Training Loss Comparison')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.show()