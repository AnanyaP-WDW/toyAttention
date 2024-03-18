""" 
PyTorch implementation of Gaussian Context Transformer

As described in http://openaccess.thecvf.com//content/CVPR2021/papers/Ruan_Gaussian_Context_Transformer_CVPR_2021_paper.pdf

Gaussian Context Transformer (GCT), which achieves contextual feature excitation using
a Gaussian function that satisfies the presupposed relationship.
"""




import torch
from torch import nn

class GCT(nn.Module):
    def __init__(self, channels, c=2, eps=1e-5):
        super().__init__()

        # adaptive average pooling -> reduces the input to 1x1 dimension
        # causes mixing of info
        # input ->  N,C,Hin​,Win​ , output -> (N,C,S0,S1)(N,C,1,1​)
        self.avgpool = nn.AdaptiveAvgPool2d(1)

        # epsilon value for numerical stability
        self.eps = eps

        # constant
        self.c = c

    def forward(self, x):
        y = self.avgpool(x)
        mean = y.mean(dim=1, keepdim=True)
        mean_x2 = (y ** 2).mean(dim=1, keepdim=True)
        var = mean_x2 - mean ** 2
        
        # Normalizes y using mean and variance, with added epsilon for numerical stability.
        y_norm = (y - mean) / torch.sqrt(var + self.eps)
        y_transform = torch.exp(-(y_norm ** 2 / 2 * self.c))
        return x * y_transform.expand_as(x)
    
if __name__ == "__main__":
    x = torch.randn(2, 64, 32, 32)
    attn = GCT(64)
    y = attn(x)
    print(y.shape)
    # print(y)