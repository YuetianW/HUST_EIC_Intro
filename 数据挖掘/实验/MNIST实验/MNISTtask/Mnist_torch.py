import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets,transforms
import torch.utils.data as Data

class Net(nn.Module):
    def __init__(self):
        super(Net,self).__init__()
        self.conv1 = nn.Conv2d(1,32,3,1,1)
        self.conv2 = nn.Conv2d(32,64,3,1,1)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.25)
        self.fc1 = nn.Linear(14*14*64,128)
        self.fc2 = nn.Linear(128,10)

    def forward(self,x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x,2)
        x = self.dropout1(x)

        x = torch.flatten(x,1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        #直接输出的话用F.cross_entropy()
        output = F.log_softmax(x,dim=1)
        #套用log_softmax()输出后用nll_loss()
        return output,x

def train(model,device,train_loader,optimizer,epochs):
    model.train()
    for batch_idx,(data,target) in enumerate(train_loader):
        data,target = data.to(device),target.to(device)
        optimizer.zero_grad()
        output,x= model(data)
        loss = F.cross_entropy(x,target)
        #loss = F.nll_loss(output,target)
        loss.backward()
        optimizer.step()

        if batch_idx%10 ==0:
            print('train epochs:{} [{}/{} ({:.0f}%)]\t Loss: {:.6f}'.format(
                epochs,batch_idx*len(data),len(train_loader.dataset),
                100.*batch_idx/len(train_loader),loss.item()
            ))

def test(model,device,test_loader):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data,target in test_loader:
            data,target = data.to(device),target.to(device)
            output,x= model(data)
            test_loss += F.cross_entropy(x,target,reduction='sum').item()
            #test_loss += F.nll_loss(output,target,reduction='sum').item()
            pred = output.argmax(dim = 1,keepdim = True)
            correct += pred.eq(target.view_as(pred)).sum().item()
    test_loss /= len(test_loader.dataset)

    print('\nTest set: Average loss: {:.6f}, Accuracy: {}/{} ({:.3f}%)\n'.format(
        test_loss,correct,len(test_loader.dataset),
        100.*correct/len(test_loader.dataset)))

def main():
    device = torch.device('cuda')

    transform = transforms.ToTensor()

    datasets1 = datasets.MNIST('../data',train = True,download=True,transform=transform)
    datasets2 = datasets.MNIST('../data',train = False,transform=transform)

    train_kws = {'batch_size':64,'num_workers':4,'pin_memory':True,'shuffle':True}
    test_kws = {'batch_size':1000,'num_workers':2,'pin_memory':True,'shuffle':True}

    train_loader = Data.DataLoader(datasets1,**train_kws)
    test_loader = Data.DataLoader(datasets2,**test_kws)

    model = Net().to(device)
    optimizer = optim.Adam(model.parameters(),lr = 0.001)
    for epoch in range(10):
        train(model,device,train_loader,optimizer,epoch)
        test(model,device,test_loader)

    torch.save(model,'net1.pt')

if __name__ == '__main__':
    main()
