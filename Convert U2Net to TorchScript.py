# This needs to be done once
import torch
from U-2-Net.model import U2NET  # Adjust the import based on the repository structure

def convert_to_torchscript():
    model = U2NET(3, 1)
    model.load_state_dict(torch.load('U-2-Net/saved_models/u2net/u2net.pth', map_location='cpu'))
    model.eval()
    traced_script_module = torch.jit.trace(model, torch.randn(1, 3, 320, 320))
    traced_script_module.save("U-2-Net/saved_models/u2net/u2net_scripted.pth")

if __name__ == "__main__":
    convert_to_torchscript()