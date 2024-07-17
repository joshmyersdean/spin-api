# Dataset Datasheet

## Basic Information

**Dataset Title**: SPIN (SubPart ImageNet)

**Dataset Description**: 
SPIN is a hierarchical semantic segmentation dataset with subpart annotations for natural images. It provides detailed segmentations at varying levels of granularity, including objects, parts, and subparts.

**Version**: 1.0

**Date of Release**: July 12, 2024

**License**: [CC 4.0](https://creativecommons.org/licenses/by/4.0/deed.en)

**Dataset Creators**:  
- Josh Myers-Dean (University of Colorado Boulder, josh.myers-dean@colorado.edu)
- Jarek Reynolds (University of Colorado Boulder)
- Brian Price (Adobe)
- Yifei Fan (Adobe)
- Danna Gurari (University of Texas at Austin, University of Colorado Boulder)

**Dataset Maintainers**:  
- Josh Myers-Dean 

**Related Datasets**:  
- [ImageNet](http://www.image-net.org/)
- [PartImageNet](https://github.com/TACJu/PartImageNet)

---

## Dataset Composition

**What is the purpose of the dataset?**  
The purpose of the dataset is to facilitate the development of algorithms for hierarchical segmentation with subpart granularity in natural images.

**What data does the dataset contain?**  
- Number of images: 10,387
- Number of object categories: 158
- Number of part categories: 40
- Number of subpart categories: 203

**What are the primary sources of the data?**  
- Source 1: [ImageNet](http://www.image-net.org/)
- Source 2: [PartImageNet](https://github.com/TACJu/PartImageNet)

**Are there any missing or incomplete data?**  
No, the dataset provides comprehensive annotations for all included images. As with most academic datasets, some errors may exist in the annotations.

---

## Data Collection Process

**How was the data collected?**  
The data was collected by extending the PartImageNet dataset, which includes natural images with annotated objects and parts. Subpart annotations were added through a detailed annotation process involving highly trusted annotators from Amazon Mechanical Turk.

**What mechanisms or methods were used to collect the data?**  
Annotations were collected using a custom task interface that presented each image-object pair alongside its nested parts and subparts for segmentation. 

**Were any ethical guidelines followed during data collection?**  
Yes, ethical guidelines were followed, including detailed instructions for annotators and continuous inspection of submitted results. Instructions can be found [here](instructions.pdf).

---

## Data Preprocessing and Cleaning

**What preprocessing/cleaning was done?**  
Preprocessing steps included verifying the accuracy of annotations and ensuring consistent segmentation quality across the dataset. Two authors manually inspected every annotation.

**How were errors and outliers handled?**  
Errors and outliers were identified through manual inspection and corrected as necessary.

---

## Uses

**What are the intended uses of the dataset?**  
The dataset is intended for research in hierarchical segmentation, object recognition, and related tasks in computer vision.

**Who are the intended users?**  
- Researchers in computer vision
- Developers of image segmentation algorithms
- Practitioners in fields requiring detailed image analysis

**Are there any known applications or use cases?**  
Potential applications include detailed image descriptions, augmented reality experiences, visual question answering, image captioning, and visual storytelling.

---

## Distribution

**How is the dataset distributed?**  
The dataset is publicly available for download at [SPIN Dataset](https://joshmyersdean.github.io/spin/index.html).

**Are there any fees or access restrictions?**  
There are no fees or access restrictions for the dataset.

---

## Maintenance and Updates

**How will the dataset be maintained?**  
The dataset will be maintained by the creators, with updates provided as necessary.

**How can users report issues or request updates?**  
Users can report issues or request updates by contacting the dataset maintainers via email.

---

## Legal and Ethical Considerations

**Are there any known privacy or ethical issues with the dataset?**  
Humans may be present in some of the image, though we offer no annotations for humans.

**What steps were taken to mitigate these issues?**  
Annotation quality was ensured through rigorous guidelines and continuous inspection.

**Does the dataset comply with any applicable laws or regulations?**  
Yes, the dataset complies with all applicable laws and regulations.

---

## Acknowledgments

**Acknowledgments**:  
We thank the crowdworkers from Amazon Mechanical Turk for their contributions to the dataset annotations.

**Funding**:  
This work was supported by Adobe Research Gift Funds and the NSF GRFP fellowship (#1917573).

---

## Additional Information

**References**:  
- [SPIN: Hierarchical Segmentation with Subpart Granularity in Natural Images](https://arxiv.org/abs/2407.09686)

---
