# -*- coding: utf-8 -*-
"""
Created on Mon May 20 15:00:06 2024

@author: Daniel Gallagher
"""

import pandas as pd
from bs4 import BeautifulSoup
import requests, re
import os

# Trophies and Trophy Progression
brawlify_url = 'https://brawlify.com/stats/profile/Q2V0LGG8#gsc.tab=0'
headers = {'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'}
req_brawlify = requests.get(brawlify_url, headers = headers)

soup = BeautifulSoup(req_brawlify.text, "html.parser")
trophies = soup.find('div', class_ = 'col-12 col-md-6 mb-0').find('td', class_ = 'text-left shadow-normal text-warning').text
trophies = re.sub(r',', '', trophies)

Daily_trophy_progression = soup.find('p', class_ = 'text-hp pl-2 mb-2 shadow-normal').find('span', {'id' : 'mainDaily'}).text
Weekly_trophy_progression = soup.find('p', class_ = 'text-hp pl-2 mb-2 shadow-normal').find('span', {'id' : 'mainWeekly'}).text
Daily_trophy_progression = Daily_trophy_progression.replace(r'+', '',)
Weekly_trophy_progression = Weekly_trophy_progression.replace(r'+', '',)

# Highest Trophy Brawler
brawlace_url = 'https://brawlace.com/players/%23Q2V0LGG8'
req_brawlace = requests.get(brawlace_url, headers = headers)

soup2 = BeautifulSoup(req_brawlace.text, "html.parser")
Highest_trophy_brawler = soup2.find('div', class_ = 'table-responsive mt-2').find('td').text
Highest_trophy_brawler = re.sub(r' ', '', Highest_trophy_brawler)

# Daily Win Percentage
brawlifyBattles_url = 'https://brawlify.com/stats/battles/Q2V0LGG8#push-1716217713-1716228967'
req_brawlifyBattles = requests.get(brawlifyBattles_url, headers = headers)

soup3 = BeautifulSoup(req_brawlifyBattles.text, 'html.parser')
Daily_win_percentage = soup3.find('p', class_ = 'pt-2 pl-3 mb-0').find('span', {'class' : 'text-green'}).text
Daily_win_percentage = re.sub(r'%', '', Daily_win_percentage)

# Most Played Mode (Out of 25)
brawlaceModes_url = 'https://brawlace.com/players/%23Q2V0LGG8?filter%5BgameMode%5D=#battlelog-section'
req_brawlaceModes = requests.get(brawlaceModes_url, headers = headers)

soup4 = BeautifulSoup(req_brawlaceModes.text, 'html.parser')

modes = soup4.find_all('option')

# Create a dictionary
modes_dict = {}

for mode in modes:
    value = mode['value']
    text = mode.text
    # Extract the number in parentheses
    number = text.split('(')[-1].split(')')[0] if '(' in text else '0'
    modes_dict[value] = int(number) if number.isdigit() else 0

Most_played_mode = max(modes_dict, key=modes_dict.get).lower()

# Get date
date = pd.Timestamp.now().strftime('%m/%d/%Y')

# Load existing data or create a new DataFrame
file_path = 'BrawlStarsStats.xlsx'
if os.path.exists(file_path):
    df = pd.read_excel(file_path)
else:
    df = pd.DataFrame(columns=[
        'Date', 'Trophies', 'Daily_trophy_progression', 
        'Weekly_trophy_progression', 'Highest_trophy_brawler', 
        'Daily_win_percentage', 'Most_played_mode'
    ])

# Check if the new row's date already exists in the DataFrame
existing_row_index = df[df['Date'] == date].index
if not existing_row_index.empty:
    existing_row_index = existing_row_index[0]
    df.loc[existing_row_index] = {
        'Date': date,
        'Trophies': trophies,
        'Daily_trophy_progression': Daily_trophy_progression,
        'Weekly_trophy_progression': Weekly_trophy_progression,
        'Highest_trophy_brawler': Highest_trophy_brawler,
        'Daily_win_percentage': Daily_win_percentage,
        'Most_played_mode': Most_played_mode
    }
else:
    # Append new data to DataFrame
    new_data = {
        'Date': date,
        'Trophies': trophies,
        'Daily_trophy_progression': Daily_trophy_progression,
        'Weekly_trophy_progression': Weekly_trophy_progression,
        'Highest_trophy_brawler': Highest_trophy_brawler,
        'Daily_win_percentage': Daily_win_percentage,
        'Most_played_mode': Most_played_mode
    }
    df = df.append(new_data, ignore_index=True)

# Save updated DataFrame to Excel
df.to_excel(file_path, index=False)