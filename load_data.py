# -*- coding: utf-8 -*-
# @Author  : ������
# @Email   ��1017190168@qq.com

import torch
import os,glob
import visdom
import time
import torchvision
import random,csv
from torch.utils.data import Dataset,DataLoader
from torchvision import transforms
from PIL import Image

class pokemom(Dataset):
    def __init__(self,root,resize,mode,):
        super(pokemom,self).__init__()
        # �������
        self.root=root
        self.resize=resize
        # ��ÿһ������ӳ��
        self.name2label={}  # "squirtle":0 ,"pikachu":1����
        for name in sorted(os.listdir(os.path.join(root))):
            # ���˵��ļ���
            if not os.path.isdir(os.path.join(root,name)):
                continue
            # �����ڱ���;�����ӳ����Ϊ���µ�Ԫ�ص�label��ֵ
            self.name2label[name]=len(self.name2label.keys())
        print(self.name2label)
        # �����ļ�
        self.images,self.labels=self.load_csv('images.csv')
        # �ü�����
        if mode=='train':
            self.images=self.images[:int(0.6*len(self.images))]   # �����ݼ���60%����Ϊѵ�����ݼ���
            self.labels=self.labels[:int(0.6*len(self.labels))]   # label��60%�����ѵ�����ݼ���
        elif mode=='val':
            self.images = self.images[int(0.6 * len(self.images)):int(0.8 * len(self.images))]  # ��60%-80%�ĵط�
            self.labels = self.labels[int(0.6 * len(self.labels)):int(0.8 * len(self.images))]
        else:
            self.images = self.images[int(0.8 * len(self.images)):]   # ��80%�ĵط�����ĩβ
            self.labels = self.labels[int(0.8 * len(self.labels)):]
        # image+label ��·��
    def load_csv(self,filename):
        # �����е�ͼƬ���ؽ���
        # ��������ڵĻ��Ž��д���
        if not os.path.exists(os.path.join(self.root,filename)):
            images=[]
            for name in self.name2label.keys():
                images+=glob.glob(os.path.join(self.root,name,'*.png'))
                images+=glob.glob(os.path.join(self.root, name, '*.jpg'))
                images += glob.glob(os.path.join(self.root, name, '*.jpeg'))
            print(len(images),images)
            # 1167 'pokeman\\bulbasaur\\00000000.png'
            # ���ļ��������ĸ�ʽ������csv�ļ���
            random.shuffle(images)
            with open(os.path.join(self.root,filename),mode='w',newline='') as f:
                writer=csv.writer(f)
                for img in images:    #  'pokeman\\bulbasaur\\00000000.png'
                    name=img.split(os.sep)[-2]
                    label=self.name2label[name]
                    writer.writerow([img,label])
                print("write into csv into :",filename)

        # ������ڵĻ���ֱ�ӵ���������ط�
        images,labels=[],[]
        with open(os.path.join(self.root, filename)) as f:
            reader=csv.reader(f)
            for row in reader:
                # �������ͻ�õ� 'pokeman\\bulbasaur\\00000000.png' 0 �Ķ���
                img,label=row
                # ��labelת��Ϊint����
                label=int(label)
                images.append(img)
                labels.append(label)
        # ��֤images��labels�ĳ�����һ�µ�
        assert len(images)==len(labels)
        return images,labels


    # �������ݵ�����
    def __len__(self):
        return len(self.images)   # ���ص��Ǳ��ü�֮��Ĺ�ϵ

    def denormalize(self, x_hat):

        mean = [0.485, 0.456, 0.406]
        std = [0.229, 0.224, 0.225]
        mean = torch.tensor(mean).unsqueeze(1).unsqueeze(1)
        std = torch.tensor(std).unsqueeze(1).unsqueeze(1)
        # print(mean.shape, std.shape)
        x = x_hat * std + mean
        return x
    # ����idx�����ݺ͵�ǰͼƬ��label
    def __getitem__(self,idx):
        # idex-[0-�ܳ���]
        # retrun images,labels
        # ��ͼƬ��label��·��ȡ����
        # �õ���img��������һ�����ͣ�'pokeman\\bulbasaur\\00000000.png'
        # Ȼ��label�õ������� 0��1��2 ���������εĸ�ʽ
        img,label=self.images[idx],self.labels[idx]
        tf=transforms.Compose([
            lambda x:Image.open(x).convert('RGB'),  # ��tͼƬ��·��ת�����Դ���ͼƬ����
            # �������ݼ�ǿ
            transforms.Resize((int(self.resize*1.25),int(self.resize*1.25))),
            # �����ת
            transforms.RandomRotation(15),   # ������ת�Ķ���СһЩ������Ļ������������ѧϰ�Ѷ�
            # ���Ĳü�
            transforms.CenterCrop(self.resize),   # ��ʱ������ת���ֲ����ڵ���ͼƬ��ñȽϵĸ���
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485,0.456,0.406],
                                 std=[0.229,0.224,0.225])

        ])
        img=tf(img)
        label=torch.tensor(label)
        return img,label




def main():
    # ��֤����
    viz=visdom.Visdom()

    db=pokemom('pokeman',64,'train')  # ������Ըı��С 224->64,����ͨ��visdom���в鿴
    # ���ӻ�����
    x,y=next(iter(db))
    print('sample:',x.shape,y.shape,y)
    viz.image(db.denormalize(x),win='sample_x',opts=dict(title='sample_x'))
    # ����batch_size������
    loader=DataLoader(db,batch_size=32,shuffle=True,num_workers=8)
    for x,y in loader:
        viz.images(db.denormalize(x),nrow=8,win='batch',opts=dict(title='batch'))
        viz.text(str(y.numpy()),win='label',opts=dict(title='batch-y'))
        # ÿһ�μ��غ���Ϣ10s
        time.sleep(10)

if __name__ == '__main__':
    main()