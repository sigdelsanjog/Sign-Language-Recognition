import os

def get_image_files(data_dir, letters):
    total_images = 0
    for letter in letters:
        letter_dir = os.path.join(data_dir, letter)
        if not os.path.exists(letter_dir):
            print(f"Warning: Directory {letter_dir} does not exist. Skipping.")
            continue
        image_files = [f for f in os.listdir(letter_dir) if os.path.isfile(os.path.join(letter_dir, f))]
        total_images += len(image_files)
    return total_images

def construct_image_path(data_dir, letter, image_file):
    return os.path.join(data_dir, letter, image_file)
