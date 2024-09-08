# Data Pipeline Design

## Problem Description

The task at hand is to develop a robust data pipeline for handling and preparing a dataset containing customer, transaction, and fraud information for machine learning purposes. This dataset needs to be transformed from its raw form into structured data suitable for general machine learning, including fraud detection. Additionally, we must partition the dataset into training and testing datasets and extract relevant features for model development.

## Proposed Design

The data pipeline is structured into three Python modules, each with a specific responsibility:

1. **Raw_Data_Handler**: This module extracts raw data from multiple sources (CSV, Parquet, JSON), merges the data, and applies transformations to clean and standardize it.
   
2. **Dataset_Designer**: This module partitions the cleaned dataset into training and testing datasets, ensuring proper splits and data integrity.
   
3. **Feature_Extractor**: This module extracts and formats relevant features from the partitioned data to prepare it for machine learning model development.

Each module contains methods for extracting, transforming, describing, and saving the dataset, ensuring that it is usable for a variety of machine learning applications.

## Design Argument

The design addresses the following requirements:

1. **Raw Data Handling**: The `Raw_Data_Handler` class extracts and processes raw data from different formats (CSV, Parquet, JSON). This design accommodates the variety of file types and ensures that all data is loaded into a consistent structure for merging and further processing. The transformation process includes general data cleaning (e.g., handling missing values), which is essential for machine learning readiness.
   
2. **Dataset Partitioning**: The `Dataset_Designer` class partitions the dataset into training and testing sets. By using an 80/20 split, the design ensures that the data is properly segmented for machine learning, providing enough data for both model training and evaluation. The class can handle multiple partitions if required in future applications.

3. **Feature Extraction**: The `Feature_Extractor` class is designed to convert raw, cleaned data into feature sets that can be used for machine learning models. The features are not limited to the fraud detection problem but are generalized to handle a variety of machine learning tasks. This allows the pipeline to be reused in different applications.

4. **Data Integrity and Versioning**: Each class includes a `describe()` method that outputs key metrics about the dataset (e.g., column names, number of records). This functionality ensures data integrity and enables version tracking across multiple stages of the pipeline. The `load()` method in each class saves the data in a standardized format (Parquet), ensuring compatibility and efficient storage.

## Testing and Evaluation of Hypotheses

The proposed design hypothesizes that separating the extraction, transformation, partitioning, and feature extraction processes into distinct modules ensures a scalable and reusable pipeline. We evaluate this hypothesis by testing the following:

1. **Modularity**: Each module is designed to handle a distinct aspect of the data pipeline. By ensuring that the modules operate independently, we hypothesize that the pipeline can be extended or modified easily. We will evaluate this by testing each module in isolation (e.g., running the `Raw_Data_Handler` independently of the `Dataset_Designer`).

2. **Generalization**: The hypothesis is that the pipeline is applicable beyond just the fraud detection problem. To evaluate this, we will run the pipeline on multiple datasets (e.g., classification or regression problems) and verify that the data transformation and feature extraction are still valid.

3. **Data Integrity**: The hypothesis is that data integrity is maintained throughout the pipeline. To evaluate this, we will inspect the `describe()` outputs after each transformation and partitioning step to ensure no data is lost, and that all relevant columns are retained.

4. **Efficiency**: The pipeline uses Parquet files for storage, which are efficient in terms of size and speed. We hypothesize that the use of Parquet files improves storage efficiency without loss of data fidelity. We will evaluate this by comparing the storage sizes of different file formats and ensuring that data can be quickly reloaded for analysis.
