import torch

if __name__ == '__main__':
    torch.manual_seed(0)
    print(torch.randint(0, 10**9, (5, )))