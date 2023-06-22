
For inference time experiments, please put the model trained on 
the THUMOS'14 dataset here with the name `thumos_model.tar`.

To obtain this trained model, one can run:
```shell
python ./train.py ./configs/thumos_i3d.yaml --output reproduce
cd ckpt
mv thumos_i3d_reproduce/epoch_035.pth.tar ./thumos_model.tar
```

