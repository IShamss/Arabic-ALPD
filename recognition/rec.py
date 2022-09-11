# Recognition class which responsible for prediction of car plates by training models
import torch
import cv2 as cv
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image


class Recognition:
    def __init__(self,model_name='resnet_model'):
        self.use_cuda = torch.cuda.is_available()
        if model_name == 'resnet_model':
            resnet_model = models.resnext50_32x4d(pretrained=True)
            resnet_model.fc = torch.nn.Linear(resnet_model.fc.in_features,38)
            if(self.use_cuda):
                resnet_model.load_state_dict(torch.load('./resnet_model.pt'))
            else:    
                resnet_model.load_state_dict(torch.load('./resnet_model.pt',map_location=torch.device('cpu')))
            resnet_model.eval()
            self.model = resnet_model
        elif model_name == 'vgg_model':
            vgg_model = models.vgg19_bn(pretrained=True)
            vgg_model.classifier[6] = torch.nn.Linear(vgg_model.classifier[6].in_features,38)
            if(self.use_cuda):
                vgg_model.load_state_dict(torch.load('./recognition/vgg_model.pt'))
            else:
                vgg_model.load_state_dict(torch.load('./recognition/vgg_model.pt',map_location=torch.device('cpu')))
            vgg_model.eval()
            self.model = vgg_model
        
        print(f"Using {model_name} Model")

    
    def predict_characters(self,images):
        mappings = {
        "ا": 0,
        "ب": 1,
        "ت": 2,
        "ث": 3,
        "ج": 4,
        "ح": 5,
        "خ": 6,
        "د": 7,
        "ذ": 8,
        "ر": 9,
        "ز": 10,
        "س": 11,
        "ش": 12,
        "ص": 13,
        "ض": 14,
        "ط": 15,
        "ظ": 16,
        "ع": 17,
        "غ": 18,
        "ف": 19,
        "ق": 20,
        "ك": 21,
        "ل": 22,
        "م": 23,
        "ن": 24,
        "ه": 25,
        "و": 26,
        "ى": 27,
        "0": 28,
        "1": 29,
        "2": 30,
        "3": 31,
        "4": 32,
        "5": 33,
        "6": 34,
        "7": 35,
        "8": 36,
        "9": 37,
        }
        result=[]
        in_transform=transforms.Compose([transforms.Resize(255),
                                    transforms.CenterCrop(224),
                                    transforms.ToTensor(),
                                    transforms.Normalize([0.5],[0.5])])
        character_classes = list(range(0,38))
        character_classes = list(map(str,character_classes))
        character_classes.sort()
        for image in images:
            image = in_transform(image)[:3,:,:].unsqueeze(0).float()
            if self.use_cuda:
                self.model.cuda()
                image.cuda()
            output = self.model(image)
            values , indices = torch.topk(output,1)
            key_list = list(mappings.keys())
            val_list = list(mappings.values())
            for i in indices[0]:
                pred_class = int(character_classes[i])
                result.append(key_list[val_list.index(pred_class)])
        plate_number = ' '.join(result)
        print(plate_number)
        return plate_number
        
    
    def test_data(self,img_paths):     
        # given a list of cropped images paths, open images and send the list of images
        # to predict characters
        images=[]
        for img_path in img_paths:
            current_img = cv.imread(img_path)
            image = Image.fromarray(current_img)
            images.append(image)
        self.predict_characters(images)

# if __name__=="__main__":
#     print("Running")
#     rec = Recognition('vgg_model')
#     rec.test_data(['./data/15/177.jpg','./data/2/45.jpg','./data/19/21.jpg','./data/31/23.jpg','./data/36/106.jpg','./data/35/7014.jpg'])