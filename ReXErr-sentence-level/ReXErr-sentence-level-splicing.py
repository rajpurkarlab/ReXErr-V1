import re
from utils import get_nouns, get_adj

def split_sentences(text):
    """
    Split a block of text into individual sentences.

    Args:
        text: str or list of str, block of text to split into sentences

    Returns:
        List of str, individual sentences
    """
    if isinstance(text, list):
        text = ' '.join(text)

    abbreviations = ['Mr.', 'Mrs.', 'Ms.', 'Dr.', 'Prof.', 'Sr.', 'Jr.', 'e.g.', 'i.e.', 'etc.', 'vs.', 'a.m.', 'p.m.']
    
    # Replace periods in abbreviations with a special marker
    for abbr in abbreviations:
        text = text.replace(abbr, abbr.replace('.', '@'))
    
    pattern = r'(?<!\d\.)(?<=[.!?])\s'
    sentences = re.split(pattern, text)
    sentences = [s.replace('@', '.') for s in sentences]
    return [s.strip() for s in sentences if s.strip()]


def match_sentences(paragraph1, paragraph2):
    """
    Match sentences between two paragraphs based on noun and adjective overlap.
    
    Args:
        paragraph1: str, first paragraph to match
        paragraph2: str, second paragraph to match
        
    Returns:
        Tuple of two lists of tuples, where each tuple contains a sentence from paragraph1 and paragraph2
        that are matched. The first list contains matches from paragraph1 to paragraph2, and the second list
        contains matches from paragraph2 to paragraph1.
    """
    # Split paragraphs into sentences
    sentences1 = split_sentences(paragraph1)
    sentences2 = split_sentences(paragraph2)
    
    # Initialize tracking arrays
    matched_indices2 = [False] * len(sentences2)
    matched_indices1 = [False] * len(sentences1)
    matches1_to_2 = [None] * len(sentences1)
    matches2_to_1 = [None] * len(sentences2)
    
    # First pass: Match findings/impressions sentences
    for i, sentence1 in enumerate(sentences1):
        if matched_indices1[i]:
            continue
            
        nouns1 = get_nouns(sentence1)
        for j, sentence2 in enumerate(sentences2):
            if matched_indices2[j]:
                continue
                
            nouns2 = get_nouns(sentence2)
            # Check for exact matches of 'impression' or 'findings'
            if ('impression' in nouns1 and 'impression' in nouns2) or \
               ('findings' in nouns1 and 'findings' in nouns2):
                matches1_to_2[i] = (sentence1, sentence2)
                matches2_to_1[j] = (sentence1, sentence2)
                matched_indices2[j] = True
                matched_indices1[i] = True
                break
    
    # Second pass: Match exact sentence matches
    for i, sentence1 in enumerate(sentences1):
        if matched_indices1[i]:
            continue
            
        for j, sentence2 in enumerate(sentences2):
            if matched_indices2[j]:
                continue
                
            if sentence1.lower() == sentence2.lower():  # Case-insensitive comparison
                matches1_to_2[i] = (sentence1, sentence2)
                matches2_to_1[j] = (sentence1, sentence2)
                matched_indices2[j] = True
                matched_indices1[i] = True
                break
    
    # Third pass: Match based on adjective and noun overlap
    for i, sentence1 in enumerate(sentences1):
        if matched_indices1[i]:
            continue
            
        nouns1 = get_nouns(sentence1)
        adj1 = get_adj(sentence1)
        best_match_index = None
        max_overlap = 0
        
        for j, sentence2 in enumerate(sentences2):
            if matched_indices2[j]:
                continue
                
            nouns2 = get_nouns(sentence2)
            adj2 = get_adj(sentence2)
            
            # Calculate overlap for both nouns and adjectives
            noun_overlap = sum(1 for noun in nouns1 if noun in nouns2)
            adj_overlap = sum(1 for adj in adj1 if adj in adj2)
            total_overlap = noun_overlap + adj_overlap
            
            # Only consider matches with at least one overlapping noun AND one overlapping adjective
            if noun_overlap > 0 and adj_overlap > 0 and total_overlap > max_overlap:
                max_overlap = total_overlap
                best_match_index = j
        
        # If we found a match with both noun and adjective overlap, use it
        if best_match_index is not None:
            matches1_to_2[i] = (sentence1, sentences2[best_match_index])
            matches2_to_1[best_match_index] = (sentence1, sentences2[best_match_index])
            matched_indices2[best_match_index] = True
            matched_indices1[i] = True
    
    # Fourth pass: Match based only on noun overlap for remaining unmatched sentences
    for i, sentence1 in enumerate(sentences1):
        if matched_indices1[i]:
            continue
            
        nouns1 = get_nouns(sentence1)
        best_match_index = None
        max_overlap = 0
        
        for j, sentence2 in enumerate(sentences2):
            if matched_indices2[j]:
                continue
                
            nouns2 = get_nouns(sentence2)
            noun_overlap = sum(1 for noun in nouns1 if noun in nouns2)
            
            # Only consider matches with at least one overlapping noun
            if noun_overlap > max_overlap:
                max_overlap = noun_overlap
                best_match_index = j
        
        # If we found a match with noun overlap, use it
        if best_match_index is not None and max_overlap > 0:
            matches1_to_2[i] = (sentence1, sentences2[best_match_index])
            matches2_to_1[best_match_index] = (sentence1, sentences2[best_match_index])
            matched_indices2[best_match_index] = True
            matched_indices1[i] = True
    
    # Final pass: Handle unmatched sentences
    for i, matched in enumerate(matched_indices1):
        if not matched:
            matches1_to_2[i] = (sentences1[i], '')
            
    for j, matched in enumerate(matched_indices2):
        if not matched:
            matches2_to_1[j] = ('', sentences2[j])
    
    return matches1_to_2, matches2_to_1

def combine_matches(matches1to2, matches2to1):
    """
    Combines matches1to2 and matches2to1 into a single ordered list of matched pairs.
    Inserts unmatched sentences from matches2to1 in the appropriate positions based on
    surrounding matched sentences.
    
    Args:
        matches1to2: List of tuples (sentence1, sentence2) matching sentences from para1 to para2
        matches2to1: List of tuples (sentence1, sentence2) in para2 order, including unmatched
        
    Returns:
        List of tuples (sentence1, sentence2) in correct combined order
    """
    combined_matches = []
    i = 0
    for match in matches1to2:
        sentence1, sentence2 = match
        if sentence2 == '':
            combined_matches.append(match)
        else:
            while i < len(matches2to1) and matches2to1[i][1] != sentence2:
                combined_matches.append(matches2to1[i])
                i += 1
            if match not in combined_matches:
                combined_matches.append(match)
                i += 1

    # Add remaining unmatched sentences from matches2to1
    for match in matches2to1[i:]:
        # if it has not been added to combined_matches, add it
        if match not in combined_matches:
            combined_matches.append(match)
            
    return combined_matches


if __name__ == '__main__':

    # sample ground truth report and error report
    sample_gt_report = "Impression: Compared to chest radiographs since ___, most recently ___.  Large right and moderate left pleural effusions and severe bibasilar atelectasis are unchanged.  Cardiac silhouette is obscured.  No pneumothorax.  Pulmonary edema is mild, obscured radiographically by overlying abnormalities."
    sample_error_report = "Impression: Compared to chest radiographs since ___, most recently ___.  Small right and  left pleural effusions and severe bibasilar atelectasis are unchanged.  Cardiac silhouette is obscured.  No pneumothorax.  Pulmonary edema is severe, obscured radiographically by overlying abnormalities."

    # split the reports into sentences
    sentences1 = split_sentences(sample_gt_report)
    sentences2 = split_sentences(sample_error_report)

    # match the sentences
    matches1to2, matches2to1 = match_sentences(sample_gt_report, sample_error_report)

    # combine the matches
    combined_matches = combine_matches(matches1to2, matches2to1)

    # print the combined matches
    for match in combined_matches:
        print(match)
