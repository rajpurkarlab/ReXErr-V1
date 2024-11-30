# ReXErr-V1: Clinically Meaningful Chest X-Ray Report Errors Derived from MIMIC-CXR


Chest X-Ray Report Errors (ReXErr-v1) Dataset -- Version 1 (v1)

Chest X-Ray Report Errors (ReXErr-v1) is a new dataset based on MIMIC-CXR and constructed using large language models (LLMs). ReXErr-v1 contains synthetic error reports for the vast majority of MIMIC-CXR (200k+ reports). Please access the dataset through PhysioNet here. This repository contains the code and the prompts used to develop ReXErr-v1.

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
    - dicom_id: Dicom ID(s) for the associated report
    - study_id: Study ID taken from MIMIC-CXR
    - subject_id: Subject ID taken from MIMIC-CXR
    - original_report: Original report taken from MIMIC-CXR
    - error_report: Report with errors injected using GPT-4o
    - errors_sampled: Errors that were sampled to create the error report. Note that the error report may not contain all of the errors sampled, and for more accurate labeling, see the sentence level labeling.

**ReXErr-sentence-level**
  - *ReXErr-sentence-level_{train/val/test}.csv* contains the original and error sentences based on the  ReXErr-report-level.csv file corresponding to the train, val, or test set respectively. Each row contains a sentence present within a radiology report, with spliced sentences presented in the same consecutive order that they appear within the original reports. Groups of sentences corresponding to a particular report are listed in ascending subject ID. Each row of the CSV corresponds to the following:
    - dicom_id: Dicom ID(s) for the associated report
    - study_id: Study ID taken from MIMIC-CXR
    - subject_id: Subject ID taken from MIMIC-CXR
    - original_sentence: Original sentence from the given MIMIC-CXR report
    - error_sentence: Sentence from the error-injected report. Note that the sentence itself may not necessarily contain an error, but it originates from the error-injected report
    - error_present: Indicator for whether an error is present in the sentence, where 0 corresponds to unchanged sentence, 1 corresponds to error sentence, and 2 corresponds to neutral sentence (references a prior or does not contain any clinically relevant indications/findings)
    - error_type: If an error is present within the error_sentence, the specific type of error it is

## Code Provided

We provide the code used to both generate the dataset using GPT-4o and sentence-by-sentence splice and label each report. We include an option for labeling the spliced reports using either Llama 3.1 (more accurate) or regex. We include the full code as well as the particular prompts used, and demonstrate how the error-specific prompts are combined together to generate errors together.

### File Organization

```
./
├── ReXErr-report-level
│   ├── ReXErr-report-level-generation.py
│   ├── ReXErr-report-level-errror_prompts.json
├── ReXErr-sentence-level
│   ├── ReXErr-sentence-level-splicing.py
│   ├── ReXErr-sentence-level-label-regex.py
│   ├── ReXErr-sentence-level-label-llama.py
│   ├── utils.py
├── README.md
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

