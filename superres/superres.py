import cv2.cv2 as cv2
from cv2.cv2 import dnn_superres

# Create an SR object
sr = dnn_superres.DnnSuperResImpl_create()

# Read image
image = cv2.imread('./input.jpeg')

# Read the desired model
path = "EDSR_x3.pb"
sr.readModel(path)
# Set CUDA backend and target to enable GPU inference
sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
sr.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
# Set the desired model and scale to get correct pre- and post-processing
sr.setModel("edsr", 3)

# Upscale the image
result = sr.upsample(image)

# Save the image
cv2.imwrite("./upscaled.jpeg", result)
