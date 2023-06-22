from tiktokapi import api

TikTokApi = api(username='your_username', password='your_password')

keyword = "cats"  # Replace with your desired keyword
count = 10  # Number of videos to retrieve

videos = TikTokApi.by_hashtag(keyword, count=count)
for video in videos:
    # Access the attributes of each video
    video_id = video['id']
    author = video['author']['uniqueId']
    description = video['desc']
    print(f"Video ID: {video_id}, Author: {author}, Description: {description}")
