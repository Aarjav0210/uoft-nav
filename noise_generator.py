import os
import cv2
import numpy as np

# create a noise generator class
class NoiseGenerator(object):
    def __init__(self):
        self.img_shape = (640, 640, 3)
        self.noise_low = np.random.normal(0, 25, self.img_shape)
        self.noise_high = np.random.normal(0, 50, self.img_shape)
    
    def _get_image(self, img_path):
        img = cv2.imread(img_path)
        return img

    def generate_noise(self, img_path, noise_type):
        img = self._get_image(img_path)
        if noise_type == 'low':
            noise = self.noise_low
        elif noise_type == 'high':
            noise = self.noise_high
        else:
            raise ValueError('Noise type must be either "low" or "high"')
        noisy_img = cv2.add(img, noise, dtype=cv2.CV_8U)
        return noisy_img
    
    def show_noise(self, img_path, noise_type):
        noisy_img = self.generate_noise(img_path, noise_type)
        cv2.imshow(f"Noisy {noise_type}", noisy_img)
        cv2.waitKey(0)

# ng = NoiseGenerator()
# img_dir = os.path.join(os.getcwd(), 'images')
# img_files = os.listdir(img_dir)
# img_list = [img for img in img_files if img.endswith(".jpg")]
# img_path = os.path.join(img_dir, img_list[0])
# ng.show_noise(img_path, 'low')
# ng.show_noise(img_path, 'high')