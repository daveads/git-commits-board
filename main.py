import asyncio
import time
import cProfile
from datetime import datetime
import sys
import re

from utils.github_scraper import user_data, UserDataProcessingError
from utils.board_sort import leaderboard_sort
from utils.github_users_list import userlist

profiler = cProfile.Profile()

def get_commit_per_user(data):
    commit_list = []
    for i in data:
        length = len(i.split()) - 1
        contributions = i.split()[length].replace(',', '')  # Remove commas from contributions string
        commit_list.append(int(contributions))
    return commit_list

async def main():
    start_time = time.time()

    githubusername = await userlist()
    try:
        data_list = await user_data(githubusername.split())
        
    except UserDataProcessingError as e:
        print(f"Error processing user data: {e}")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")

    commits = get_commit_per_user(data_list)
    Lead_data = await leaderboard_sort(commits, data_list)
    end_time = time.time()

    
    from utils.generate_html import generate_html_table
    sys.stdout.write(await generate_html_table(Lead_data))
    
    
    execution_time = end_time - start_time
    # sys.stdout.write(f"Execution time: {execution_time} seconds\n")

if __name__ == "__main__":
    asyncio.run(main())
