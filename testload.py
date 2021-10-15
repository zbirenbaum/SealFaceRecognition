from network import Network
import tensorflow as tf

network = Network()
model = './models_for_comparison/sealnet/SealNet_Fold3/20211015-100334/graph.meta'
model = './models_for_comparison/sealnet/SealNet_Fold3/20211015-100334/'
network.load_model(model)
