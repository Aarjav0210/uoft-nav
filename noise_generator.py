import os
import cv2
import numpy as np

# create a noise generator class
class NoiseGenerator(object):
    def __init__(self):
        self.img_shape = (224, 224, 3)
        self.noise_low = np.random.normal(0, 25, self.img_shape)
        self.noise_high = np.random.normal(0, 50, self.img_shape)
    
    def _get_image(self, img_path):
        img = cv2.imread(img_path)
        return img

    def generate_noise(self, image_content, noise_type):
        img = cv2.imdecode(np.frombuffer(image_content, np.uint8), cv2.IMREAD_COLOR)
        if noise_type == 'low':
            noise = self.noise_low
        elif noise_type == 'high':
            noise = self.noise_high
        else:
            raise ValueError('Noise type must be either "low" or "high"')
        noisy_img = cv2.add(img, noise, dtype=cv2.CV_8U)

        # Encode the noisy image as a PNG file in memory
        _, buffer = cv2.imencode('.png', noisy_img)

        # Convert the image buffer to a binary string
        image_content = buffer.tobytes()

        return image_content

    
    def show_noise(self, img_path, noise_type):
        noisy_img = self.generate_noise(img_path, noise_type)
        cv2.imshow(f"Noisy {noise_type}", noisy_img)
        cv2.waitKey(0)