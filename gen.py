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

# Font configuration
matplotlib.rcParams['font.family'] = 'Arial'

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = ' '.join(text.split())
    return text

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
    processed_text = preprocess_text(input_text)

    def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        hues = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'] # add more hex colors if you want
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
    plt.figure(figsize=(figure_width, figure_height), dpi=300)
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()

def main():
    print("=== Word Cloud Generator ===\n")

    try:
        with open('data.txt', 'r', encoding='utf-8') as file:
            text_to_process = file.read().strip()
    except FileNotFoundError:
        print("Sorry, I couldn't find 'data.txt' in this folder.")
        return
    except Exception as e:
        print(f"Something went wrong reading 'data.txt': {e}")
        return

    if not text_to_process:
        print("Looks like 'data.txt' is empty.")
        return

    print("\nMaking your word cloud...")
    my_wordcloud = create_word_cloud(
        text_to_process,
        font_path=None,
        mask_path=None,
        bg_color='white'
    )

    print("Showing your word cloud...")
    display_word_cloud(my_wordcloud)

    print("\nThanks for trying the Word Cloud Generator!")

if __name__ == "__main__":
    main()
