import pandas as pd
from nltk.corpus import wordnet
import difflib
import phonetics
from nltk import pos_tag
from nltk.tokenize import word_tokenize


# Define patterns for extracting medical concepts

devices_pattern = (
    r'\bpicc\b|\bendotracheal\b|\bnasogastric\b|\btube\b|\bcatheter\b|\bpacemaker\b|\bstent\b|\bng\b|\bet\b|\bett\b|'
    r'\bclip\b|\bstaple\b|\bcoil\b|\bicd\b|\blvad\b|\brvad\b|\btracheostomy\b|\bvalve\b|\bplate\b|\bdevice\b|'
    r'\bdrain\b|\bgastric\b|\belectrode\b|\blead\b|\bport-a-cath\b|\bcath\b|\bclamp\b|\bdefibrillator\b|'
    r'\binternal jugular line\b|\bsubclavian line\b|\bhickman line\b|\bright atrial line\b|\bbroviac line\b|'
    r'\bpacer\b|\btip\b|\bij\b|\bnj\b|\bwires\b|\bsvc\b|\bdobbhoff\b|\bicd\b|\bintubated\b|\bpump\b|\bport\b|'
    r'\bextubate\b|\bnasojejunal\b|\benteric\b|\bimpella\b|\bmitraclip\b|\bsternotomy\b|\bsuture\b|\bsubclavian\b|'
    r'\biabp\b|\bballoon pump\b|\bfilter\b|\bivc filter\b|\btavr\b|\bstent graft\b|\bpigtail\b|\blarge bore\b|'
    r'\bchest tube\b|\bepidural\b|\bstimulator\b|\bfixation\b|\borif\b|\bcentral venous\b|\bICD\b|\bLVAD\b|\bRVAD\b'
)

false_negation = (
    r'\bno\b|\bnot\b|\bunremarkable\b|\bnone\b|\bnormal\b|\bclear\b|\babsent\b'
)

location_pattern = (
    r'right|left|bilateral|lower|upper|middle|mid|midline|lateral|medial|inferior|superior|anterior|posterior'
)

severity_pattern = (
    r'moderate|severe|mild|minimal|marked|significant|extensive|large|small|tiny|massive|gross|focal|diffuse|some'
)

prior_pattern = (
    r'more|regress|advanc|less|fewer|constant|unchanged|prior|new|stable|progressed|interval|previous|further|again|since|increase|improve|remain|worse|persist|remov|similar|cleared|earlier|existing|decrease|reduc|recurren|redemonstrat|resol|still|has enlarged|lower|larger|extubated|smaller|higher|continue|compar|change|develop|before'
)

measurement_pattern = (
    r'mm|cm|meters|inches'
)

def get_nouns(sentence):
    """
    Extract nouns from a sentence
    
    Args:
        sentence: str, input sentence
        
    Returns:
        List of nouns in the sentence
    """
    words = word_tokenize(sentence)
    tagged = pos_tag(words)
    nouns = [word.lower() for word, pos in tagged if pos.startswith('N')]
    return nouns

def get_adj(sentence):
    """
    Extract adjectives from a sentence
    
    Args:
        sentence: str, input sentence
        
    Returns:
        List of adjectives in the sentence
    """
    words = word_tokenize(sentence)
    tagged = pos_tag(words)
    adj = [word.lower() for word, pos in tagged if pos.startswith('J')]
    return adj


def find_homophones_and_typos(sentence1, sentence2, max_position_diff=2):
    """
    Detect homophones and typos between two sentences
    """
    def is_valid_word(word):
        return bool(wordnet.synsets(word))
    
    if pd.isna(sentence1) or pd.isna(sentence2):
        return {"homophones": [], "typos": []}
        
    # Tokenize sentences into words
    words1 = sentence1.lower().split()
    words2 = sentence2.lower().split()

    # Generate phonetic representations using Metaphone
    phonetic_words1 = {idx: (word, phonetics.metaphone(word)) for idx, word in enumerate(words1)}
    phonetic_words2 = {idx: (word, phonetics.metaphone(word)) for idx, word in enumerate(words2)}

    homophones = []
    typos = []

    # First pass: check all nearby words for typos
    for idx1, (word1, _) in phonetic_words1.items():
        for idx2, (word2, _) in phonetic_words2.items():
            if abs(idx1 - idx2) <= max_position_diff and word1 != word2:
                similarity_ratio = difflib.SequenceMatcher(None, word1, word2).ratio()
                
                # High similarity (but not identical) suggests a typo
                if 0.7 <= similarity_ratio < 1.0:
                    typos.append((word1, word2))

    # Second pass: check for homophones among non-typo words
    for idx1, (word1, metaphone1) in phonetic_words1.items():
        for idx2, (word2, metaphone2) in phonetic_words2.items():
            # Skip if already identified as a typo
            if any((word1, word2) in typo or (word2, word1) in typo for typo in typos):
                continue
                
            # Check for homophones
            if metaphone1 == metaphone2 and word1 != word2 and abs(idx1 - idx2) <= max_position_diff:
                # Known homophones
                if (word1 == 'knew' and word2 == 'new') or (word1 == 'new' and word2 == 'knew'):
                    homophones.append((word1, word2))
                    continue
                
                # Check similarity
                similarity_ratio = difflib.SequenceMatcher(None, word1, word2).ratio()
                
                if similarity_ratio < 0.7:  # Lower similarity suggests a homophone
                    # Skip specific non-homophone cases
                    skip_pairs = [
                        ('tube', 'tip'), ('due', 'to'), ('no', 'new'),
                        ('an', 'in'), ('as', 'is'), ('air', 'or'),
                        ('1', '2'), ('or', 'are'), ('be', 'by')
                    ]
                    
                    if any((word1, word2) in [pair, pair[::-1]] for pair in skip_pairs):
                        continue
                        
                    if not is_valid_word(word1) or not is_valid_word(word2):
                        continue
                    
                    homophones.append((word1, word2))
    
    return {"homophones": homophones, "typos": typos}
