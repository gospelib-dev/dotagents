#!/usr/bin/env python3
"""
Comprehensive text analysis tool for n-gram frequency and readability testing.
Usage: python analyze.py <file> [options]

No external dependencies required — uses only Python standard library.
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
import os

# Common English stop words to exclude from frequency analysis
STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of',
    'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been', 'be', 'have',
    'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may',
    'might', 'must', 'shall', 'can', 'need', 'dare', 'ought', 'used', 'it', 'its',
    'he', 'she', 'they', 'them', 'his', 'her', 'their', 'my', 'your', 'our',
    'this', 'that', 'these', 'those', 'i', 'you', 'we', 'me', 'him', 'us',
    'what', 'which', 'who', 'whom', 'whose', 'where', 'when', 'why', 'how',
    'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other', 'some',
    'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
    'very', 'just', 'also', 'now', 'here', 'there', 'then', 'once', 'if',
    'into', 'through', 'during', 'before', 'after', 'above', 'below', 'up',
    'down', 'out', 'off', 'over', 'under', 'again', 'further', 'any', 'about',
    'being', 'while', 'until', 'against', 'between', 'because', 'even', 'still',
    "it's", "he's", "she's", "that's", "what's", "there's", "here's", "who's",
    "i'm", "you're", "we're", "they're", "i've", "you've", "we've", "they've",
    "i'll", "you'll", "we'll", "they'll", "i'd", "you'd", "we'd", "they'd",
    "isn't", "aren't", "wasn't", "weren't", "hasn't", "haven't", "hadn't",
    "doesn't", "don't", "didn't", "won't", "wouldn't", "couldn't", "shouldn't",
    "can't", "cannot", "let's", "that'll", "who'll", "what'll", "where's",
    "said", 'like', 'back', 'one', 'two', 'get', 'got', 'went', 'go', 'going',
    'come', 'came', 'see', 'saw', 'seen', 'know', 'knew', 'known', 'think',
    'thought', 'make', 'made', 'take', 'took', 'taken', 'give', 'gave', 'given',
    'tell', 'told', 'say', 'says', 'put', 'seem', 'seemed', 'seems', 'feel',
    'felt', 'look', 'looked', 'looking', 'looks', 'want', 'wanted', 'way',
    'well', 'much', 'many', 'something', 'nothing', 'anything', 'everything',
    'someone', 'anyone', 'everyone', 'nobody', 'thing', 'things', 'time',
    'long', 'little', 'big', 'great', 'old', 'new', 'first', 'last', 'next',
    'good', 'right', 'left', 'hand', 'hands', 'head', 'eyes', 'face', 'voice',
}


AVOID_LIST_PATHS = ('guides/avoid-list.md', '.github/resources/avoid-list.md')  # second: older book branches


def find_avoid_list(search_from=None):
    """Find the avoid list of the repo holding `search_from` (a file or dir), else of the cwd.

    The script is shared outside any repo, so never search from its own location.
    """
    starts = [Path(search_from).resolve()] if search_from else []
    starts.append(Path.cwd().resolve())
    for start in starts:
        for directory in (start, *start.parents):
            for rel in AVOID_LIST_PATHS:
                if (directory / rel).is_file():
                    return directory / rel
    return None


def load_avoid_list(search_from=None) -> dict:
    """Load avoid-list.md and parse phrases by severity level."""
    avoid_file = find_avoid_list(search_from)
    if avoid_file is None:
        print("Warning: no guides/avoid-list.md found above the analyzed file or the current "
              "directory; avoid-list checks skipped.", file=sys.stderr)
        return {'banned': [], 'forbidden': [], 'avoid': [], 'limit': [], 'caution': []}
    
    content = avoid_file.read_text(encoding='utf-8')
    
    avoid_list = {
        'banned': [],
        'forbidden': [],
        'avoid': [],
        'limit': [],
        'caution': [],
    }
    
    current_section = None
    in_table = False
    
    for line in content.split('\n'):
        line = line.strip()
        
        # Detect section headers
        if '## 🚫 BANNED' in line:
            current_section = 'banned'
            in_table = False
            continue
        elif '## ⛔ FORBIDDEN' in line:
            current_section = 'forbidden'
            in_table = False
            continue
        elif '## 🔴 AVOID' in line:
            current_section = 'avoid'
            in_table = False
            continue
        elif '## 🟠 LIMIT' in line:
            current_section = 'limit'
            in_table = False
            continue
        elif '## 🟡 CAUTION' in line:
            current_section = 'caution'
            in_table = False
            continue
        
        # Skip empty lines and headers
        if not line or line.startswith('#'):
            in_table = False
            continue
        
        # Detect table headers and start tracking table
        if '|' in line and ('---' in line or 'Phrase' in line or 'Pattern' in line or 'Action' in line or 'Word' in line):
            in_table = True
            continue
        
        # Parse table rows
        if in_table and current_section and '|' in line:
            # Split by | and extract first cell
            cells = [cell.strip() for cell in line.split('|')]
            if len(cells) >= 2:
                phrase = cells[1]
                
                # Clean up markdown formatting
                phrase = re.sub(r'\*\*([^*]+)\*\*', r'\1', phrase)  # Remove bold
                phrase = re.sub(r'\*([^*]+)\*', r'\1', phrase)  # Remove italic
                phrase = re.sub(r'`([^`]+)`', r'\1', phrase)  # Remove code
                phrase = re.sub(r'~~([^~]+)~~', r'\1', phrase)  # Remove strikethrough
                phrase = phrase.replace('**', '').replace('*', '')
                phrase = phrase.strip().strip('"').strip("'")
                
                if phrase and len(phrase) > 1:
                    avoid_list[current_section].append(phrase.lower())
    
    return avoid_list


def check_avoid_list(text: str, avoid_list: dict) -> dict:
    """Check text for avoid-list phrases and return findings by severity."""
    findings = {
        'banned': [],
        'forbidden': [],
        'avoid': [],
        'limit': [],
        'caution': [],
    }
    
    text_lower = text.lower()
    
    for severity in findings.keys():
        for phrase in avoid_list.get(severity, []):
            if not phrase:
                continue
            
            # Create a regex pattern that matches whole phrases/words
            if ' ' in phrase:
                # For multi-word phrases, use flexible matching
                pattern = re.compile(r'\b' + re.escape(phrase) + r'\b', re.IGNORECASE)
            else:
                # For single words
                pattern = re.compile(r'\b' + re.escape(phrase) + r'\b', re.IGNORECASE)
            
            matches = list(pattern.finditer(text_lower))
            if matches:
                for match in matches:
                    # Find line number
                    line_num = text[:match.start()].count('\n') + 1
                    findings[severity].append({
                        'phrase': phrase,
                        'count': len(matches),
                        'line': line_num,
                        'context': text[max(0, match.start() - 40):min(len(text), match.end() + 40)].replace('\n', ' ').strip()
                    })
    
    # Deduplicate while preserving first occurrence
    for severity in findings.keys():
        seen = set()
        deduplicated = []
        for item in findings[severity]:
            key = (item['phrase'], item['line'])
            if key not in seen:
                seen.add(key)
                deduplicated.append(item)
        findings[severity] = deduplicated
    
    return findings


def count_syllables(word: str) -> int:
    """
    Estimate syllable count for a word.
    Uses a heuristic approach based on vowel patterns.
    """
    word = word.lower().strip()
    if not word:
        return 0
    
    # Handle special cases
    if len(word) <= 3:
        return 1
    
    # Count vowel groups
    vowels = 'aeiouy'
    count = 0
    prev_is_vowel = False
    
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_is_vowel:
            count += 1
        prev_is_vowel = is_vowel
    
    # Adjust for silent 'e' at end
    if word.endswith('e') and count > 1:
        count -= 1
    
    # Adjust for common endings
    if word.endswith(('le', 'les')) and len(word) > 2 and word[-3] not in vowels:
        count += 1
    
    # Ensure at least one syllable
    return max(1, count)


def count_complex_words(words: list) -> int:
    """Count words with 3 or more syllables (for Gunning Fog and SMOG)."""
    return sum(1 for word in words if count_syllables(word) >= 3)


def extract_text(content: str) -> str:
    """Extract plain text from Markdown content."""
    # Remove code blocks
    text = re.sub(r'```[\s\S]*?```', '', content)
    text = re.sub(r'`[^`]+`', '', text)
    
    # Remove Markdown formatting
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)  # Headers
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # Links
    text = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', text)  # Images
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*([^*]+)\*', r'\1', text)  # Italic
    text = re.sub(r'_([^_]+)_', r'\1', text)  # Underscore emphasis
    text = re.sub(r'^[-*+]\s+', '', text, flags=re.MULTILINE)  # List items
    text = re.sub(r'^\d+\.\s+', '', text, flags=re.MULTILINE)  # Numbered lists
    text = re.sub(r'^>\s+', '', text, flags=re.MULTILINE)  # Blockquotes
    text = re.sub(r'---+', '', text)  # Horizontal rules
    text = re.sub(r'\|[^|]+\|', '', text)  # Tables
    
    return text


def tokenize(text: str) -> list:
    """Tokenize text into words."""
    # Convert to lowercase and extract words
    words = re.findall(r"[a-zA-Z]+(?:'[a-zA-Z]+)?", text.lower())
    return words


def get_sentences(text: str) -> list:
    """Split text into sentences."""
    # Handle common abbreviations
    text = re.sub(r'\b(Mr|Mrs|Ms|Dr|Prof|Sr|Jr|vs|etc|e\.g|i\.e)\.\s', r'\1<ABBR> ', text)
    
    # Split on sentence-ending punctuation
    sentences = re.split(r'[.!?]+\s*', text)
    
    # Restore abbreviations and filter empty
    sentences = [s.replace('<ABBR>', '.').strip() for s in sentences if s.strip()]
    
    return sentences


def get_paragraphs(text: str) -> list:
    """Split text into paragraphs."""
    paragraphs = re.split(r'\n\s*\n', text)
    return [p.strip() for p in paragraphs if p.strip()]


def get_ngrams(words: list, n: int) -> list:
    """Generate n-grams from word list."""
    return [' '.join(words[i:i+n]) for i in range(len(words) - n + 1)]


def calculate_readability(words: list, sentences: list) -> dict:
    """Calculate various readability scores."""
    if not words or not sentences:
        return {}
    
    total_words = len(words)
    total_sentences = len(sentences)
    total_syllables = sum(count_syllables(w) for w in words)
    total_characters = sum(len(w) for w in words)
    complex_words = count_complex_words(words)
    
    avg_words_per_sentence = total_words / total_sentences
    avg_syllables_per_word = total_syllables / total_words
    avg_chars_per_word = total_characters / total_words
    
    # Flesch Reading Ease
    flesch_ease = 206.835 - (1.015 * avg_words_per_sentence) - (84.6 * avg_syllables_per_word)
    flesch_ease = max(0, min(100, flesch_ease))
    
    # Flesch-Kincaid Grade Level
    flesch_kincaid = (0.39 * avg_words_per_sentence) + (11.8 * avg_syllables_per_word) - 15.59
    flesch_kincaid = max(0, flesch_kincaid)
    
    # Gunning Fog Index
    gunning_fog = 0.4 * (avg_words_per_sentence + 100 * (complex_words / total_words))
    
    # SMOG Index (requires at least 30 sentences for accuracy)
    if total_sentences >= 30:
        smog = 1.0430 * (30 * complex_words / total_sentences) ** 0.5 + 3.1291
    else:
        # Adjusted formula for shorter texts
        smog = 1.0430 * (complex_words * (30 / total_sentences)) ** 0.5 + 3.1291
    
    # Coleman-Liau Index
    L = (total_characters / total_words) * 100  # avg letters per 100 words
    S = (total_sentences / total_words) * 100  # avg sentences per 100 words
    coleman_liau = 0.0588 * L - 0.296 * S - 15.8
    
    # Automated Readability Index
    ari = 4.71 * (total_characters / total_words) + 0.5 * (total_words / total_sentences) - 21.43
    ari = max(0, ari)
    
    return {
        'flesch_reading_ease': round(flesch_ease, 1),
        'flesch_kincaid_grade': round(flesch_kincaid, 1),
        'gunning_fog': round(gunning_fog, 1),
        'smog_index': round(smog, 1),
        'coleman_liau': round(coleman_liau, 1),
        'ari': round(ari, 1),
        'avg_words_per_sentence': round(avg_words_per_sentence, 1),
        'avg_syllables_per_word': round(avg_syllables_per_word, 2),
        'complex_word_percentage': round(100 * complex_words / total_words, 1),
    }


def interpret_flesch(score: float) -> str:
    """Interpret Flesch Reading Ease score."""
    if score >= 90:
        return "Very Easy (5th grade)"
    elif score >= 80:
        return "Easy (6th grade)"
    elif score >= 70:
        return "Fairly Easy (7th grade)"
    elif score >= 60:
        return "Standard (8th-9th grade)"
    elif score >= 50:
        return "Fairly Difficult (10th-12th grade)"
    elif score >= 30:
        return "Difficult (College)"
    else:
        return "Very Difficult (College graduate)"


def analyze_text(content: str, include_stopwords: bool = False, search_from=None) -> dict:
    """Perform complete text analysis."""
    # Extract plain text
    text = extract_text(content)
    
    # Basic tokenization
    all_words = tokenize(text)
    sentences = get_sentences(text)
    paragraphs = get_paragraphs(text)
    
    # Filter for frequency analysis
    if include_stopwords:
        freq_words = all_words
    else:
        freq_words = [w for w in all_words if w not in STOP_WORDS]
    
    # Calculate statistics
    total_words = len(all_words)
    unique_words = len(set(all_words))
    total_sentences = len(sentences)
    total_paragraphs = len(paragraphs)
    
    # Vocabulary richness
    type_token_ratio = unique_words / total_words if total_words > 0 else 0
    
    # N-gram analysis
    unigrams = Counter(freq_words)
    bigrams = Counter(get_ngrams(all_words, 2))
    trigrams = Counter(get_ngrams(all_words, 3))
    fourgrams = Counter(get_ngrams(all_words, 4))
    
    # Readability scores
    readability = calculate_readability(all_words, sentences)
    
    # Detect overused items
    overused = {
        'words': [],
        'bigrams': [],
        'trigrams': [],
        'fourgrams': [],
    }
    
    # Words appearing > 1% of total
    word_threshold = max(5, total_words * 0.01)
    for word, count in unigrams.most_common():
        if count >= word_threshold and word not in STOP_WORDS:
            overused['words'].append({'phrase': word, 'count': count, 'per_1000': round(1000 * count / total_words, 1)})
    
    # Bigrams: > 5 per 1000 words
    bigram_threshold = max(3, total_words * 0.005)
    for phrase, count in bigrams.most_common():
        words_in_phrase = phrase.split()
        # Skip if mostly stop words
        if sum(1 for w in words_in_phrase if w in STOP_WORDS) < len(words_in_phrase):
            if count >= bigram_threshold:
                overused['bigrams'].append({'phrase': phrase, 'count': count, 'per_1000': round(1000 * count / total_words, 1)})
    
    # Trigrams: > 3 per 1000 words
    trigram_threshold = max(2, total_words * 0.003)
    for phrase, count in trigrams.most_common():
        words_in_phrase = phrase.split()
        if sum(1 for w in words_in_phrase if w in STOP_WORDS) < len(words_in_phrase):
            if count >= trigram_threshold:
                overused['trigrams'].append({'phrase': phrase, 'count': count, 'per_1000': round(1000 * count / total_words, 1)})
    
    # Fourgrams: > 2 per 1000 words
    fourgram_threshold = max(2, total_words * 0.002)
    for phrase, count in fourgrams.most_common():
        words_in_phrase = phrase.split()
        if sum(1 for w in words_in_phrase if w in STOP_WORDS) < len(words_in_phrase):
            if count >= fourgram_threshold:
                overused['fourgrams'].append({'phrase': phrase, 'count': count, 'per_1000': round(1000 * count / total_words, 1)})
    
    # Load and check avoid-list
    avoid_list = load_avoid_list(search_from)
    avoid_findings = check_avoid_list(content, avoid_list)
    
    return {
        'statistics': {
            'total_words': total_words,
            'unique_words': unique_words,
            'total_sentences': total_sentences,
            'total_paragraphs': total_paragraphs,
            'type_token_ratio': round(type_token_ratio, 3),
            'lexical_density': round(100 * unique_words / total_words, 1) if total_words else 0,
        },
        'readability': readability,
        'frequency': {
            'unigrams': unigrams.most_common(50),
            'bigrams': bigrams.most_common(50),
            'trigrams': trigrams.most_common(50),
            'fourgrams': fourgrams.most_common(50),
        },
        'overused': overused,
        'avoid_list': avoid_findings,
    }


def format_output(results: dict, top_n: int = 20, min_freq: int = 2) -> str:
    """Format results as readable text."""
    lines = []
    stats = results['statistics']
    read = results['readability']
    freq = results['frequency']
    overused = results['overused']
    avoid_findings = results.get('avoid_list', {})
    
    # Header
    lines.append("=" * 70)
    lines.append("TEXT ANALYSIS REPORT")
    lines.append("=" * 70)
    
    # Avoid-List Findings (shown first for highest priority)
    has_avoid_findings = any(avoid_findings.get(k, []) for k in avoid_findings)
    if has_avoid_findings:
        lines.append("\n## 🚨 AVOID-LIST FINDINGS\n")
        
        if avoid_findings.get('banned'):
            lines.append("  🚫 BANNED (Never use these):")
            for item in avoid_findings['banned'][:15]:
                lines.append(f"    • Line {item['line']}: \"{item['phrase']}\" (count: {item['count']})")
                lines.append(f"      Context: ...{item['context']}...")
        
        if avoid_findings.get('forbidden'):
            lines.append("\n  ⛔ FORBIDDEN (Find an alternative):")
            for item in avoid_findings['forbidden'][:15]:
                lines.append(f"    • Line {item['line']}: \"{item['phrase']}\" (count: {item['count']})")
                lines.append(f"      Context: ...{item['context']}...")
        
        if avoid_findings.get('avoid'):
            lines.append("\n  🔴 AVOID (Strongly discouraged):")
            for item in avoid_findings['avoid'][:15]:
                lines.append(f"    • Line {item['line']}: \"{item['phrase']}\" (count: {item['count']})")
                lines.append(f"      Context: ...{item['context']}...")
        
        if avoid_findings.get('limit'):
            lines.append("\n  🟠 LIMIT (Use sparingly):")
            for item in avoid_findings['limit'][:10]:
                lines.append(f"    • Line {item['line']}: \"{item['phrase']}\" (count: {item['count']})")
                lines.append(f"      Context: ...{item['context']}...")
        
        if avoid_findings.get('caution'):
            lines.append("\n  🟡 CAUTION (Monitor for overuse):")
            for item in avoid_findings['caution'][:10]:
                lines.append(f"    • Line {item['line']}: \"{item['phrase']}\" (count: {item['count']})")
                lines.append(f"      Context: ...{item['context']}...")
    
    # Basic Statistics
    lines.append("\n## BASIC STATISTICS\n")
    lines.append(f"  Total Words:        {stats['total_words']:,}")
    lines.append(f"  Unique Words:       {stats['unique_words']:,}")
    lines.append(f"  Total Sentences:    {stats['total_sentences']:,}")
    lines.append(f"  Total Paragraphs:   {stats['total_paragraphs']:,}")
    lines.append(f"  Type-Token Ratio:   {stats['type_token_ratio']:.3f}")
    lines.append(f"  Lexical Density:    {stats['lexical_density']}%")
    
    if read:
        lines.append(f"\n  Avg Words/Sentence: {read['avg_words_per_sentence']}")
        lines.append(f"  Avg Syllables/Word: {read['avg_syllables_per_word']}")
        lines.append(f"  Complex Words:      {read['complex_word_percentage']}%")
    
    # Readability Scores
    if read:
        lines.append("\n## READABILITY SCORES\n")
        lines.append(f"  Flesch Reading Ease:    {read['flesch_reading_ease']:5.1f}  ({interpret_flesch(read['flesch_reading_ease'])})")
        lines.append(f"  Flesch-Kincaid Grade:   {read['flesch_kincaid_grade']:5.1f}  (US Grade Level)")
        lines.append(f"  Gunning Fog Index:      {read['gunning_fog']:5.1f}  (Years of Education)")
        lines.append(f"  SMOG Index:             {read['smog_index']:5.1f}  (Years of Education)")
        lines.append(f"  Coleman-Liau Index:     {read['coleman_liau']:5.1f}  (US Grade Level)")
        lines.append(f"  Automated Readability:  {read['ari']:5.1f}  (US Grade Level)")
    
    # Overused Alerts
    has_overused = any(overused[k] for k in overused)
    if has_overused:
        lines.append("\n## ⚠️  OVERUSED WORDS/PHRASES\n")
        
        if overused['words']:
            lines.append("  Words (appearing frequently):")
            for item in overused['words'][:10]:
                lines.append(f"    • \"{item['phrase']}\" — {item['count']}x ({item['per_1000']}/1000 words)")
        
        if overused['bigrams']:
            lines.append("\n  2-Word Phrases:")
            for item in overused['bigrams'][:10]:
                lines.append(f"    • \"{item['phrase']}\" — {item['count']}x ({item['per_1000']}/1000 words)")
        
        if overused['trigrams']:
            lines.append("\n  3-Word Phrases:")
            for item in overused['trigrams'][:10]:
                lines.append(f"    • \"{item['phrase']}\" — {item['count']}x ({item['per_1000']}/1000 words)")
        
        if overused['fourgrams']:
            lines.append("\n  4-Word Phrases:")
            for item in overused['fourgrams'][:10]:
                lines.append(f"    • \"{item['phrase']}\" — {item['count']}x ({item['per_1000']}/1000 words)")
    
    # Top Words
    lines.append("\n## TOP WORDS (excluding common words)\n")
    for word, count in freq['unigrams'][:top_n]:
        if count >= min_freq:
            lines.append(f"  {count:4d}  {word}")
    
    # Top Bigrams
    lines.append("\n## TOP 2-GRAMS\n")
    shown = 0
    for phrase, count in freq['bigrams']:
        if count >= min_freq and shown < top_n:
            words = phrase.split()
            if sum(1 for w in words if w in STOP_WORDS) < len(words):
                lines.append(f"  {count:4d}  \"{phrase}\"")
                shown += 1
    
    # Top Trigrams
    lines.append("\n## TOP 3-GRAMS\n")
    shown = 0
    for phrase, count in freq['trigrams']:
        if count >= min_freq and shown < top_n:
            words = phrase.split()
            if sum(1 for w in words if w in STOP_WORDS) < len(words):
                lines.append(f"  {count:4d}  \"{phrase}\"")
                shown += 1
    
    # Top Fourgrams
    lines.append("\n## TOP 4-GRAMS\n")
    shown = 0
    for phrase, count in freq['fourgrams']:
        if count >= min_freq and shown < top_n:
            words = phrase.split()
            if sum(1 for w in words if w in STOP_WORDS) < len(words):
                lines.append(f"  {count:4d}  \"{phrase}\"")
                shown += 1
    
    lines.append("\n" + "=" * 70)
    
    return '\n'.join(lines)


def format_markdown(results: dict, top_n: int = 20, min_freq: int = 2) -> str:
    """Format results as Markdown."""
    lines = []
    stats = results['statistics']
    read = results['readability']
    freq = results['frequency']
    overused = results['overused']
    avoid_findings = results.get('avoid_list', {})
    
    lines.append("# Text Analysis Report\n")
    
    # Avoid-List Findings (shown first for highest priority)
    has_avoid_findings = any(avoid_findings.get(k, []) for k in avoid_findings)
    if has_avoid_findings:
        lines.append("## 🚨 Avoid-List Findings\n")
        
        if avoid_findings.get('banned'):
            lines.append("### 🚫 BANNED (Never use these)\n")
            lines.append("| Line | Phrase | Count | Context |")
            lines.append("|------|--------|-------|---------|")
            for item in avoid_findings['banned'][:15]:
                context = item['context'][:60].replace('|', '\\|')
                lines.append(f"| {item['line']} | `{item['phrase']}` | {item['count']} | {context}... |")
        
        if avoid_findings.get('forbidden'):
            lines.append("\n### ⛔ FORBIDDEN (Find an alternative)\n")
            lines.append("| Line | Phrase | Count | Context |")
            lines.append("|------|--------|-------|---------|")
            for item in avoid_findings['forbidden'][:15]:
                context = item['context'][:60].replace('|', '\\|')
                lines.append(f"| {item['line']} | `{item['phrase']}` | {item['count']} | {context}... |")
        
        if avoid_findings.get('avoid'):
            lines.append("\n### 🔴 AVOID (Strongly discouraged)\n")
            lines.append("| Line | Phrase | Count | Context |")
            lines.append("|------|--------|-------|---------|")
            for item in avoid_findings['avoid'][:15]:
                context = item['context'][:60].replace('|', '\\|')
                lines.append(f"| {item['line']} | `{item['phrase']}` | {item['count']} | {context}... |")
        
        if avoid_findings.get('limit'):
            lines.append("\n### 🟠 LIMIT (Use sparingly)\n")
            lines.append("| Line | Phrase | Count |")
            lines.append("|------|--------|-------|")
            for item in avoid_findings['limit'][:10]:
                lines.append(f"| {item['line']} | `{item['phrase']}` | {item['count']} |")
        
        if avoid_findings.get('caution'):
            lines.append("\n### 🟡 CAUTION (Monitor for overuse)\n")
            lines.append("| Line | Phrase | Count |")
            lines.append("|------|--------|-------|")
            for item in avoid_findings['caution'][:10]:
                lines.append(f"| {item['line']} | `{item['phrase']}` | {item['count']} |")
    
    # Basic Statistics
    lines.append("## Basic Statistics\n")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| Total Words | {stats['total_words']:,} |")
    lines.append(f"| Unique Words | {stats['unique_words']:,} |")
    lines.append(f"| Total Sentences | {stats['total_sentences']:,} |")
    lines.append(f"| Total Paragraphs | {stats['total_paragraphs']:,} |")
    lines.append(f"| Type-Token Ratio | {stats['type_token_ratio']:.3f} |")
    lines.append(f"| Lexical Density | {stats['lexical_density']}% |")
    if read:
        lines.append(f"| Avg Words/Sentence | {read['avg_words_per_sentence']} |")
        lines.append(f"| Avg Syllables/Word | {read['avg_syllables_per_word']} |")
        lines.append(f"| Complex Words | {read['complex_word_percentage']}% |")
    
    # Readability
    if read:
        lines.append("\n## Readability Scores\n")
        lines.append("| Metric | Score | Interpretation |")
        lines.append("|--------|-------|----------------|")
        lines.append(f"| Flesch Reading Ease | {read['flesch_reading_ease']} | {interpret_flesch(read['flesch_reading_ease'])} |")
        lines.append(f"| Flesch-Kincaid Grade | {read['flesch_kincaid_grade']} | US Grade Level |")
        lines.append(f"| Gunning Fog Index | {read['gunning_fog']} | Years of Education |")
        lines.append(f"| SMOG Index | {read['smog_index']} | Years of Education |")
        lines.append(f"| Coleman-Liau Index | {read['coleman_liau']} | US Grade Level |")
        lines.append(f"| Automated Readability | {read['ari']} | US Grade Level |")
    
    # Overused
    has_overused = any(overused[k] for k in overused)
    if has_overused:
        lines.append("\n## ⚠️ Overused Words/Phrases\n")
        
        if overused['words']:
            lines.append("### Words\n")
            lines.append("| Word | Count | Per 1000 |")
            lines.append("|------|-------|----------|")
            for item in overused['words'][:10]:
                lines.append(f"| {item['phrase']} | {item['count']} | {item['per_1000']} |")
        
        if overused['bigrams']:
            lines.append("\n### 2-Word Phrases\n")
            lines.append("| Phrase | Count | Per 1000 |")
            lines.append("|--------|-------|----------|")
            for item in overused['bigrams'][:10]:
                lines.append(f"| {item['phrase']} | {item['count']} | {item['per_1000']} |")
        
        if overused['trigrams']:
            lines.append("\n### 3-Word Phrases\n")
            lines.append("| Phrase | Count | Per 1000 |")
            lines.append("|--------|-------|----------|")
            for item in overused['trigrams'][:10]:
                lines.append(f"| {item['phrase']} | {item['count']} | {item['per_1000']} |")
    
    # Top Words
    lines.append("\n## Top Words\n")
    lines.append("| Count | Word |")
    lines.append("|-------|------|")
    for word, count in freq['unigrams'][:top_n]:
        if count >= min_freq:
            lines.append(f"| {count} | {word} |")
    
    # Top N-grams
    lines.append("\n## Top 2-Grams\n")
    lines.append("| Count | Phrase |")
    lines.append("|-------|--------|")
    shown = 0
    for phrase, count in freq['bigrams']:
        if count >= min_freq and shown < top_n:
            words = phrase.split()
            if sum(1 for w in words if w in STOP_WORDS) < len(words):
                lines.append(f"| {count} | {phrase} |")
                shown += 1
    
    lines.append("\n## Top 3-Grams\n")
    lines.append("| Count | Phrase |")
    lines.append("|-------|--------|")
    shown = 0
    for phrase, count in freq['trigrams']:
        if count >= min_freq and shown < top_n:
            words = phrase.split()
            if sum(1 for w in words if w in STOP_WORDS) < len(words):
                lines.append(f"| {count} | {phrase} |")
                shown += 1
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Comprehensive text analysis with n-gram frequency and readability testing.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analyze.py chapter.md
  python analyze.py novel/*.md --top 30
  python analyze.py story.md --json | jq '.readability'
  python analyze.py manuscript.md --markdown > report.md
  python analyze.py --text "Sample text to analyze directly"
        """
    )
    parser.add_argument('files', nargs='*', help='File(s) to analyze (optional if using --text)')
    parser.add_argument('--text', type=str, help='Text string to analyze directly (alternative to files)')
    parser.add_argument('--top', type=int, default=20, help='Number of top items to show (default: 20)')
    parser.add_argument('--min-freq', type=int, default=2, help='Minimum frequency to report (default: 2)')
    parser.add_argument('--no-stopwords', action='store_true', help='Include stop words in frequency analysis')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--markdown', action='store_true', help='Output as Markdown')
    
    args = parser.parse_args()
    
    # The avoid list comes from the repo of the first analyzed file (the cwd for --text).
    read_paths = []

    # Validate that either files or --text is provided
    if args.text:
        combined = args.text
    elif args.files:
        # Collect all content from files
        all_content = []
        for file_pattern in args.files:
            path = Path(file_pattern)
            if path.exists():
                try:
                    content = path.read_text(encoding='utf-8')
                    all_content.append(content)
                    read_paths.append(path)
                except Exception as e:
                    print(f"Error reading {path}: {e}", file=sys.stderr)
            else:
                # Try glob pattern
                from glob import glob
                for match in glob(file_pattern):
                    try:
                        content = Path(match).read_text(encoding='utf-8')
                        all_content.append(content)
                        read_paths.append(Path(match))
                    except Exception as e:
                        print(f"Error reading {match}: {e}", file=sys.stderr)
        
        if not all_content:
            print("Error: No files found or readable.", file=sys.stderr)
            sys.exit(1)
        
        # Combine all content
        combined = '\n\n'.join(all_content)
    else:
        print("Error: Either provide files or use --text option.", file=sys.stderr)
        sys.exit(1)
    
    # Analyze
    results = analyze_text(combined, include_stopwords=args.no_stopwords,
                           search_from=read_paths[0] if read_paths else None)
    
    # Output
    if args.json:
        # Convert Counter objects for JSON serialization
        output = {
            'statistics': results['statistics'],
            'readability': results['readability'],
            'frequency': {
                'unigrams': results['frequency']['unigrams'][:args.top],
                'bigrams': results['frequency']['bigrams'][:args.top],
                'trigrams': results['frequency']['trigrams'][:args.top],
                'fourgrams': results['frequency']['fourgrams'][:args.top],
            },
            'overused': results['overused'],
            'avoid_list': results.get('avoid_list', {}),
        }
        print(json.dumps(output, indent=2))
    elif args.markdown:
        print(format_markdown(results, args.top, args.min_freq))
    else:
        print(format_output(results, args.top, args.min_freq))


if __name__ == '__main__':
    main()
