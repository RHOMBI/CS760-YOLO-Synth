import torch, torchvision, torchaudio
print("Torch version:     ", torch.__version__)           # e.g. 2.7.0.dev20250309+cu128
print("Vision version:    ", torchvision.__version__)      # e.g. 0.22.0.dev20250310+cu128
print("Audio version:     ", torchaudio.__version__)        # e.g. 2.6.0.dev20250310+cu128
print("CUDA available:    ", torch.cuda.is_available())    # True
print("Device capability: ", torch.cuda.get_device_capability(0))  # (12, 0) on 5090