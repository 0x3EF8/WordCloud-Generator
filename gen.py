#!/usr/bin/env python3
"""
Word Cloud Generator
A little script to make word clouds from your text.
Developed by 0x3ef8
"""

import numpy as np # type: ignore
from wordcloud import WordCloud, STOPWORDS # type: ignore
import matplotlib.pyplot as plt # type: ignore
import re
import matplotlib # type: ignore
from collections import Counter

# Font configuration
matplotlib.rcParams['font.family'] = 'Arial'

def preprocess_text(text):
    """Clean up text by making it lowercase, removing punctuation, and fixing spaces."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = ' '.join(text.split())
    return text

def count_words(text):
    """Count how often each word appears, skipping common words like 'the' or 'and'."""
    processed_text = preprocess_text(text)
    words = processed_text.split()
    # Skip stopwords
    stopwords = set(STOPWORDS)
    filtered_words = [word for word in words if word not in stopwords]
    # Count words
    word_counts = Counter(filtered_words)
    return word_counts

def display_word_counts(word_counts, top_n=10):
    """Show the top 10 most common words and their counts."""
    print("\n=== Word Counts ===")
    print(f"{'Word':<20} {'Count':<10}")
    print("-" * 30)
    for word, count in word_counts.most_common(top_n):
        print(f"{word:<20} {count:<10}")
    print(f"\nTotal unique words: {len(word_counts)}")
    print(f"Total words (excluding common words): {sum(word_counts.values())}")

def create_word_cloud(
    input_text,
    cloud_width=1200,
    cloud_height=800,
    bg_color='white',
    font_path=None,
    mask_path=None,
    contour_width=0,
    contour_color='black'
):
    """Make a word cloud from the given text."""
    processed_text = preprocess_text(input_text)

    def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        hues = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']
        return np.random.choice(hues)

    cloud_config = {
        'width': cloud_width,
        'height': cloud_height,
        'background_color': bg_color,
        'max_words': 200,
        'stopwords': STOPWORDS,
        'min_font_size': 10,
        'max_font_size': 150,
        'relative_scaling': 0.5,
        'collocations': False,
        'color_func': color_func,
        'prefer_horizontal': 0.9,
        'font_path': font_path,
        'mask': None,
        'contour_width': contour_width,
        'contour_color': contour_color,
        'scale': 3,
    }

    return WordCloud(**cloud_config).generate(processed_text)

def display_word_cloud(word_cloud, figure_width=15, figure_height=10):
    """Show the word cloud image."""
    plt.figure(figsize=(figure_width, figure_height), dpi=300)
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()

def main():
    """Read data.txt, count words, and create a word cloud."""
    print("=== Word Cloud Generator ===\n")

    try:
        with open('data.txt', 'r', encoding='utf-8') as file:
            text_to_process = file.read().strip()
    except FileNotFoundError:
        print("Oops, couldn't find 'data.txt' in the current folder.")
        return
    except Exception as e:
        print(f"Something went wrong while reading 'data.txt': {e}")
        return

    if not text_to_process:
        print("It looks like 'data.txt' is empty.")
        return

    # Count and show word frequencies
    print("Counting words...")
    word_counts = count_words(text_to_process)
    display_word_counts(word_counts, top_n=10)

    # Create and show word cloud
    print("\nCreating your word cloud...")
    my_wordcloud = create_word_cloud(
        text_to_process,
        font_path=None,
        mask_path=None,
        bg_color='white'
    )

    print("Showing your word cloud...")
    display_word_cloud(my_wordcloud)

    print("\nAll done! Hope you like your word cloud!")

if __name__ == "__main__":
    main()
