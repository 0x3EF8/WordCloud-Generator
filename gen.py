#!/usr/bin/env python3
"""
Word Cloud Generator
A little script to make word clouds from your text.
Developed by 0x3ef8
"""

import numpy as np
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from PIL import Image
import os
from collections import Counter
import re
import matplotlib
import time

# Set matplotlib to use a clean font
matplotlib.rcParams['font.family'] = 'Arial'

def preprocess_text(text):
    """
    Cleans up text to get it ready for the word cloud.
    
    Args:
        text (str): The text you want to use
        
    Returns:
        str: Cleaned-up text
    """
    # Make text lowercase and remove special characters
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    # Fix extra spaces
    text = ' '.join(text.split())
    return text

def get_word_frequencies(text):
    """
    Counts how often each word appears in the text.
    
    Args:
        text (str): The text to count words from
        
    Returns:
        dict: A dictionary with words and their counts
    """
    words = text.split()
    return Counter(words)

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
    """
    Makes a word cloud from your text with some customization options.
    
    Args:
        input_text (str): Text for the word cloud
        cloud_width (int): Width of the word cloud
        cloud_height (int): Height of the word cloud
        bg_color (str): Background color
        font_path (str): Path to a custom font file
        mask_path (str): Path to a mask image file
        contour_width (int): Width of the mask outline
        contour_color (str): Color of the mask outline
    
    Returns:
        WordCloud: The generated word cloud
    """
    # Clean up the text
    processed_text = preprocess_text(input_text)
    
    # Load mask if provided
    mask = None
    if mask_path and os.path.exists(mask_path):
        mask = np.array(Image.open(mask_path))
    
    # Pick random colors for words
    def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        hues = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        return np.random.choice(hues)
    
    # Word cloud configuration
    cloud_config = {
        'width': cloud_width,
        'height': cloud_height,
        'background_color': bg_color,
        'max_words': 200,
        'stopwords': STOPWORDS,
        'min_font_size': 10,
        'max_font_size': 150,
        'relative_scaling': 0.5,
        'collocations': False,  # Skip repeated phrases
        'color_func': color_func,
        'prefer_horizontal': 0.9,
        'font_path': font_path,
        'mask': mask,
        'contour_width': contour_width,
        'contour_color': contour_color,
        'scale': 3,  # Better resolution
    }
    
    # Create the word cloud
    word_cloud = WordCloud(**cloud_config).generate(processed_text)
    return word_cloud

def display_word_cloud(word_cloud, figure_width=15, figure_height=10):
    """
    Shows the word cloud on screen.
    
    Args:
        word_cloud: The word cloud to show
        figure_width (int): Width of the display
        figure_height (int): Height of the display
    """
    plt.figure(figsize=(figure_width, figure_height), dpi=300)
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()

def save_word_cloud(word_cloud, filename='wordcloud.png'):
    """
    Saves the word cloud as an image file.
    
    Args:
        word_cloud: The word cloud to save
        filename (str): Name of the output file
    """
    try:
        word_cloud.to_file(filename)
        print(f"Saved the word cloud as '{filename}'", flush=True)
    except Exception as e:
        print(f"Oops, couldn't save the file: {e}", flush=True)

def main():
    """
    Runs the word cloud generator.
    """
    print("=== Word Cloud Generator ===")
    print("Let's make a word cloud from your text!\n")
    
    # Read the text file
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
    
    # Create the word cloud
    print("\nMaking your word cloud...")
    my_wordcloud = create_word_cloud(
        text_to_process,
        font_path=None,
        mask_path=None,
        bg_color='white'
    )
    
    # Show the word cloud first
    print("Showing your word cloud...")
    display_word_cloud(my_wordcloud)
    
    # Then ask to save the word cloud
    save_choice = input("\nWant to save your word cloud? (y/n): ").lower()
    if save_choice in ['y', 'yes']:
        filename = input("Enter a filename (or press Enter for default): ").strip()
        if not filename:
            filename = 'wordcloud.png'
        elif not filename.endswith('.png'):
            filename += '.png'
        save_word_cloud(my_wordcloud, filename)
    
    print("\nThanks for trying the Word Cloud Generator!")

if __name__ == "__main__":
    main()