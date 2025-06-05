import os

def add_suffix_to_files(root_dir, suffix="_perturbed"):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            name, ext = os.path.splitext(filename)
            new_name = f"{name}{suffix}{ext}"
            src = os.path.join(dirpath, filename)
            dst = os.path.join(dirpath, new_name)
            os.rename(src, dst)
            print(f"Renamed: {src} -> {dst}")

if __name__ == "__main__":
    root_directory = r"C:/Users/Jack/University/Compsci760/CS760-YOLO-Synth/datasets/isaac/perturb/labels/train"
    add_suffix_to_files(root_directory)
