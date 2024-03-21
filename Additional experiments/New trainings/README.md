These notebooks run a set of additional trainings using a 3DResnet50 architecture for the backbone.

Notebook 1 prepares .tif images in a .csv format that relates each of their names with their corresponding class.
Notebook 2 runs the training and inference, using a network defined in the github repository 
https://github.com/kenshohara/3D-ResNets-PyTorch


```bibtex
@inproceedings{hara3dcnns,
  author={Kensho Hara and Hirokatsu Kataoka and Yutaka Satoh},
  title={Can Spatiotemporal 3D CNNs Retrace the History of 2D CNNs and ImageNet?},
  booktitle={Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
  pages={6546--6555},
  year={2018},
}
```

The codes from Kensho Hara's repository have been included in this repository, in the 3D-ResNets-PyTorch folder.


Within the data/resultsResNet50 folder there are two subfolders, one of them for the pretrained version of the training and the other
one for the training from scratch. Inside each of them are the weights for the last epoch of training, together with the final results
of accuracy, precision, recall and f1 for the test set (inside the "top1.txt" file) and the logs for training and validation. The
output provided by the training pipeline saves the weights for all epochs, this is a summary.