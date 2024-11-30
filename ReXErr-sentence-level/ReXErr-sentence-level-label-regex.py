
import re
from utils import devices_pattern, location_pattern, severity_pattern, false_negation, prior_pattern, measurement_pattern, get_nouns, find_homophones_and_typos

def label_errors(original_sentence, error_sentence, original_report, error_report):
    def get_label(has_prior, is_match=False):
        if is_match and not has_prior:
            return 0
        return 2 if has_prior else 1
    
    label_list, error_list = [], []
    for orig_sentence, err_sentence in zip(original_sentence, error_sentence):
        # Check for prior words in either sentence
        has_prior = (re.search(prior_pattern, orig_sentence, re.IGNORECASE) if orig_sentence else False) or \
                    (re.search(prior_pattern, err_sentence, re.IGNORECASE) if err_sentence else False)
        
        # Handle empty original sentence cases
        if orig_sentence == '':
            if err_sentence.strip().replace('\n', ' ') in original_report.strip().replace('\n', ' '):
                error_type = "Add repetition"
            elif re.search(devices_pattern, err_sentence, re.IGNORECASE):
                error_type = "Add medical device"
            else:
                error_type = "False prediction"
            label = get_label(has_prior)
            
        # Handle empty error sentence
        elif err_sentence == '':
            error_type = "False negation"
            label = get_label(has_prior)
            
        # Handle false negation cases
        elif re.search(false_negation, err_sentence) and not re.search(false_negation, orig_sentence):
            error_type = "False negation"
            label = get_label(has_prior)
            
        # Handle matching sentences
        elif orig_sentence == err_sentence:
            error_type = "Not applicable"
            label = get_label(has_prior, is_match=True)
            
        # Handle all other cases
        else:
            # Extract features
            locations_original = re.findall(location_pattern, orig_sentence, re.IGNORECASE)
            locations_error = re.findall(location_pattern, err_sentence, re.IGNORECASE)
            severity_original = re.findall(severity_pattern, orig_sentence, re.IGNORECASE)
            severity_error = re.findall(severity_pattern, err_sentence, re.IGNORECASE)
            devices_original = re.findall(devices_pattern, orig_sentence, re.IGNORECASE)
            devices_error = re.findall(devices_pattern, err_sentence, re.IGNORECASE)
            measurement_original = re.findall(measurement_pattern, orig_sentence, re.IGNORECASE)
            measurement_error = re.findall(measurement_pattern, err_sentence, re.IGNORECASE)
            
            results = find_homophones_and_typos(orig_sentence, err_sentence)
            
            # Determine error type
            if results['homophones'] or results['typos']:
                error_type = "Change to homophone" if len(results['homophones']) > len(results['typos']) else "Add typo"
            elif devices_original != devices_error:
                error_type = "Change name of device"
            elif len(devices_error) > 0 and locations_original != locations_error:
                error_type = "Change position of device"
            elif locations_original != locations_error:
                error_type = "Change location"
            elif severity_original != severity_error:
                error_type = "Change severity"
            elif measurement_original != measurement_error:
                error_type = "Change measurement"
            else:
                error_type = "False prediction"

            
            label = get_label(has_prior)

        label_list.append(label)
        error_list.append(error_type)

    return label_list, error_list      

if __name__ == "__main__":
    
    # sample ground truth report and error report
    sample_gt_report = "Impression: Compared to chest radiographs since ___, most recently ___.  Large right and moderate left pleural effusions and severe bibasilar atelectasis are unchanged.  Cardiac silhouette is obscured.  No pneumothorax.  Pulmonary edema is mild, obscured radiographically by overlying abnormalities."
    sample_error_report = "Impression: Compared to chest radiographs since ___, most recently ___.  Small right and  left pleural effusions and severe bibasilar atelectasis are unchanged.  Cardiac silhouette is obscured.  No pneumothorax.  Pulmonary edema is severe, obscured radiographically by overlying abnormalities."

    # Sample ground truth and error sentences from splicing.py
    sample_gt_sentences = [
        "Impression: Compared to chest radiographs since ___, most recently ___. ",
        "Large right and moderate left pleural effusions and severe bibasilar atelectasis are unchanged. ",
        "Cardiac silhouette is obscured.",
        "No pneumothorax.",
        "Pulmonary edema is mild, obscured radiographically by overlying abnormalities."
    ]
    sample_error_sentences = [
        "Impression: Compared to chest radiographs since ___, most recently ___. ",
        "Large left and moderate right pleural effusions and severe bibasilar atelectasis are unchanged. ",
        "Cardiac silhouette is visible.",
        "No pneumothorax.",
        "Pulmonary edema is severe, obscured radiographically by overlying abnormalities."
    ]

    # label the errors
    labels, error_types = label_errors(sample_gt_sentences, sample_error_sentences, sample_gt_report, sample_error_report)

    # print the labels and error types
    for label, error_type in zip(labels, error_types):
        print(label, error_type)

