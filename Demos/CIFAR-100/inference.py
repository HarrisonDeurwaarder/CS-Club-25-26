import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision.transforms import ToTensor

from datasets import load_dataset
from train import CNN, ImageDataset

import PIL
from random import randint


def main() -> None:
    '''
    Main function
    '''
    # Get the device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Load the model
    model = CNN()
    model.load_state_dict(torch.load('model.pth'), map_location=device)
    
    # Create the dataset (perhaps not the most efficient use of time/memory)
    data = load_dataset('cifar100')
    dataset = ImageDataset(data)
    
    with torch.no_grad():
        img, _ = dataset[randint(0, len(dataset)-1)]
        PIL.ImageShow
    
    
if __name__ == '__main__':
    main()