E-Commerce Data Exploration Project
==============================

![alt text](notebooks/imgs/ecom_back.png "Title")

This is a project that explores the E-commerce transaction data from the [UCI repository](http://archive.ics.uci.edu/ml/datasets/Online+Retail). The analysis covered followes the standard data science pipeline from data loading, data cleaning, exploratory data analysis and modeling. All work is carried out in Jupyter notebooks with the help of several helper functions that you can find under the `src` module.

## Installation

To use this project please clone this repo in your local machine. You will then need to create the environment. You can do so in two different ways from your main project folder:

**using conda (recommended)**

```
    conda env create -f environment.yml
```

**using pip**

```
    pip install -r requirements.txt
```

Once your environment is all setup you will need to install the `src` module. To do that, activate your environment and from your project home directory execute:

```
    pip install --editable .
```

## Navigation

As discussed above, all analysis is within the `notebooks` folder. However I have also uploaded the finished notebooks on nbviewer. It is recommended that you use the links below to allow for the Plotly charts to load properly. Any work in progress is marked with (WIP)

1. [NB1 - Data Loading and Cleaning]()
2. [NB2 - Exploratory Data Analysis]()
3. [NB3 - Customer Segmentation]()
4. NB4 - Customer Attrition Prevention (WIP)
5. NB5 - Product Recommendation (WIP)



Project Organization
------------

This project is using [cookiecutter](https://github.com/cookiecutter/cookiecutter) as its folder structure. You can find more about this in [this article](https://medium.com/@rrfd/cookiecutter-data-science-organize-your-projects-atom-and-jupyter-2be7862f487e).

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
