# SealNet

Harbor Seals Face Recognition project

## Prerequisites

This project uses [Tensorflow](https://www.tensorflow.org/).

## Installation

1. Clone the repo

  ```sh
  git clone https://github.com/aylab/SealFaceRecognition.git
  ```

2. Create a [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) virtual environment and activate it.

  ```sh
  conda create --name myenv python=3.7 pip
  conda activate myenv
  ```

3. Install dependencies using pip

  ```sh
  pip install -r requirements.txt
  ```

<!-- USAGE EXAMPLES -->
## Usage

For training on seal face images:

```sh
python train.py -c config.py -d /path/to/photos
```
<!-- CONFIG EXAMPLE -->
## Configuration

The `config.py` file contains all the configurations required for training. The root directory should contain subdirectories of seal individuals.

<!-- CONTRIBUTING -->
## Contributing

Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- CONTACT -->
## Contact

Ahmet Ay - Colgate University
