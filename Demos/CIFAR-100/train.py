import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision.transforms import ToTensor

from datasets import load_dataset


class CNN(nn.Module):
    '''
    Convolutional neural network for PyTorch demo
    '''
    def __init__(self,) -> None:
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, padding=1),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(in_channels=16, out_channels=64, kernel_size=3, padding=1),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        self.seq = nn.Sequential(
            nn.Linear(4096, 1028),
            nn.ReLU(),
            nn.Linear(1028, 512),
            nn.ReLU(),
            nn.Linear(512, 100),
        )
        
    def forward(self,
                image: torch.Tensor) -> torch.Tensor:
        '''
        Pass an image through the CNN
        '''
        out: torch.Tensor = self.conv(image)
        out = out.flatten(1)
        return self.seq(out)
        

class ImageDataset(Dataset):
    '''
    Dataset to handle images
    '''
    def __init__(self,
                 data,) -> None:
        self.data = data
        self.transform = ToTensor()
        
    def __len__(self,) -> int:
        return len(self.data)
    
    def __getitem__(self, 
                    idx: int,):
        sample = self.data[idx]
        img, label = sample['img'], sample['fine_label']
        return (
            self.transform(img),
            label,
        )
        

model: CNN = CNN()
optimizer: optim.Adam = optim.Adam(model.parameters())
criterion: nn.CrossEntropyLoss = nn.CrossEntropyLoss()

# Data preparation
data = load_dataset('cifar100') # DatasetDict with 'train' (50k) and 'test' (10k)
dataset = ImageDataset(data['train'])
dataloader = DataLoader(dataset, batch_size=64, shuffle=True)

# Info about dataset/training
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(
    f'\nSample: {data["train"][0]}',
    f'Classes: {len(set(data["train"]["fine_label"]))}',
    f'Device: {device}',
    sep='\n'
)

model.to(device)
# Training loop
for epoch in range(16):
    for img, label in dataloader:
        # Forward pass
        logits = model(img.to(device))
        # Backward pass
        optimizer.zero_grad()
        loss = criterion(logits, label.to(device))
        loss.backward()
        optimizer.step()
    print(f'Epoch #{epoch+1} done!')