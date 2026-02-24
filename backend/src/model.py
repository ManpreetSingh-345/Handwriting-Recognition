import torch
import torch.nn as nn
import torch.nn.functional as F

#create new nueral network 
#nn.module is is pytorch nueral network we imported

class CharacterCNN(nn.Module): 
    def __init__(self):
         super(CharacterCNN, self).__init__()