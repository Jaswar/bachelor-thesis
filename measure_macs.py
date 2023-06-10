import argparse
from compute_common import load_model, construct_sample
from fvcore.nn import FlopCountAnalysis
import torch

def main(args):
    if args.seed != -1:
        torch.manual_seed(args.seed)
    model = load_model('configs/thumos_i3d_inference.yaml', 'ckpt/thumos_model.tar')
    video_list = construct_sample(args.length, 30, 4, 16)

    # The library is actually counting MACs, see: https://github.com/facebookresearch/fvcore/pull/77
    macs = FlopCountAnalysis(model, video_list)
    gmacs = macs.total() / (10 ** 9)

    with open(args.output, 'a') as f:
        f.writelines(f'{args.length},{gmacs}\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Check the number of GMACs of the ActionFormer model')
    parser.add_argument('--length', type=int, help='number of features')
    parser.add_argument('--output', type=str, help='where to save the output')
    parser.add_argument('--seed', type=int, default=-1, help='the random seed')
    args = parser.parse_args()
    main(args)