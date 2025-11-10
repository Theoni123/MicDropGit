"""
Language analysis utilities for text analysis
Analyzes clarity, word choice, filler words, structure, tone, and repetition
"""

import re
import string
from collections import Counter
import numpy as np

# Try to import NLP libraries
try:
    import spacy
    HAS_SPACY = True
except ImportError:
    HAS_SPACY = False
    spacy = None

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize
    HAS_NLTK = True
    # Download required NLTK data if not already downloaded
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        try:
            nltk.download('punkt', quiet=True)
        except:
            pass
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        try:
            nltk.download('stopwords', quiet=True)
        except:
            pass
except ImportError:
    HAS_NLTK = False
    nltk = None

try:
    import textstat
    HAS_TEXTSTAT = True
except ImportError:
    HAS_TEXTSTAT = False
    textstat = None

# Common filler words
FILLER_WORDS = [
    'um', 'uh', 'er', 'ah', 'like', 'you know', 'actually', 'basically',
    'literally', 'sort of', 'kind of', 'I mean', 'well', 'so', 'right',
    'okay', 'ok', 'yeah', 'yep', 'hmm', 'huh', 'oh', 'wow'
]


def detect_filler_words(text):
    """
    Detect filler words in text
    
    Args:
        text: Input text string
    
    Returns:
        Dictionary with filler word statistics
    """
    if not text:
        return {
            'filler_count': 0,
            'filler_words': {},
            'filler_rate': 0.0,
            'total_words': 0
        }
    
    # Normalize text
    text_lower = text.lower()
    
    # Count filler words
    filler_counts = {}
    total_filler_count = 0
    
    # Split into words
    words = re.findall(r'\b\w+\b', text_lower)
    total_words = len(words)
    
    # Count individual filler words
    for filler in FILLER_WORDS:
        # Handle multi-word fillers
        if ' ' in filler:
            count = len(re.findall(r'\b' + re.escape(filler) + r'\b', text_lower))
        else:
            count = words.count(filler)
        
        if count > 0:
            filler_counts[filler] = count
            total_filler_count += count
    
    # Calculate filler rate (fillers per 100 words)
    filler_rate = (total_filler_count / total_words * 100) if total_words > 0 else 0.0
    
    return {
        'filler_count': total_filler_count,
        'filler_words': filler_counts,
        'filler_rate': filler_rate,
        'total_words': total_words
    }


def analyze_vocabulary_diversity(text):
    """
    Analyze vocabulary diversity and richness
    
    Args:
        text: Input text string
    
    Returns:
        Dictionary with vocabulary statistics
    """
    if not text:
        return {
            'unique_words': 0,
            'total_words': 0,
            'diversity_ratio': 0.0,
            'avg_word_length': 0.0,
            'long_words_count': 0
        }
    
    # Tokenize words
    if HAS_NLTK:
        try:
            words = word_tokenize(text.lower())
            words = [w for w in words if w.isalpha()]
        except:
            words = re.findall(r'\b\w+\b', text.lower())
    else:
        words = re.findall(r'\b\w+\b', text.lower())
    
    if not words:
        return {
            'unique_words': 0,
            'total_words': 0,
            'diversity_ratio': 0.0,
            'avg_word_length': 0.0,
            'long_words_count': 0
        }
    
    total_words = len(words)
    unique_words = len(set(words))
    diversity_ratio = unique_words / total_words if total_words > 0 else 0.0
    
    # Average word length
    word_lengths = [len(w) for w in words]
    avg_word_length = np.mean(word_lengths) if word_lengths else 0.0
    
    # Count long words (6+ characters)
    long_words_count = sum(1 for w in words if len(w) >= 6)
    
    return {
        'unique_words': unique_words,
        'total_words': total_words,
        'diversity_ratio': diversity_ratio,
        'avg_word_length': avg_word_length,
        'long_words_count': long_words_count
    }


def analyze_readability(text):
    """
    Analyze readability metrics using textstat
    
    Args:
        text: Input text string
    
    Returns:
        Dictionary with readability statistics
    """
    if not text or not HAS_TEXTSTAT:
        return {
            'flesch_reading_ease': 0.0,
            'flesch_kincaid_grade': 0.0,
            'smog_index': 0.0,
            'coleman_liau_index': 0.0,
            'automated_readability_index': 0.0
        }
    
    try:
        return {
            'flesch_reading_ease': textstat.flesch_reading_ease(text),
            'flesch_kincaid_grade': textstat.flesch_kincaid_grade(text),
            'smog_index': textstat.smog_index(text),
            'coleman_liau_index': textstat.coleman_liau_index(text),
            'automated_readability_index': textstat.automated_readability_index(text)
        }
    except:
        return {
            'flesch_reading_ease': 0.0,
            'flesch_kincaid_grade': 0.0,
            'smog_index': 0.0,
            'coleman_liau_index': 0.0,
            'automated_readability_index': 0.0
        }


def analyze_sentence_structure(text):
    """
    Analyze sentence structure and complexity
    
    Args:
        text: Input text string
    
    Returns:
        Dictionary with sentence structure statistics
    """
    if not text:
        return {
            'sentence_count': 0,
            'avg_sentence_length': 0.0,
            'avg_words_per_sentence': 0.0,
            'long_sentences_count': 0,
            'short_sentences_count': 0
        }
    
    # Tokenize sentences
    if HAS_NLTK:
        try:
            sentences = sent_tokenize(text)
        except:
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
    else:
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return {
            'sentence_count': 0,
            'avg_sentence_length': 0.0,
            'avg_words_per_sentence': 0.0,
            'long_sentences_count': 0,
            'short_sentences_count': 0
        }
    
    sentence_count = len(sentences)
    
    # Calculate sentence lengths
    sentence_lengths = [len(s) for s in sentences]
    avg_sentence_length = np.mean(sentence_lengths) if sentence_lengths else 0.0
    
    # Count words per sentence
    if HAS_NLTK:
        try:
            words_per_sentence = [len(word_tokenize(s)) for s in sentences]
        except:
            words_per_sentence = [len(re.findall(r'\b\w+\b', s)) for s in sentences]
    else:
        words_per_sentence = [len(re.findall(r'\b\w+\b', s)) for s in sentences]
    
    avg_words_per_sentence = np.mean(words_per_sentence) if words_per_sentence else 0.0
    
    # Count long (>25 words) and short (<10 words) sentences
    long_sentences_count = sum(1 for wps in words_per_sentence if wps > 25)
    short_sentences_count = sum(1 for wps in words_per_sentence if wps < 10)
    
    return {
        'sentence_count': sentence_count,
        'avg_sentence_length': avg_sentence_length,
        'avg_words_per_sentence': avg_words_per_sentence,
        'long_sentences_count': long_sentences_count,
        'short_sentences_count': short_sentences_count
    }


def detect_repetition(text):
    """
    Detect repeated words and phrases
    
    Args:
        text: Input text string
    
    Returns:
        Dictionary with repetition statistics
    """
    if not text:
        return {
            'repeated_words': {},
            'most_repeated': [],
            'repetition_score': 0.0
        }
    
    # Tokenize words
    if HAS_NLTK:
        try:
            words = word_tokenize(text.lower())
            words = [w for w in words if w.isalpha() and len(w) > 2]  # Filter short words
        except:
            words = re.findall(r'\b\w{3,}\b', text.lower())
    else:
        words = re.findall(r'\b\w{3,}\b', text.lower())
    
    if not words:
        return {
            'repeated_words': {},
            'most_repeated': [],
            'repetition_score': 0.0
        }
    
    # Count word frequencies
    word_counts = Counter(words)
    
    # Filter out common words (stopwords)
    if HAS_NLTK:
        try:
            stop_words = set(stopwords.words('english'))
            word_counts = {word: count for word, count in word_counts.items() 
                          if word not in stop_words and count > 2}
        except:
            word_counts = {word: count for word, count in word_counts.items() if count > 2}
    else:
        word_counts = {word: count for word, count in word_counts.items() if count > 2}
    
    # Calculate repetition score (percentage of words that are repeated)
    total_unique = len(set(words))
    repeated_unique = len(word_counts)
    repetition_score = (repeated_unique / total_unique * 100) if total_unique > 0 else 0.0
    
    # Get most repeated words
    most_repeated = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return {
        'repeated_words': dict(word_counts),
        'most_repeated': most_repeated,
        'repetition_score': repetition_score
    }


def analyze_tone(text):
    """
    Analyze tone and formality
    
    Args:
        text: Input text string
    
    Returns:
        Dictionary with tone statistics
    """
    if not text:
        return {
            'formality_score': 0.0,
            'confidence_indicators': 0,
            'engagement_score': 0.0
        }
    
    text_lower = text.lower()
    
    # Formality indicators (formal words/phrases)
    formal_words = [
        'therefore', 'furthermore', 'moreover', 'consequently', 'nevertheless',
        'accordingly', 'subsequently', 'hence', 'thus', 'indeed'
    ]
    
    # Confidence indicators
    confidence_words = [
        'definitely', 'certainly', 'absolutely', 'clearly', 'obviously',
        'undoubtedly', 'surely', 'indeed', 'precisely', 'exactly'
    ]
    
    # Engagement indicators (questions, exclamations, direct address)
    question_count = text.count('?')
    exclamation_count = text.count('!')
    you_count = len(re.findall(r'\byou\b', text_lower))
    we_count = len(re.findall(r'\bwe\b', text_lower))
    
    # Count formal words
    formal_count = sum(1 for word in formal_words if word in text_lower)
    
    # Count confidence words
    confidence_count = sum(1 for word in confidence_words if word in text_lower)
    
    # Calculate scores
    word_count = len(re.findall(r'\b\w+\b', text))
    formality_score = (formal_count / word_count * 100) if word_count > 0 else 0.0
    engagement_score = ((question_count + exclamation_count + you_count + we_count) / 
                        word_count * 100) if word_count > 0 else 0.0
    
    return {
        'formality_score': formality_score,
        'confidence_indicators': confidence_count,
        'engagement_score': engagement_score,
        'question_count': question_count,
        'exclamation_count': exclamation_count
    }


def analyze_grammar_basic(text):
    """
    Basic grammar checking (simple heuristics)
    
    Args:
        text: Input text string
    
    Returns:
        Dictionary with basic grammar statistics
    """
    if not text:
        return {
            'grammar_issues': [],
            'issue_count': 0
        }
    
    issues = []
    
    # Check for common issues
    # Double spaces
    if '  ' in text:
        issues.append('Multiple consecutive spaces detected')
    
    # Check sentence capitalization
    sentences = re.split(r'[.!?]+', text)
    for i, sentence in enumerate(sentences[1:], 1):  # Skip first sentence
        sentence = sentence.strip()
        if sentence and sentence[0].islower():
            issues.append(f'Sentence {i+1} may need capitalization')
    
    # Check for common errors (basic)
    if re.search(r'\bi\s+[a-z]', text):  # Lowercase 'i' not at start
        issues.append("Lowercase 'i' detected (should be 'I')")
    
    return {
        'grammar_issues': issues,
        'issue_count': len(issues)
    }


def analyze_language(text):
    """
    Comprehensive language analysis
    
    Args:
        text: Input text string
    
    Returns:
        Dictionary with all language metrics
    """
    if not text or not text.strip():
        return {
            'filler_words': {},
            'vocabulary': {},
            'readability': {},
            'sentence_structure': {},
            'repetition': {},
            'tone': {},
            'grammar': {}
        }
    
    return {
        'filler_words': detect_filler_words(text),
        'vocabulary': analyze_vocabulary_diversity(text),
        'readability': analyze_readability(text),
        'sentence_structure': analyze_sentence_structure(text),
        'repetition': detect_repetition(text),
        'tone': analyze_tone(text),
        'grammar': analyze_grammar_basic(text)
    }

