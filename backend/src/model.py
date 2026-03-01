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

         self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1) #layer 1

         # expands pattern search 

         self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1) #layer 2

         #splits into 2x2 matrix and takes highest value 
         #then puts together the highest values in a 4x4 matrix 
         #by doing this it throws away irrelavent data and figures out the pattern

         self.pool = nn.MaxPool2d(2, 2)

         #this takes all fetaure maps that we made 64 and connc=ect them
         #all maps are in a 7x7 matrix
         #then takes highest value maps and uses that to figure the 128 most important pixels

         self.fc1 = nn.Linear(64 * 7 * 7, 128)
         self.fc2 = nn.Linear(128, 47) #takes and figures out the 47 diffrent possible outcomes 

    def forward(self,x): #next steps gets pushed here
        x = self.pool(F.relu(self.conv1(x))) #takes patterns turns to numbers then gets rid of unused number and shrinks image using layer 1(conv.1)
        x = self.pool(F.relu(self.conv2(x))) #same thing with layer 2

        x = x.view(x.size(0), -1) #weighthed calculations by making flat
        x = F.relu(self.fc1(x)) #get rid of extra and commits to 128 
        x = self.fc2(x) #decides what character it is
        return x
    
        #x = self.pool(F.relu(self.conv3(x))) #same thing with layer 3 this at bottom next to other pool area
        #self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1) #layer 3 this should be at top area (Experiment with conv 3 and pooling to see if it improves accuracy, but be mindful of overfitting)
