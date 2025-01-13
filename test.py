import torch
print(torch.__version__)
print("cuda is available ",torch.cuda.is_available())
print("cuda version " , torch.version.cuda)
print("gpu name ", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "no gpu")


