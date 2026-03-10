import torch
import torch.nn as nn
import torch.nn.functional as F

#create new nueral network 
#nn.module is is pytorch nueral network we imported

class CharacterCNN(nn.Module): 
    
    #constuctor

    def __init__(self): 
    
    #access parent class 

         super(CharacterCNN, self).__init__()

         # vision layers looks at 3x3 images across the whole thing and figures out patterns has 32 pattern
         # has 32 pattern detectors

         self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1, bias=False) #layer 1, bias=False since BN follows
         self.bn1 = nn.BatchNorm2d(32) #makes the output of conv1 more consistent
         # expands pattern search 

         self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1, bias=False) #layer 2, bias=False since BN follows
         self.bn2 = nn.BatchNorm2d(64) #makes the output of conv2 more consistent
         
         self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1, bias=False) #layer 3, bias=False since BN follows
         self.bn3 = nn.BatchNorm2d(128) #makes the output of conv3 more consistent

         #splits into 2x2 matrix and takes highest value 
         #then puts together the highest values in a 4x4 matrix 
         #by doing this it throws away irrelavent data and figures out the pattern

         self.pool = nn.MaxPool2d(2, 2)

         #this takes all fetaure maps that we made 64 and connc=ect them
         #all maps are in a 7x7 matrix
         #then takes highest value maps and uses that to figure the 128 most important pixels

         self.global_pool = nn.AdaptiveAvgPool2d((1,1))
         self.fc1 = nn.Linear(128, 256) #Increased to 256 so the model has more space to learn before deciding
         self.dropout = nn.Dropout(0.5) # prevents overfitting which makes it learn rather than memorize 
         self.fc2 = nn.Linear(256, 128) #added second FC layer, gradually narrows (middle man) to help model learn better representations before final decision
         self.dropout2 = nn.Dropout(0.3) #light dropout to prevent overfitting in the second FC layer
         self.fc3 = nn.Linear(128, 47) #takes and figures out the 47 diffrent possible outcomes

    def forward(self,x): #next steps gets pushed here
        x = (F.relu(self.bn1(self.conv1(x))))#takes patterns turns to numbers then gets rid of unused number and shrinks image using layer 1(conv.1)
        x=self.pool(x)
        x = (F.relu(self.bn2(self.conv2(x)))) #same thing with layer 2
        x= self.pool(x)

        x = (F.relu(self.bn3(self.conv3(x)),)) #same thing with layer 3
        x= self.pool(x)
        x = self.global_pool(x) 

        x = torch.flatten(x, 1) #weighthed calculations by making flat
        x = F.relu(self.fc1(x), inplace=True) #relu is activation function that adds nonlinearity, inplace=True saves memory by doing it in place
        x=self.dropout(x)
        x = F.relu(self.fc2(x), inplace=True) #get rid of extra and commits to 128 
        x=self.dropout2(x) #prevents overfitting by randomly dropping nuerons
        x = self.fc3(x) #decides what character it is
        return x
       
       
