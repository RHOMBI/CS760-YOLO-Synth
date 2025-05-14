import os
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import random

# Creating an output folder
os.makedirs('img/perturbed_img', exist_ok=True)

# Read the original annotation
def read_annotation(file_path):
    with open(file_path, 'r') as f:
        return f.read().strip()

# Save the annotation file
def save_annotation(annotation, file_path):
    with open(file_path, 'w') as f:
        f.write(annotation)

# Adding Gaussian Noise
def add_gaussian_noise(image, mean=0, std=20):
    np_img = np.array(image).astype(np.int16)
    gauss = np.random.normal(mean, std, np_img.shape)
    noisy_img = np.clip(np_img + gauss, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_img)

# Add Gaussian Blur
def add_blur(image, radius=0.5):
    return image.filter(ImageFilter.GaussianBlur(radius))

# Random colour change
def color_jitter(image, brightness=0.5, contrast=0.5, saturation=0.5):
    # Random brightness variation
    image = ImageEnhance.Brightness(image).enhance(random.uniform(1 - brightness, 1 + brightness))
    # Random contrast variation
    image = ImageEnhance.Contrast(image).enhance(random.uniform(1 - contrast, 1 + contrast))
    # Random saturation changes (need to convert to HSV and back)
    image_hsv = image.convert('HSV')
    np_img = np.array(image_hsv)
    np_img[..., 1] = np.clip(np_img[..., 1] * random.uniform(1 - saturation, 1 + saturation), 0, 255)
    image = Image.fromarray(np_img, 'HSV').convert('RGB')
    return image

# main perturbation function
def perturb_images(input_folder, output_folder):
    img_files = [f for f in os.listdir(input_folder) if f.endswith('.png')]

    for img_file in img_files:
        img_path = os.path.join(input_folder, img_file)
        ann_path = img_path.replace('.png', '.txt')

        img = Image.open(img_path).convert('RGB')
        annotation = read_annotation(ann_path)

        # Execute perturbating
        img_noisy = add_gaussian_noise(img)
        img_blur = add_blur(img_noisy)
        img_jitter = color_jitter(img_blur)

        # Save the perturbated image and original annotation (perturbation does not affect positioning)
        new_img_name = img_file.replace('.png', '_perturbed.png')
        new_ann_name = img_file.replace('.png', '_perturbed.txt')

        img_jitter.save(os.path.join(output_folder, new_img_name))
        save_annotation(annotation, os.path.join(output_folder, new_ann_name))


perturb_images('img/generate_img', 'img/perturbed_img')
