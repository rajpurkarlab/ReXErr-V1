# ReXErr-V1

Chest X-Ray Report Errors (ReXErr-v1) Dataset -- Version 1 (v1)

Chest X-Ray Report Errors (ReXErr-v1) is a new dataset based on MIMIC-CXR and constructed using large language models (LLMs). ReXErr-v1 contains synthetic error reports for the vast majority of MIMIC-CXR (200k+ reports). We have obtained permission from PhysioNet to host it. Please do not reshare without permission.

## Error Categories

We insert errors across the following categories, designed in collaboration with clinicians and board-certified radiologists, which encompass both common human and AI-model errors.

<img width="1367" alt="Screenshot 2024-11-02 at 7 18 10 PM" src="https://github.com/user-attachments/assets/4c17023e-a44a-406f-8cc1-91f48bde3602">

## Error Injection Pipeline

The overal error injection pipeline is visualized in the figure below:

![image](https://github.com/user-attachments/assets/ac3c4fbf-4c23-43f9-9083-501a555e87d8)

As shown, we collaborated with clinicians in an iterative fashion, constructing our prompts for GPT-4o to most accurately and plausibly synthesize errors across the three separate categories sampled. After generating error reports from the MIMIC-CXR dataset, reports were then spliced into individual sentences with post-hoc error labeling performed using Llama 3.1. See the full paper [here](https://arxiv.org/abs/2409.10829) for more information regarding the error sampling strategy, sentence-splicing protocol, and particular prompts used.

## Dataset Contents

**ReXErr-report-level**
  - *ReXErr-report-level_{train/val/test}.csv* contains the original and error reports from a filtered version of the MIMIC-CXR dataset corresponding to the train, val, or test set respectively. Each row contains a unique radiology report, which corresponds to multiple images present within MIMIC-CXR. Reports are listed in ascending subject ID. Each row of the CSV corresponds to the following:
    - Dicom ID: Dicom ID(s) for the associated report
    - Study ID: Study ID taken from MIMIC-CXR
    - Subject ID: Subject ID taken from MIMIC-CXR
    - View: Views present of the images associated with the report
    - Original Report: Original report taken from MIMIC-CXR
    - Error Report: Report with errors injected using GPT-4o
    - Errors Present: Specific errors present within the report. Corresponds to the error categories mentioned above.

**ReXErr-sentence-level**
  - *ReXErr-sentence-level_{train/val/test}.csv* contains the original and error sentences based on the  ReXErr-report-level.csv file corresponding to the train, val, or test set respectively. Each row contains a sentence present within a radiology report, with spliced sentences presented in the same consecutive order that they appear within the original reports. Groups of sentences corresponding to a particular report are listed in ascending subject ID. Each row of the CSV corresponds to the following:
    - Dicom ID: Dicom ID(s) for the associated report
    - Study ID: Study ID taken from MIMIC-CXR
    - Subject ID: Subject ID taken from MIMIC-CXR
    - View: Views present of the images associated with the report
    - Index: Index of the sentence in the present row within the full error report
    - Original Sentence: Original sentence from the given MIMIC-CXR report
    - Error-Report Sentence: Sentence from the error-injected report. Note that the sentence may not necessarily contain an error, but is taken from the error-injected report.
    - Label: Label for the sentence, where 0 corresponds to unchanged sentence, 1 corresponds to error sentence, and 2 corresponds to neutral sentence (references prior)
    - Error Type: If an error is present within the Error-Report Sentence, the specific type of error it is

**Error_Analysis.ipynb** is a jupyter notebook that loads both ReXErr-report-level.csv and ReXErr-sentence-level.csv and illustrates the error distributions as well as the organization of both files.  

## File Organization

```
./
├── README.md
├── ReXErr-report-level
│   ├── ReXErr-report-level_train.csv
│   ├── ReXErr-report-level_val.csv
│   └── ReXErr-report-level_test.csv
├── ReXErr-sentence-level
│   ├── ReXErr-sentence-level_train.csv
│   ├── ReXErr-sentence-level_val.csv
│   └── ReXErr-sentence-level_test.csv
├── Error_Analysis.ipynb
```

## Citation:

Please cite the following if you use ReXErr in your work or find it useful, along with the standard citation for PhysioNet.

```
title={ReXErr: Synthesizing Clinically Meaningful Errors in Diagnostic Radiology Reports},
author={Rao, Vishwanatha M and Zhang, Serena and Acosta, Julian N and Adithan, Subathra and Rajpurkar, Pranav},
journal={arXiv preprint arXiv:2409.10829},
year={2024}
```

```
PhysioNet Citation
```

