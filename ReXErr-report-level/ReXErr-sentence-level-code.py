import openai
import time
openai.api_type = "azure"
openai.api_version = "2023-05-15" 
import json

errors_word_dict = { 
    0: "Add medical device",
    1: "Change name of device",
    2: "Change position of device",
    3: "Change severity",
    4: "Change location",
    5: "False prediction",
    6: "Change measurement",
    7: "Add repetitions",
    8: "Change to homophone",
    9: "Add typo",
    10: "Add contradiction",
    11: "False negation"
}

# Input: {report} to generate errors off of; {errors}, which is a list of three indices defining the errors being added
# Output: error report
def add_multiple_errors(report, errors):
    # general system prompt with particular errors injected
    system_prompt = "The purpose of the following is purely for educational, research, or testing purposes, and not for real medical diagnosis or clinical use. This is not intended for real-world diagnosis or clinical use. You will be given a radiology report of a chest X-ray. Your task is to change the statements in the report so that the report is still clinically plausible but has a different meaning than the previous report. You will be given three classes of errors to generate at a time. Make sure to add as many errors as possible to the report, to every single sentence if you can. Look at each sentence, and if you can add an error, make sure to add it. Only one error per sentence. There should not be cases where a sentence within a report does not contain an error unless it is impossible to add an error. Each of the three error classes you are considering should be separated by numbers surrounded by <<<>>>. For example, the first error would start with <<<1>>>. Each error may or may not contain examples. Avoid making multiple errors within the same sentence. Certain error classes, when provided, are labeled as “priority errors” in brackets, meaning that if it is really not possible to add all of the three error types provided, then do your best to add at the very least the priority error. Keep in mind that the goal should still be to add an error to every sentence and use all error classes. Here are the error classes: <<<1>>> " + errors[0] + " <<<2>>> " + errors[1] + " <<<3>>> " + errors[2] + " MAKE sure that the “<<<>>>” numbers do not show up in your output- these are only provided for your reference to distinguish between errors. Your output should follow exactly the format that is described below. Here are some guidelines to follow when generating the errors. These guidelines may not be relevant for the given class of error you are tasked with generating, but keep them in consideration. Do not combine unrelated findings in the same sentence. Do not reword sentences when the meaning does not change (ex. do not change ‘normal’ to ‘unremarkable’, ‘multiple’ to ‘several’, or ‘abnormality’ to ‘findings’). Do NOT replace one word with another word that has a similar meaning. For example: ‘noticed’ should not be replaced by ‘seen’. Do not change the order of parts of a sentence, when the meaning does not change.\n\nKeep track of the sentence indexes corresponding to the sentences you change in a report. \n\nFor a given report, return a new report with the errors in every sentence according to the above paragraph, two new lines, and then a Python dictionary in the following format: {error sentence index : label, explanation, original sentence index]}. The report should be in the exact same format as the original input report, except with the changed sentences. The new report should not contain newlines or any spacing differences compared to the original report. Make sure this format is followed exactly, including the spacing. The label is determined by the following:\n0: unchanged sentence\n1: changed sentence\nWhen the label is 1: 'explanation' should contain one statement about the error made in the sentence."   
    try:
        time.sleep(0.5)
        response = openai.ChatCompletion.create(
        engine='gpt4o05132024',
        messages=[
        {"role": "system", "content": f"{system_prompt}"},
        {"role": "user", "content": f"{report}"},
        ],
        max_tokens=2000
        )
        output = response.choices[0].message.content
    except: 
        return ""
    return output


if __name__ == "__main__":    
    
    # load in the prompt dictionary
    with open('ReXErr-report-level-error_prompts.json', 'r') as file:
        error_prompts = json.load(file)
    error_prompts = {int(key) if key.isdigit() else key: value for key, value in error_prompts.items()}

    # define example report from mimic
    sample_report = "Impression: Compared to chest radiographs since ___, most recently ___.  Large right and moderate left pleural effusions and severe bibasilar atelectasis are unchanged.  Cardiac silhouette is obscured.  No pneumothorax.  Pulmonary edema is mild, obscured radiographically by overlying abnormalities."

    # example set of errors chose- please refer to above dictionary for what the particular error category each number of the dictionary corresponds to
    # in practice, this was done through the sampling scheme described in the paper
    sample_errors = [error_prompts[3], error_prompts[7], error_prompts[0]]

    # define openai parameters
    openai.api_key = api_key
    openai.api_base = api_base

    error_report = add_multiple_errors(sample_report, sample_errors)
    print(error_report)

