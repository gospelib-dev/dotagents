#!/usr/bin/env python3
"""
Extract sections from markdown files with context summaries.

Usage:
    python extract.py <file_or_dir_or_glob> [section_pattern] [options]

Examples:
    python extract.py STORY.md "Scene 3"
    python extract.py STORY.md "Act II Scene 3"           # Soft match: finds Act II AND Scene 3
    python extract.py STORY.md "Chapter 8; Act II Scene 4" # Multiple queries separated by ;
    python extract.py STORY.md "Chapter 3" --related       # Also extracts sections linked via internal links

Multi-File Search:
    python extract.py ./docs/                              # All .md files in directory (shallow)
    python extract.py ./docs/ -r                           # All .md files recursively
    python extract.py "*.md"                               # Glob pattern
    python extract.py "**/*.md" "Scene 3"                  # Glob with pattern filter

Header Listing:
    python extract.py STORY.md --list                      # List all headers
    python extract.py STORY.md --tree                      # Show header tree structure
    python extract.py STORY.md --list --summary            # List with brief summaries
    python extract.py ./docs/ -r --tree                    # Tree across multiple files

Hierarchical Selectors (CSS-like):
    python extract.py STORY.md "## Main Characters > Mara"          # Direct child
    python extract.py STORY.md "Main Characters >> Theo"            # Any descendant
    python extract.py STORY.md "## Main Characters > ### Mara"      # With explicit levels
    python extract.py STORY.md "Act I > Scene 2 + Scene 3"          # Adjacent sibling
    python extract.py STORY.md "Act I > Scene 2 ~ Scene 5"          # General sibling

Selector Operators:
    >   Direct child (immediate next heading level)
    >>  Descendant (any level below)
    +   Adjacent sibling (next section at same level)
    ~   General sibling (any following section at same level)
    ;   Multiple selectors (OR)
    ##  Level prefix (e.g., ## = level 2, ### = level 3)
"""

import argparse
import glob
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Generator


@dataclass
class Section:
    """Represents a markdown section."""
    heading: str
    level: int
    line_start: int
    line_end: int
    content: str
    anchor: str = ""
    source_file: Optional[str] = None  # For multi-file operations
    is_key_value: bool = False  # True if this is a **Key**: Value pseudo-section
    parent_section_start: Optional[int] = None  # Line start of containing section (for key-value pairs)
    
    def __post_init__(self):
        if not self.anchor:
            self.anchor = self._generate_anchor()
    
    def _generate_anchor(self) -> str:
        """Generate a GitHub-compatible markdown anchor from heading text."""
        anchor = self.heading.lower()
        # Replace & with - (GitHub behavior - space around & becomes --)
        anchor = re.sub(r'\s*&\s*', '--', anchor)
        # Replace other special chars (except & which is handled) with nothing
        anchor = re.sub(r'[^\w\s-]', '', anchor)
        # Replace spaces with dashes
        anchor = re.sub(r'\s+', '-', anchor)
        # Strip leading/trailing dashes
        anchor = anchor.strip('-')
        return f"#{anchor}"
    
    def summary(self, max_sentences: int = 2) -> str:
        """Get first N sentences as summary."""
        # Skip the heading line itself
        lines = self.content.split('\n')[1:]
        text = ' '.join(line.strip() for line in lines if line.strip() and not line.startswith('#'))
        
        # Extract sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        summary_sentences = sentences[:max_sentences]
        return ' '.join(summary_sentences)[:300] + ('...' if len(' '.join(summary_sentences)) > 300 else '')
    
    def brief_summary(self, max_chars: int = 100) -> str:
        """Get a brief one-line summary of the section."""
        # For key-value pairs, extract the value part
        if self.is_key_value:
            # Content is "**Key**: Value", extract the value
            match = re.match(r'\*\*[^*]+\*\*\s*:\s*(.+)', self.content)
            if match:
                value = match.group(1).strip()
                if len(value) <= max_chars:
                    return value
                return value[:max_chars-3].rsplit(' ', 1)[0] + '...'
            return ""
        
        # Skip the heading line itself
        lines = self.content.split('\n')[1:]
        text = ' '.join(line.strip() for line in lines if line.strip() and not line.startswith('#') and not line.startswith('|') and not line.startswith('-'))
        
        if not text:
            return ""
        
        # Get first sentence or truncate
        first_sentence = re.split(r'(?<=[.!?])\s+', text)[0]
        if len(first_sentence) <= max_chars:
            return first_sentence
        return first_sentence[:max_chars-3].rsplit(' ', 1)[0] + '...'


@dataclass
class ExtractionResult:
    """Result of section extraction with context."""
    section: Section
    parent: Optional[Section] = None
    previous: Optional[Section] = None
    next_section: Optional[Section] = None
    related: list = field(default_factory=list)
    linked_sections: list = field(default_factory=list)  # Sections from **Scenes**: metadata


def parse_markdown_sections(content: str, include_key_values: bool = True) -> list[Section]:
    """
    Parse a markdown file into sections based on headings.
    
    Also extracts key-value pairs like **Key**: Value as pseudo-sections
    at level 7 (below heading level 6) for searching purposes.
    """
    lines = content.split('\n')
    sections = []
    current_heading = None
    current_level = 0
    current_start = 0
    
    # Pattern for key-value pairs: **Key**: Value (at start of line or after list marker)
    # Matches: **Key**: Value, - **Key**: Value, * **Key**: Value, etc.
    key_value_pattern = re.compile(r'^(?:[-*+]\s+|\d+\.\s+)?\*\*([^*]+)\*\*\s*:\s*(.+)$')
    
    for i, line in enumerate(lines):
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        
        if heading_match:
            # Save previous section
            if current_heading is not None:
                section_content = '\n'.join(lines[current_start:i])
                sections.append(Section(
                    heading=current_heading,
                    level=current_level,
                    line_start=current_start + 1,  # 1-indexed
                    line_end=i,
                    content=section_content
                ))
            
            # Start new section
            current_level = len(heading_match.group(1))
            current_heading = heading_match.group(2).strip()
            current_start = i
    
    # Don't forget the last section
    if current_heading is not None:
        section_content = '\n'.join(lines[current_start:])
        sections.append(Section(
            heading=current_heading,
            level=current_level,
            line_start=current_start + 1,
            line_end=len(lines),
            content=section_content
        ))
    
    # Now extract key-value pairs as pseudo-sections
    if include_key_values:
        key_value_sections = []
        current_parent = None
        current_parent_level = 0
        
        for i, line in enumerate(lines):
            line_num = i + 1  # 1-indexed
            
            # Track current parent section
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if heading_match:
                current_parent_level = len(heading_match.group(1))
                # Find the section that starts at this line
                for section in sections:
                    if section.line_start == line_num:
                        current_parent = section
                        break
                continue
            
            # Check for key-value pattern
            kv_match = key_value_pattern.match(line.strip())
            if kv_match:
                key = kv_match.group(1).strip()
                value = kv_match.group(2).strip()
                
                # Create pseudo-section at level 7 (one below max heading level)
                kv_section = Section(
                    heading=key,
                    level=7,  # Pseudo-level below normal headings
                    line_start=line_num,
                    line_end=line_num,
                    content=f"**{key}**: {value}",
                    is_key_value=True,
                    parent_section_start=current_parent.line_start if current_parent else None
                )
                key_value_sections.append(kv_section)
        
        # Merge key-value sections into main sections list, maintaining order
        if key_value_sections:
            sections.extend(key_value_sections)
            sections.sort(key=lambda s: (s.line_start, -s.level))  # Sort by line, then by level (parents before children)
    
    return sections


@dataclass
class SelectorSegment:
    """Represents one segment of a hierarchical selector."""
    pattern: str          # The text pattern to match
    level: Optional[int]  # Optional explicit level (from # prefix)
    combinator: str       # How this relates to previous: '', '>', '>>', '+', '~'


def is_hierarchical_selector(query: str) -> bool:
    """Check if a query uses hierarchical selector syntax."""
    # Look for CSS-like combinators: >, >>, +, ~
    # But not inside colons (which indicate literal patterns)
    if ':' in query and '>' not in query and '+' not in query and '~' not in query:
        return False
    return bool(re.search(r'\s*(?:>>|>|\+|~)\s*', query))


def parse_selector_segment(segment: str) -> SelectorSegment:
    """
    Parse a single selector segment like "## Main Characters" or "Mara".
    
    Returns SelectorSegment with pattern and optional level.
    """
    segment = segment.strip()
    level = None
    pattern = segment
    
    # Check for # prefix indicating level
    level_match = re.match(r'^(#{1,6})\s+(.+)$', segment)
    if level_match:
        level = len(level_match.group(1))
        pattern = level_match.group(2).strip()
    
    return SelectorSegment(pattern=pattern, level=level, combinator='')


def parse_hierarchical_selector(query: str) -> list[SelectorSegment]:
    """
    Parse a hierarchical selector string into segments.
    
    Examples:
        "## Main Characters > Mara" -> [
            SelectorSegment(pattern="Main Characters", level=2, combinator=''),
            SelectorSegment(pattern="Mara", level=None, combinator='>')
        ]
        "Main Characters >> Theo" -> [
            SelectorSegment(pattern="Main Characters", level=None, combinator=''),
            SelectorSegment(pattern="Theo", level=None, combinator='>>')
        ]
    """
    segments = []
    
    # Tokenize by combinators, preserving the combinator type
    # Order matters: >> before > to avoid partial matching
    tokens = re.split(r'\s*(>>|>|\+|~)\s*', query)
    
    combinator = ''
    for token in tokens:
        token = token.strip()
        if not token:
            continue
        
        if token in ('>', '>>', '+', '~'):
            combinator = token
        else:
            segment = parse_selector_segment(token)
            segment.combinator = combinator
            segments.append(segment)
            combinator = ''
    
    return segments


def build_pattern_regex(pattern: str) -> re.Pattern:
    """
    Build a regex pattern that handles word boundaries correctly.
    
    Specifically handles Roman numerals (I, II, III, IV, V, etc.) to prevent
    "Act I" from matching "Act II" or "Act III".
    """
    escaped = re.escape(pattern)
    
    # Check if pattern ends with a Roman numeral (common case: "Act I", "Scene II")
    # Roman numerals: I, II, III, IV, V, VI, VII, VIII, IX, X, etc.
    roman_pattern = r'(?:Act|Scene|Chapter|Part)\s+[IVXLCDM]+$'
    if re.search(roman_pattern, pattern, re.IGNORECASE):
        # Add word boundary at the end to prevent "Act I" matching "Act II"
        escaped = escaped + r'(?![IVXLCDM])'
    
    # Also check for digit endings (e.g., "Scene 1" shouldn't match "Scene 10")
    if re.search(r'\d$', pattern):
        escaped = escaped + r'(?!\d)'
    
    return re.compile(escaped, re.IGNORECASE)


def section_matches_pattern(section: Section, pattern: str, level: Optional[int] = None) -> bool:
    """Check if a section matches a pattern and optional level constraint."""
    if level is not None and section.level != level:
        return False
    
    regex = build_pattern_regex(pattern)
    return bool(regex.search(section.heading))


def find_ancestors(sections: list[Section], target: Section) -> list[Section]:
    """Find all ancestor sections (parents at decreasing levels) of target."""
    ancestors = []
    current_level = target.level
    
    for section in reversed(sections):
        if section.line_start >= target.line_start:
            continue
        if section.level < current_level:
            ancestors.append(section)
            current_level = section.level
            if current_level == 1:
                break
    
    return list(reversed(ancestors))


def is_direct_child(parent: Section, child: Section, sections: list[Section]) -> bool:
    """Check if child is a direct child of parent (next heading level, no intervening same-level)."""
    if child.line_start <= parent.line_start:
        return False
    if child.level != parent.level + 1:
        return False
    
    # Check no section at parent's level between them
    for section in sections:
        if section.line_start > parent.line_start and section.line_start < child.line_start:
            if section.level <= parent.level:
                return False
    
    return True


def is_descendant(ancestor: Section, descendant: Section, sections: list[Section]) -> bool:
    """Check if descendant is anywhere under ancestor in the hierarchy."""
    if descendant.line_start <= ancestor.line_start:
        return False
    if descendant.level <= ancestor.level:
        return False
    
    # Check no section at ancestor's level or lower between them
    for section in sections:
        if section.line_start > ancestor.line_start and section.line_start < descendant.line_start:
            if section.level <= ancestor.level:
                return False
    
    return True


def is_adjacent_sibling(prev: Section, current: Section, sections: list[Section]) -> bool:
    """Check if current is the immediately next sibling of prev (same level, no intervening same-level)."""
    if current.line_start <= prev.line_start:
        return False
    if current.level != prev.level:
        return False
    
    # Must be next section at this level
    for section in sections:
        if section.line_start > prev.line_start and section.line_start < current.line_start:
            if section.level == prev.level:
                return False
            # Also check if we've left the parent scope
            if section.level < prev.level:
                return False
    
    return True


def is_general_sibling(prev: Section, current: Section, sections: list[Section]) -> bool:
    """Check if current is any following sibling of prev (same level, same parent scope)."""
    if current.line_start <= prev.line_start:
        return False
    if current.level != prev.level:
        return False
    
    # Check we haven't left the parent scope
    for section in sections:
        if section.line_start > prev.line_start and section.line_start < current.line_start:
            if section.level < prev.level:
                return False
    
    return True


def find_sections_hierarchical(sections: list[Section], selector_segments: list[SelectorSegment]) -> list[Section]:
    """
    Find sections matching a hierarchical selector.
    
    Processes segments left-to-right, applying combinators to filter matches.
    """
    if not selector_segments:
        return []
    
    # Start with first segment - find all matching sections
    first = selector_segments[0]
    current_matches = [
        s for s in sections 
        if section_matches_pattern(s, first.pattern, first.level)
    ]
    
    if not current_matches:
        return []
    
    # Process remaining segments with their combinators
    for segment in selector_segments[1:]:
        next_matches = []
        
        for anchor in current_matches:
            # Find sections matching this segment's pattern
            candidates = [
                s for s in sections 
                if section_matches_pattern(s, segment.pattern, segment.level)
            ]
            
            # Filter by combinator relationship to anchor
            for candidate in candidates:
                if segment.combinator == '>':
                    if is_direct_child(anchor, candidate, sections):
                        next_matches.append(candidate)
                elif segment.combinator == '>>':
                    if is_descendant(anchor, candidate, sections):
                        next_matches.append(candidate)
                elif segment.combinator == '+':
                    if is_adjacent_sibling(anchor, candidate, sections):
                        next_matches.append(candidate)
                elif segment.combinator == '~':
                    if is_general_sibling(anchor, candidate, sections):
                        next_matches.append(candidate)
        
        # Deduplicate while preserving order
        seen = set()
        current_matches = []
        for m in next_matches:
            if m.line_start not in seen:
                current_matches.append(m)
                seen.add(m.line_start)
        
        if not current_matches:
            return []
    
    return current_matches


def parse_query(query: str) -> list[list[str]]:
    """
    Parse a query string into multiple query groups.
    
    - Semicolon separates independent queries (OR)
    - Space-separated terms within a query are soft-matched (each term is searched)
    - If a query contains ':' it's treated as a single literal pattern
    
    Example: "Chapter 8; Act II Scene 4" -> [["Chapter 8"], ["Act II", "Scene 4"]]
    Example: "Act II Scene 3" -> [["Act II", "Scene 3"]]
    Example: "Chapter 2: The Long Road" -> [["Chapter 2: The Long Road"]]
    """
    query_groups = []
    
    # Split by semicolon for independent queries
    for subquery in query.split(';'):
        subquery = subquery.strip()
        if not subquery:
            continue
        
        # If query contains ':', treat as single literal pattern (e.g., "Chapter 2: The Long Road")
        if ':' in subquery:
            query_groups.append([subquery])
            continue
        
        # Parse space-separated terms, but keep quoted strings together
        # and recognize patterns like "Act I", "Scene 3", "Chapter 8"
        terms = []
        
        # Pattern to match: "Act I", "Act II", "Scene 1", "Chapter 1", etc.
        # These are treated as single units
        pattern = r'((?:Act|Scene|Chapter|Part)\s+[IVXLCDM\d]+(?:\.\d+)?)|(\S+)'
        
        matches = re.findall(pattern, subquery, re.IGNORECASE)
        for structured, word in matches:
            if structured:
                terms.append(structured.strip())
            elif word:
                # Skip common connecting words
                if word.lower() not in ('the', 'a', 'an', 'and', 'or', 'of', 'in', 'to'):
                    terms.append(word)
        
        if terms:
            query_groups.append(terms)
    
    return query_groups


def find_sections_soft_match(sections: list[Section], terms: list[str], level: Optional[int] = None) -> list[Section]:
    """
    Find sections matching any of the terms (soft match).
    Each term is matched independently against section headings.
    """
    matches = []
    seen_starts = set()
    
    for term in terms:
        regex = build_pattern_regex(term)
        
        for section in sections:
            if section.line_start in seen_starts:
                continue
            if level is not None and section.level != level:
                continue
            if regex.search(section.heading):
                matches.append(section)
                seen_starts.add(section.line_start)
    
    # Sort by line_start to maintain document order
    matches.sort(key=lambda s: s.line_start)
    return matches


def find_sections(sections: list[Section], pattern: str, level: Optional[int] = None) -> list[Section]:
    """Find sections matching the pattern (legacy single-pattern mode)."""
    try:
        regex = re.compile(pattern, re.IGNORECASE)
    except re.error:
        # Treat as literal string if not valid regex
        regex = re.compile(re.escape(pattern), re.IGNORECASE)
    
    matches = []
    for section in sections:
        if level is not None and section.level != level:
            continue
        if regex.search(section.heading):
            matches.append(section)
    
    return matches


def extract_internal_links(content: str) -> list[dict]:
    """
    Extract all internal markdown links from content.
    
    Matches patterns like:
    - [Scene 4: Market Day](#scene-4-market-day)
    - [Act I, Scene 1](#act-i-scene-1-life-aboard-expanded)
    - [STORY.md](STORY.md#chapter-3)
    
    Returns list of dicts with 'text' and 'anchor' keys.
    """
    links = []
    
    # Match markdown links: [text](#anchor) or [text](file#anchor) or [text](file.md#anchor)
    # Captures: [1] = link text, [2] = full href, [3] = anchor part (after #)
    link_pattern = r'\[([^\]]+)\]\(([^)]*#([^)]+))\)'
    
    for match in re.finditer(link_pattern, content):
        text = match.group(1)
        anchor = match.group(3)  # Just the part after #
        links.append({
            'text': text,
            'anchor': f'#{anchor}'
        })
    
    return links


def find_linked_sections(sections: list[Section], target: Section) -> list[Section]:
    """
    Find sections linked via internal markdown links in the target content.
    
    Matches sections by comparing their generated anchors to the link anchors
    found in the content.
    """
    internal_links = extract_internal_links(target.content)
    if not internal_links:
        return []
    
    linked = []
    seen_starts = set()
    
    # Build a set of anchors to find
    target_anchors = {link['anchor'].lower() for link in internal_links}
    
    for section in sections:
        if section.line_start in seen_starts:
            continue
        if section.line_start == target.line_start:
            continue
        
        # Check if this section's anchor matches any of the internal links
        section_anchor_lower = section.anchor.lower()
        if section_anchor_lower in target_anchors:
            linked.append(section)
            seen_starts.add(section.line_start)
    
    # Sort by line_start to maintain document order
    linked.sort(key=lambda s: s.line_start)
    return linked


def find_parent(sections: list[Section], target: Section) -> Optional[Section]:
    """Find the parent section (lower heading level that precedes target)."""
    for section in reversed(sections):
        if section.line_start < target.line_start and section.level < target.level:
            return section
    return None


def find_siblings(sections: list[Section], target: Section) -> tuple[Optional[Section], Optional[Section]]:
    """Find previous and next sections at the same level."""
    same_level = [s for s in sections if s.level == target.level]
    
    previous = None
    next_section = None
    
    for i, section in enumerate(same_level):
        if section.line_start == target.line_start:
            if i > 0:
                previous = same_level[i - 1]
            if i < len(same_level) - 1:
                next_section = same_level[i + 1]
            break
    
    return previous, next_section


def find_related(sections: list[Section], target: Section) -> list[dict]:
    """Find sections referenced in the target content."""
    related = []
    content_lower = target.content.lower()
    
    for section in sections:
        if section.line_start == target.line_start:
            continue
        
        # Count references to this section's heading
        heading_pattern = re.escape(section.heading.split('(')[0].strip().lower())
        if len(heading_pattern) < 4:  # Skip very short headings
            continue
            
        matches = len(re.findall(heading_pattern, content_lower))
        if matches > 0:
            related.append({
                'heading': section.heading,
                'anchor': section.anchor,
                'references': matches,
                'line_start': section.line_start,
                'line_end': section.line_end
            })
    
    # Sort by reference count, descending
    related.sort(key=lambda x: x['references'], reverse=True)
    return related[:10]  # Top 10 related


def extract_with_context(sections: list[Section], target: Section, 
                         include_related: bool = True,
                         include_linked: bool = False) -> ExtractionResult:
    """Extract a section with full context."""
    parent = find_parent(sections, target)
    previous, next_section = find_siblings(sections, target)
    related = find_related(sections, target) if include_related else []
    linked = find_linked_sections(sections, target) if include_linked else []
    
    return ExtractionResult(
        section=target,
        parent=parent,
        previous=previous,
        next_section=next_section,
        related=related,
        linked_sections=linked
    )


def format_markdown(result: ExtractionResult, include_context: bool = True) -> str:
    """Format extraction result as markdown."""
    output = []
    
    output.append(f"# Extracted: {result.section.heading}")
    output.append("")
    
    if include_context:
        output.append("## Context Summary")
        output.append("")
        
        if result.parent:
            output.append(f"**Parent Section**: [{result.parent.heading}]({result.parent.anchor})")
            output.append(f"> {result.parent.summary()}")
            output.append("")
        
        if result.previous:
            output.append(f"**Previous Section**: [{result.previous.heading}]({result.previous.anchor}) (lines {result.previous.line_start}-{result.previous.line_end})")
            output.append(f"> {result.previous.summary(1)}")
            output.append("")
        
        if result.next_section:
            output.append(f"**Next Section**: [{result.next_section.heading}]({result.next_section.anchor}) (lines {result.next_section.line_start}-{result.next_section.line_end})")
            output.append(f"> {result.next_section.summary(1)}")
            output.append("")
        
        if result.linked_sections:
            output.append("## Linked Sections")
            output.append("")
            for section in result.linked_sections:
                output.append(f"- [{section.heading}]({section.anchor}) (lines {section.line_start}-{section.line_end})")
            output.append("")
        
        if result.related:
            output.append("## Related Sections")
            output.append("")
            for ref in result.related:
                output.append(f"- [{ref['heading']}]({ref['anchor']}) (lines {ref['line_start']}-{ref['line_end']}) — Referenced {ref['references']} time(s)")
            output.append("")
    
    output.append("---")
    output.append("")
    output.append("## Content")
    output.append("")
    output.append(result.section.content)
    
    return '\n'.join(output)


def format_json(result: ExtractionResult) -> str:
    """Format extraction result as JSON."""
    data = {
        'section': {
            'heading': result.section.heading,
            'level': result.section.level,
            'line_start': result.section.line_start,
            'line_end': result.section.line_end,
            'anchor': result.section.anchor,
            'content': result.section.content
        },
        'context': {}
    }
    
    if result.section.source_file:
        data['section']['source_file'] = result.section.source_file
    
    if result.parent:
        data['context']['parent'] = {
            'heading': result.parent.heading,
            'summary': result.parent.summary(),
            'anchor': result.parent.anchor,
            'line_start': result.parent.line_start,
            'line_end': result.parent.line_end
        }
    
    if result.previous:
        data['context']['previous'] = {
            'heading': result.previous.heading,
            'summary': result.previous.summary(1),
            'anchor': result.previous.anchor,
            'line_start': result.previous.line_start,
            'line_end': result.previous.line_end
        }
    
    if result.next_section:
        data['context']['next'] = {
            'heading': result.next_section.heading,
            'summary': result.next_section.summary(1),
            'anchor': result.next_section.anchor,
            'line_start': result.next_section.line_start,
            'line_end': result.next_section.line_end
        }
    
    if result.linked_sections:
        data['linked_sections'] = [
            {
                'heading': s.heading,
                'anchor': s.anchor,
                'line_start': s.line_start,
                'line_end': s.line_end
            }
            for s in result.linked_sections
        ]
    
    data['related'] = result.related
    
    return json.dumps(data, indent=2)


# =============================================================================
# Multi-file support functions
# =============================================================================

def resolve_file_targets(path_args: list[str], recursive: bool = False) -> list[Path]:
    """
    Resolve path argument(s) into a list of markdown files.
    
    Handles:
    - Single file: path/to/file.md
    - Multiple files: file1.md file2.md file3.md
    - Directory (shallow): path/to/dir/
    - Directory (recursive): path/to/dir/ with -r flag
    - Glob pattern: **/*.md, *.md, docs/**/*.md
    - Mixed: file.md ./docs/ "*.md"
    
    Returns list of Path objects sorted alphabetically.
    """
    all_files = []
    seen = set()
    
    for path_arg in path_args:
        path = Path(path_arg)
        
        # If it's a single existing file, add it
        if path.is_file():
            if path.suffix.lower() == '.md' and path not in seen:
                all_files.append(path)
                seen.add(path)
            continue
        
        # If it's a directory, find markdown files
        if path.is_dir():
            pattern = '**/*.md' if recursive else '*.md'
            for f in sorted(path.glob(pattern)):
                if f.is_file() and f not in seen:
                    all_files.append(f)
                    seen.add(f)
            continue
        
        # Check if it's a glob pattern (contains wildcards)
        if '*' in path_arg or '?' in path_arg or '[' in path_arg:
            # Try glob from current directory
            for f in sorted(Path('.').glob(path_arg)):
                if f.is_file() and f.suffix.lower() == '.md' and f not in seen:
                    all_files.append(f)
                    seen.add(f)
            continue
        
        # Path doesn't exist - could be a typo or non-existent path
        # Try treating it as a glob pattern anyway (in case user forgot quotes)
        # e.g., "docs/*.md" without quotes might lose the *
        potential_dir = path.parent
        potential_pattern = path.name
        if potential_dir.is_dir() and potential_pattern:
            # Try to find files matching the pattern in the parent directory
            for f in sorted(potential_dir.glob(potential_pattern)):
                if f.is_file() and f.suffix.lower() == '.md' and f not in seen:
                    all_files.append(f)
                    seen.add(f)
    
    return sorted(all_files)


def parse_markdown_sections_from_file(filepath: Path) -> list[Section]:
    """Parse sections from a file, adding source_file metadata."""
    content = filepath.read_text(encoding='utf-8')
    sections = parse_markdown_sections(content)
    
    # Add source file info to each section
    for section in sections:
        section.source_file = str(filepath)
    
    return sections


@dataclass
class FileSection:
    """Represents a file as a virtual section for multi-file tree views."""
    filepath: Path
    sections: list[Section]
    
    @property
    def heading(self) -> str:
        return self.filepath.name
    
    @property
    def level(self) -> int:
        return 0  # Files are above # (level 1)


def collect_all_sections(files: list[Path]) -> list[tuple[Path, list[Section]]]:
    """
    Collect sections from multiple files.
    
    Returns list of (filepath, sections) tuples.
    """
    results = []
    for filepath in files:
        try:
            sections = parse_markdown_sections_from_file(filepath)
            results.append((filepath, sections))
        except Exception as e:
            print(f"Warning: Could not parse {filepath}: {e}", file=sys.stderr)
    return results


def expand_with_related_sections(
    file_sections: list[tuple[Path, list[Section]]],
    pattern: str
) -> list[tuple[Path, list[Section]]]:
    """
    Expand file_sections to include linked/related sections.
    
    When --related is used with --list/--tree, this function:
    1. Finds all sections matching the pattern
    2. Finds sections linked via internal markdown links from those matches
    3. Adds linked sections to the sections list (with deduplication)
    
    Returns updated file_sections with linked sections marked.
    """
    result = []
    
    for filepath, sections in file_sections:
        # Find sections matching the pattern
        matching_sections = [s for s in sections if section_matches_search(s, pattern)]
        
        if not matching_sections:
            # No matches in this file, keep as-is
            result.append((filepath, sections))
            continue
        
        # Find linked sections from all matches
        seen_line_starts = {s.line_start for s in sections}  # Track what we already have
        linked_sections = []
        
        for match in matching_sections:
            linked = find_linked_sections(sections, match)
            for linked_section in linked:
                if linked_section.line_start not in seen_line_starts:
                    linked_sections.append(linked_section)
                    seen_line_starts.add(linked_section.line_start)
        
        if linked_sections:
            # Merge linked sections and sort by line number
            all_sections = sections + linked_sections
            all_sections.sort(key=lambda s: (s.line_start, -s.level))
            result.append((filepath, all_sections))
        else:
            result.append((filepath, sections))
    
    return result


# =============================================================================
# Header listing functions
# =============================================================================

def format_header_list(
    sections: list[Section],
    level_filter: Optional[int] = None,
    pattern: Optional[str] = None,
    include_summary: bool = False,
    source_file: Optional[str] = None
) -> list[str]:
    """
    Format sections as a flat list.
    
    Args:
        sections: List of Section objects
        level_filter: Only include sections at this level (optional)
        pattern: Only include sections matching this pattern (optional)
        include_summary: Include brief summaries
        source_file: File path to show (for multi-file output)
    
    Returns list of formatted lines.
    """
    output = []
    
    for section in sections:
        # Apply level filter (key-value pairs use level 7, so level filter needs special handling)
        if level_filter is not None:
            if section.is_key_value:
                # Key-value pairs are only shown if no level filter or if explicitly filtering for them
                if level_filter != 7:
                    continue
            elif section.level != level_filter:
                continue
        
        # Apply pattern filter
        if pattern:
            if not section_matches_search(section, pattern):
                continue
        
        # Format the line
        if section.is_key_value:
            level_indicator = "**kv**"  # Special indicator for key-value pairs
        else:
            level_indicator = '#' * section.level
        line = f"{level_indicator} {section.heading}"
        
        if source_file:
            line = f"[{source_file}] {line}"
        
        line += f" (L{section.line_start}-{section.line_end})"
        
        if include_summary:
            summary = section.brief_summary()
            if summary:
                line += f"\n    → {summary}"
        
        output.append(line)
    
    return output


def format_header_tree(
    sections: list[Section],
    level_filter: Optional[int] = None,
    pattern: Optional[str] = None,
    include_summary: bool = False,
    file_prefix: Optional[str] = None,
    indent: str = "  "
) -> list[str]:
    """
    Format sections as an indented tree structure.
    
    Args:
        sections: List of Section objects
        level_filter: Only include sections at or below this level (optional)
        pattern: Only include sections matching this pattern (optional)
        include_summary: Include brief summaries
        file_prefix: Optional file name to show at top
        indent: Indentation string per level
    
    Returns list of formatted lines.
    """
    output = []
    
    if file_prefix:
        output.append(f"📄 {file_prefix}")
    
    # Track which sections match pattern (if any) and their ancestors
    matching_lines = set()
    if pattern:
        for section in sections:
            if section_matches_search(section, pattern):
                matching_lines.add(section.line_start)
                # Also mark ancestors as relevant
                for ancestor in find_ancestors(sections, section):
                    matching_lines.add(ancestor.line_start)
    
    for section in sections:
        # Apply level filter (key-value pairs use level 7, so level filter needs special handling)
        if level_filter is not None:
            if section.is_key_value:
                # Key-value pairs are only shown if explicitly matching a pattern
                if not pattern or not section_matches_search(section, pattern):
                    continue
            elif section.level > level_filter:
                continue
        
        # Apply pattern filter - show section if it matches OR is ancestor of a match
        if pattern and section.line_start not in matching_lines:
            continue
        
        # Calculate indent based on level
        if section.is_key_value:
            # Key-value pairs get extra indent to show they're nested content
            base_indent = indent * 7  # Treat as deeply nested
        else:
            base_indent = indent * section.level
        if file_prefix:
            base_indent = indent + base_indent  # Extra indent when file prefix shown
        
        # Format the line
        if section.is_key_value:
            line = f"{base_indent}• {section.heading}"  # Bullet for key-value pairs
        else:
            line = f"{base_indent}{section.heading}"
        line += f" (L{section.line_start}-{section.line_end})"
        
        # Highlight if this is a direct match (not just ancestor)
        if pattern and section_matches_search(section, pattern):
            line += " ✓"
        
        output.append(line)
        
        if include_summary:
            summary = section.brief_summary()
            if summary:
                output.append(f"{base_indent}{indent}→ {summary}")
    
    return output


def section_matches_search(section: Section, pattern: str) -> bool:
    """Check if section matches a search pattern (case-insensitive)."""
    try:
        regex = re.compile(pattern, re.IGNORECASE)
        return bool(regex.search(section.heading))
    except re.error:
        # Treat as literal string if not valid regex
        return pattern.lower() in section.heading.lower()


def format_multi_file_list(
    file_sections: list[tuple[Path, list[Section]]],
    level_filter: Optional[int] = None,
    pattern: Optional[str] = None,
    include_summary: bool = False
) -> str:
    """Format headers from multiple files as a list."""
    output = []
    
    for filepath, sections in file_sections:
        file_output = format_header_list(
            sections,
            level_filter=level_filter,
            pattern=pattern,
            include_summary=include_summary,
            source_file=str(filepath)
        )
        if file_output:
            output.extend(file_output)
    
    return '\n'.join(output)


def format_multi_file_tree(
    file_sections: list[tuple[Path, list[Section]]],
    level_filter: Optional[int] = None,
    pattern: Optional[str] = None,
    include_summary: bool = False
) -> str:
    """Format headers from multiple files as a tree."""
    output = []
    
    for i, (filepath, sections) in enumerate(file_sections):
        if i > 0:
            output.append("")  # Blank line between files
        
        file_output = format_header_tree(
            sections,
            level_filter=level_filter,
            pattern=pattern,
            include_summary=include_summary,
            file_prefix=str(filepath)
        )
        output.extend(file_output)
    
    return '\n'.join(output)


def format_list_json(
    file_sections: list[tuple[Path, list[Section]]],
    level_filter: Optional[int] = None,
    pattern: Optional[str] = None,
    include_summary: bool = False
) -> str:
    """Format headers as JSON."""
    data = {
        'files': []
    }
    
    for filepath, sections in file_sections:
        file_data = {
            'path': str(filepath),
            'headers': []
        }
        
        for section in sections:
            # Apply filters
            if level_filter is not None and section.level != level_filter:
                continue
            if pattern and not section_matches_search(section, pattern):
                continue
            
            header_data = {
                'heading': section.heading,
                'level': section.level,
                'line_start': section.line_start,
                'line_end': section.line_end,
                'anchor': section.anchor
            }
            
            if include_summary:
                header_data['summary'] = section.brief_summary()
            
            file_data['headers'].append(header_data)
        
        if file_data['headers']:
            data['files'].append(file_data)
    
    return json.dumps(data, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description='Extract sections from markdown files with context summaries.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python extract.py STORY.md "Scene 3"
    python extract.py STORY.md "Act II Scene 3"            # Finds Act II AND Scene 3
    python extract.py STORY.md "Chapter 8; Act II Scene 4" # Multiple queries
    python extract.py STORY.md "Chapter 3" --related       # Includes internally linked sections

Multi-File Search:
    python extract.py ./docs/                              # All .md files in directory (shallow)
    python extract.py ./docs/ -r                           # All .md files recursively
    python extract.py "**/*.md"                            # Glob pattern
    python extract.py "docs/**/*.md" "Scene 3"             # Glob with pattern filter
    python extract.py file1.md file2.md "Scene"            # Multiple specific files
    python extract.py ./docs/ ./notes/ -r --list           # Multiple directories

Header Listing:
    python extract.py STORY.md --list                      # List all headers
    python extract.py STORY.md --tree                      # Show header tree structure
    python extract.py STORY.md --list --summary            # List with brief summaries
    python extract.py ./docs/ -r --tree                    # Tree across multiple files
    python extract.py STORY.md --list "Scene"              # List headers matching pattern

Hierarchical Selectors:
    python extract.py STORY.md "## Main Characters > Mara"          # Direct child
    python extract.py STORY.md "Main Characters >> Theo"            # Any descendant
    python extract.py STORY.md "## Main Characters > ### Mara"      # With explicit levels
    python extract.py STORY.md "Act I > Scene 2 + Scene 3"          # Adjacent sibling
    python extract.py STORY.md "Act I > Scene 2 ~ Scene 5"          # General sibling
        """
    )
    parser.add_argument('paths', nargs='+', 
                        help='Path(s) to markdown file(s), directory, or glob pattern')
    parser.add_argument('-p', '--pattern', default=None,
                        help='Heading text, space-separated terms, or semicolon-separated queries (optional for --list/--tree)')
    parser.add_argument('-r', '--recursive', action='store_true',
                        help='Recursively search directories for .md files')
    parser.add_argument('--level', type=int, choices=range(1, 7), 
                        help='Only match headings at this level (1-6)')
    parser.add_argument('--context', dest='context', action='store_true', default=True,
                        help='Include context summaries (default)')
    parser.add_argument('--no-context', dest='context', action='store_false',
                        help='Exclude context summaries')
    parser.add_argument('--related', action='store_true', default=False,
                        help='Include cross-references and sections linked via internal markdown links')
    parser.add_argument('--no-related', dest='related', action='store_false',
                        help='Exclude related section references')
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown',
                        help='Output format (default: markdown)')
    
    # Header listing modes
    parser.add_argument('--list', action='store_true',
                        help='List all headers (flat format)')
    parser.add_argument('--tree', action='store_true',
                        help='Show headers as an indented tree')
    parser.add_argument('--summary', action='store_true',
                        help='Include brief summaries with --list or --tree')
    
    args = parser.parse_args()
    
    # Validate mutually exclusive options
    if args.list and args.tree:
        print("Error: --list and --tree are mutually exclusive", file=sys.stderr)
        sys.exit(1)
    
    # Separate file paths from potential pattern argument
    # If --pattern is not explicitly set, check if last positional arg looks like a pattern
    paths = args.paths
    pattern = args.pattern
    
    if pattern is None and len(paths) > 1:
        # Check if the last argument looks like a search pattern (not a file/dir/glob)
        last_arg = paths[-1]
        last_path = Path(last_arg)
        is_file_or_dir = last_path.exists()
        is_glob = '*' in last_arg or '?' in last_arg or '[' in last_arg
        
        # If it's not a file, directory, or glob pattern, treat as search pattern
        if not is_file_or_dir and not is_glob:
            # Additional check: if it contains spaces or special selector chars, it's likely a pattern
            if ' ' in last_arg or '>' in last_arg or ';' in last_arg or not last_arg.endswith('.md'):
                pattern = last_arg
                paths = paths[:-1]
    
    # Resolve file targets
    files = resolve_file_targets(paths, args.recursive)
    
    if not files:
        # Provide more helpful error message
        path_str = ', '.join(paths)
        if any(Path(p).is_dir() for p in paths if Path(p).exists()):
            print(f"Error: No markdown files found in: {path_str}", file=sys.stderr)
            print("Hint: Use -r/--recursive to search subdirectories", file=sys.stderr)
        elif any(not Path(p).exists() for p in paths):
            non_existent = [p for p in paths if not Path(p).exists() and '*' not in p and '?' not in p]
            if non_existent:
                print(f"Error: Path(s) do not exist: {', '.join(non_existent)}", file=sys.stderr)
            else:
                print(f"Error: No markdown files found matching: {path_str}", file=sys.stderr)
        else:
            print(f"Error: No markdown files found matching: {path_str}", file=sys.stderr)
        sys.exit(1)
    
    # ==========================================================================
    # Header listing mode (--list or --tree)
    # ==========================================================================
    if args.list or args.tree:
        # Collect sections from all files
        file_sections = collect_all_sections(files)
        
        if not file_sections:
            print("Error: No sections found in any file", file=sys.stderr)
            sys.exit(1)
        
        # If --related is used with a pattern, expand to include linked sections
        if args.related and pattern:
            file_sections = expand_with_related_sections(file_sections, pattern)
        
        # Determine output format
        if args.format == 'json':
            output = format_list_json(
                file_sections,
                level_filter=args.level,
                pattern=pattern,
                include_summary=args.summary
            )
        elif args.tree:
            if len(files) == 1:
                # Single file - no need for file prefix
                filepath, sections = file_sections[0]
                output = '\n'.join(format_header_tree(
                    sections,
                    level_filter=args.level,
                    pattern=pattern,
                    include_summary=args.summary,
                    file_prefix=None
                ))
            else:
                output = format_multi_file_tree(
                    file_sections,
                    level_filter=args.level,
                    pattern=pattern,
                    include_summary=args.summary
                )
        else:  # --list
            if len(files) == 1:
                # Single file - no need for file prefix
                filepath, sections = file_sections[0]
                output = '\n'.join(format_header_list(
                    sections,
                    level_filter=args.level,
                    pattern=pattern,
                    include_summary=args.summary,
                    source_file=None
                ))
            else:
                output = format_multi_file_list(
                    file_sections,
                    level_filter=args.level,
                    pattern=pattern,
                    include_summary=args.summary
                )
        
        print(output)
        return
    
    # ==========================================================================
    # Standard extraction mode (requires pattern)
    # ==========================================================================
    if not pattern:
        print("Error: Pattern required for extraction mode (or use --list/--tree)", file=sys.stderr)
        sys.exit(1)
    
    # For standard extraction, process each file and combine results
    all_results = []
    
    for filepath in files:
        try:
            content = filepath.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Warning: Could not read {filepath}: {e}", file=sys.stderr)
            continue
        
        # Parse sections
        sections = parse_markdown_sections(content)
        
        # Add source file info
        for section in sections:
            section.source_file = str(filepath)
        
        # Find all matching sections
        matches = []
        seen_starts = set()
        
        # Split by semicolon for multiple independent selectors
        selector_parts = [p.strip() for p in pattern.split(';') if p.strip()]
        
        for part in selector_parts:
            if is_hierarchical_selector(part):
                # Use hierarchical selector matching
                selector_segments = parse_hierarchical_selector(part)
                part_matches = find_sections_hierarchical(sections, selector_segments)
            else:
                # Use traditional soft-match query parsing
                query_groups = parse_query(part)
                part_matches = []
                for terms in query_groups:
                    term_matches = find_sections_soft_match(sections, terms, args.level)
                    part_matches.extend(term_matches)
            
            for match in part_matches:
                if match.line_start not in seen_starts:
                    matches.append(match)
                    seen_starts.add(match.line_start)
        
        # Sort by document order
        matches.sort(key=lambda s: s.line_start)
        
        # Extract with context
        for match in matches:
            result = extract_with_context(
                sections, match, 
                include_related=args.related,
                include_linked=args.related
            )
            all_results.append((filepath, result))
            
            # If --related is set, collect linked sections
            if args.related and result.linked_sections:
                for linked in result.linked_sections:
                    if linked.line_start not in seen_starts:
                        linked_result = extract_with_context(
                            sections, linked,
                            include_related=False,
                            include_linked=False
                        )
                        all_results.append((filepath, linked_result))
                        seen_starts.add(linked.line_start)
    
    if not all_results:
        print(f"No sections found matching: {pattern}", file=sys.stderr)
        sys.exit(1)
    
    # Sort by file then line start
    all_results.sort(key=lambda x: (str(x[0]), x[1].section.line_start))
    
    # Output
    if args.format == 'json':
        if len(all_results) == 1:
            print(format_json(all_results[0][1]))
        else:
            json_results = [json.loads(format_json(r)) for _, r in all_results]
            print(json.dumps({'matches': json_results}, indent=2))
    else:
        current_file = None
        for i, (filepath, result) in enumerate(all_results):
            # Show file header when switching files in multi-file mode
            if len(files) > 1 and filepath != current_file:
                if current_file is not None:
                    print("\n" + "=" * 80 + "\n")
                print(f"# FILE: {filepath}")
                print("=" * 80 + "\n")
                current_file = filepath
            elif i > 0:
                print("\n" + "-" * 80 + "\n")
            
            print(format_markdown(result, include_context=args.context))


if __name__ == "__main__":
    main()
