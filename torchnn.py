from torch import nn ,save,load
from torch.optim import Adam
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor

#Get Data
train= datasets.MNIST(root="data",download=True, train=True, transform=ToTensor())
dataset=DataLoader(train,32)

class ImageClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.model=nn.Sequential(
           nn.Conv2d(1,32,(3,3)),
           nn.ReLU(),
           nn.Conv2d(32,64,(3,3)),
           nn.ReLU(),
           nn.Conv2d(64,64,(3,3)),
           nn.ReLU(),
           nn.Flatten(),
           nn.Linear(64*(28-6)*(28-6),10)
        )
        
    def forward(self,x):
        return self.model(x)
    
#Instance of Neural Netowrk, Classifier and Optimizer
clf =ImageClassifier()
opt= Adam(clf.parameters(), lr=1e-3)
loss_fn =nn.CrossEntropyLoss()

# Trainin Flow
if __name__ == "__main__":
    for epoch in range(10):
        for batch in dataset:
            X,y=batch
            yhat =clf(X)
            loss = loss_fn(yhat,y)
            
            #Apply Background
            opt.zero_grad()
            loss.backward()
            opt.step()
            
        print(f"Epoch:{epoch} loss is {loss .item()}")
        
        with open('model_state.pt', 'wb') as f:
            save(clf.state_dict(f))
