# SPIN API
![A line of photos representing samples from our dataset with subpart decompositions.](static/spin_teaser.jpg)
A Python package for interacting with the [SPIN dataset](https://arxiv.org/abs/2407.09686v1), visualizing annotations, and rasterizing segmentations.

This repository supplements the paper "SPIN: Hierarchical Segmentation with Subpart Granularity in Natural Images".

## Installation

To install the package, you can use pip:

```bash
pip install spin-api
```

We provide an example of how to use the SPIN API in `demo.ipynb`. Of note, we offer functions for downloading the annotations and provide them in a nice COCO format, or allow for rasterization if desired.

## Documentation
API documentation can be found at [this webpage](https://joshmyersdean.github.io/spin-api/).

## Images
Obtain the images from the Segmentation split of [PartImageNet](https://github.com/TACJu/PartImageNet).

## Data Documentation
To view the annotator instructions and other dataset-specific information including a data sheet, please refer to the [data_spec](data_spec/) directory.

## Issues
If you find an issue with the API or dataset, please feel free to make a pull request or an issue. Also feel free to reach out directly at josh.myers-dean@colorado.edu

## Citation
If you find our work useful, please consider citing!

```pre
@InProceedings{Myers-Dean_2024_ECCV,
	author    = {Myers-Dean, Josh and Reynolds, Jarek and Price, Brian and Fan, Yifei and Gurari, Danna},
	title     = {SPIN: Hierarchical Segmentation with Subpart Granularity in Natural Images},
	booktitle = {European Conference on Computer Vision},
	year      = {2024},
} 
```