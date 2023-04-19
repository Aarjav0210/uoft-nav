import re 
import matplotlib.pyplot as plt

# Read data from the txt file
with open('resnet18results.txt', 'r') as f:
    content = f.read()

# Extract train and validation loss values
train_losses = re.findall(r'Train Loss: (\d+\.\d+)', content)
val_losses = re.findall(r'Val Loss: (\d+\.\d+)', content)

# Convert the loss values from strings to floats
train_losses = [float(loss) for loss in train_losses]
val_losses = [float(loss) for loss in val_losses]

# Plot the data
epochs = range(1, len(train_losses) + 1)
plt.plot(epochs, train_losses, 'r', label='Training loss')
plt.plot(epochs, val_losses, 'b', label='Validation loss')

plt.title('ResNet18: Training and Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.show()