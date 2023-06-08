import torch
import torch.nn as nn
import torch.utils.data
import os
from libs.core import load_config
from libs.modeling import make_meta_arch


def load_model(config_path, checkpoint_path):
    cfg = load_config(config_path)

    model = make_meta_arch(cfg['model_name'], **cfg['model'])
    model = nn.DataParallel(model, device_ids=cfg['devices'])

    # print("=> loading checkpoint '{}'".format(checkpoint_path))
    # load ckpt, reset epoch / best rmse
    checkpoint = torch.load(
        checkpoint_path,
        map_location=torch.device(cfg['devices'][0])
    )
    # load ema model instead
    # print("Loading from EMA model ...")
    model.load_state_dict(checkpoint['state_dict_ema'])
    del checkpoint

    model.eval()

    return model


def construct_sample(feature_length, fps, feature_stride, num_frames, embedding_size=2048, features=None):
    # the inverse of: num_features = (fps * duration - num_frames) // feature_stride + 1
    duration = float((feature_length - 1) * feature_stride + num_frames) / fps
    if features is None:
        features = torch.rand((embedding_size, feature_length))

    video_list = [{
        'video_id': 'random',
        'feats': features,
        'fps': fps,
        'duration': duration,
        'feat_stride': feature_stride,
        'feat_num_frames': num_frames,
    }]

    return video_list

def run_command(command):
    os.system(f'conda run -n action-former {command}')

