# Requirements

Requirements based on [ActionFormer](https://github.com/happyharrycn/actionformer_release).

- Linux
- Python 3.5+
- PyTorch 1.11
- TensorBoard
- CUDA 11.0+
- GCC 4.9+
- NumPy 1.11+
- PyYaml
- Pandas
- h5py
- joblib
- fvcore

# Compilation

Part of NMS is implemented in C++. The code can be compiled by

```shell
cd ./libs/utils
python setup.py install --user
cd ../..
```

The code should be recompiled every time you update PyTorch.
