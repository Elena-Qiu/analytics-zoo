# Pytorch Sentiment example

We demonstrate how to easily show the graphical results of running synchronous distributed PyTorch training using PyTorch Estimator of Project Orca in Analytics Zoo. We use the LSTMClassifier to train on IMDB dataset. See [here](https://github.com/prakashpandey9/Text-Classification-Pytorch) for the original single-node version of this example. We provide the "torch_distributed" PyTorch training backend for this example.

# Prepare the environment

We recommend you to use Anaconda to prepare the environment, especially if you want to run on a yarn cluster:

```
conda create -n zoo python=3.7  # "zoo" is conda environment name, you can use any name you like.
conda activate zoo
pip install torch
pip install torchtext

pip install analytics-zoo[ray]  # 0.10.0.dev3 or above
```

# Run on local after pip install

You can run as follows:

```
python main.py
```

# Run on yarn cluster for yarn-client mode after pip install

```
export HADOOP_CONF_DIR=the directory of the hadoop and yarn configurations
python main.py --cluster_mode yarn
```

# Results

You can find the results of training and validation as follows:

```
num_samples : 24992
Accuracy : tensor(0.5851)
val_loss : 0.6760138604460849
Stopping orca context
```

