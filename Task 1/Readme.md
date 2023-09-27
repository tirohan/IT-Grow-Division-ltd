# MNIST Image Classification

## Introduction

This repository contains code and documentation for an image classification project using the MNIST dataset. The project involves the development of a custom Convolutional Neural Network (CNN) model to classify handwritten digits (0-9) in grayscale images.

## Project Highlights

- **Custom CNN Model**: A custom CNN architecture is designed and implemented using Keras. The model is optimized for accuracy and tailored to the MNIST dataset.

- **Data Preprocessing**: Input image data is preprocessed, including normalization and optional anomaly detection and dimensionality reduction techniques.

- **Exploratory Data Analysis (EDA)**: Data insights are visualized to understand the distribution of target labels.

- **Optional Anomaly Detection**: PyCaret is used for anomaly detection with Principal Component Analysis (PCA).

- **Optional Dimensionality Reduction**: PCA is employed for dimensionality reduction.

- **Optional 3D Visualization**: The reduced-dimensional data is visualized in 3D using UMAP.

- **Model Training**: The custom CNN model is trained with early stopping to prevent overfitting.

- **Model Evaluation**: The trained model is evaluated using various classification metrics, and loss and accuracy curves are visualized.

- **Detailed Documentation**: A comprehensive documentation file explains the project process and the rationale for using a custom CNN model.

## Prerequisites

Before running the code, make sure you have the following prerequisites installed:

- Python 3.x
- TensorFlow
- Keras
- PyCaret (for optional anomaly detection)
- NumPy
- Pandas
- Matplotlib
- Seaborn
- Plotly
- Scikit-learn

You can install the required Python packages using `pip`:

`pip install -r requirements.txt`
## Usage

1. Clone this repository:
`git clone https://github.com/your-username/mnist-image-classification.git`
2. Navigate to the project directory:
`cd mnist-image-classification`
3. Execute the Jupyter Notebook or Python scripts for the specific tasks you want to run:

   - `MNIST_Task1.ipynb`: Jupyter Notebook for the entire project, including data preprocessing, model training, and evaluation.

   - Other scripts: Individual Python scripts for specific tasks (e.g., anomaly detection, 3D visualization).

4. Follow the documentation for detailed instructions on running and understanding the project.
