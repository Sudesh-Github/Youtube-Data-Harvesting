import pandas as pd
import streamlit as st
import pymysql
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime
import plotly.express as px
import json

# Assuming 'item' is a JSON string


# Establish MySQL connection
mydb = pymysql.connect(host='127.0.0.1', user='root', password='Master5$', database='sudesh1')
mycursor = mydb.cursor()

# Build YouTube API connection
api_key = "AIzaSyB1AiIkoZl65MxyFDPljJ9Pl4WP-jCF2ww"
youtube = build('youtube', 'v3', developerKey=api_key)

# Create tables if they don't exist
create_channels_table_query = """
CREATE TABLE IF NOT EXISTS channels (
    Channel_id VARCHAR(255) PRIMARY KEY,
    Channel_name VARCHAR(255),
    Playlist_id VARCHAR(255),
    Total_videos INT,
    Playlist_name VARCHAR(255),
    Channel_Views INT,
    Channel_Description TEXT,
    Channel_Status VARCHAR(255)
)
"""
mycursor.execute(create_channels_table_query)

create_videos_table_query = """
CREATE TABLE IF NOT EXISTS videos (
    Video_id VARCHAR(255),
    Channel_id VARCHAR(255),
    Playlist_id VARCHAR(255),
    Video_name VARCHAR(255),
    Video_Description TEXT,
    Published_at DATETIME,
    View_count INT,
    Like_count INT,
    Dislike_count INT,
    Favourite_count INT,
    Comment_count INT,
    Duration INT,
    Thumbnail VARCHAR(255),
    Caption_status VARCHAR(255),
    FOREIGN KEY (Channel_id) REFERENCES channels(Channel_id)
)
"""
mycursor.execute(create_videos_table_query)

create_comments_table_query = """
CREATE TABLE IF NOT EXISTS comments (
    Comment_id VARCHAR(255) PRIMARY KEY,
    Video_id VARCHAR(255),
    Comment_text TEXT,
    Comment_author VARCHAR(255),
    Comment_published_date DATETIME,
    FOREIGN KEY (Video_id) REFERENCES videos(Video_id)

)
"""
mycursor.execute(create_comments_table_query)

# Function to get channel details
def get_channel_details(channel_id):
    ch_data = []
    try:
        response = youtube.channels().list(part='snippet,contentDetails,statistics', id=channel_id).execute()
        for item in response['items']:
            data = {
                'Channel_id': item['id'],
                'Channel_name': item['snippet']['title'],
                'Playlist_id': item['contentDetails']['relatedPlaylists']['uploads'],
                'Total_videos' : item['statistics']['videoCount'],
                'Playlist_name': item['snippet']['title'],
                'Channel_Views': item['statistics']['viewCount'],
                'Channel_Description': item['snippet']['description'],
                'Channel_Status': item['snippet'].get('status')
            }
            ch_data.append(data)
    except HttpError as e:
        st.error(f"Error getting channel details: {e}")
    return ch_data

# Function to insert channels into the database
def insert_channels(ch_details):
    try:
        channel_insert_query = "INSERT INTO channels VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = [(ch['Channel_id'], ch['Channel_name'], ch['Playlist_id'], ch['Total_videos'],
                   ch['Playlist_name'], ch['Channel_Views'], ch['Channel_Description'], ch['Channel_Status']) for ch in ch_details]
        mycursor.executemany(channel_insert_query, values)
        mydb.commit()
    except Exception as e:
        st.error(f"Error inserting channels: {e}")
        mydb.rollback()

# Function to get videos from channel
def get_videos_from_channel(channel_id):
    video_ids = []
    try:
        playlist_response = youtube.channels().list(part='contentDetails', id=channel_id).execute()
        playlist_id = playlist_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        next_page_token = None
        while True:
            playlist_items_response = youtube.playlistItems().list(part='contentDetails', playlistId=playlist_id,
                                                                   maxResults=50, pageToken=next_page_token).execute()
            for item in playlist_items_response['items']:
                video_ids.append(item['contentDetails']['videoId'])
            next_page_token = playlist_items_response.get('nextPageToken')
            if not next_page_token:
                break
    except HttpError as e:
        st.error(f"Error getting videos from channel: {e}")
    return video_ids

# Function to get video details
def get_video_details(video_ids):
    video_data = []
    try:
        for video_id in video_ids:
            response = youtube.videos().list(
                part="snippet,statistics,contentDetails",
                id=video_id
            ).execute()

            for item in response['items']:
                channel_id = get_channel_id(item['snippet']['channelTitle'])
                if(channel_id):
                    data = {
                    'Video_id': item['id'],
                    'Channel_id': channel_id,
                    'Video_name': item['snippet']['title'],
                    'Video_Description': item['snippet']['description'],
                    'Published_at': item['snippet']['publishedAt'],
                    'View_count': item['statistics']['viewCount'],
                    'Like_count': item['statistics'].get('likeCount'),
                    'Dislike_count': item['statistics'].get('dislikeCount'),
                    'Favourite_count': item['statistics'].get('favouriteCount'),
                    'Comment_count': item['statistics'].get('commentCount'),
                    'Duration': item['statistics'].get('duration'),
                    'Thumbnail': item['statistics'].get('thumbnail'),
                    'Caption_status': item['snippet'].get('captionstatus'),
                     }
                video_data.append(data)
    except HttpError as e:
        st.error(f"Error getting video details: {e}")
    return video_data

# Function to insert videos into the databasef
def insert_videos(video_data):
    try:
        video_insert_query = """
        INSERT INTO videos (Video_id, Channel_id, Video_name, Video_Description, Published_at, View_count,
        Like_count, Dislike_count, Favourite_count, Comment_count, Duration, Thumbnail, Caption_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = [(video['Video_id'], video['Channel_id'], video['Video_name'], video['Video_Description'],
                    datetime.strptime(video['Published_at'], '%Y-%m-%dT%H:%M:%SZ'), video['View_count'], video['Like_count'], video['Dislike_count'], video ['Favourite_count'], 
                    video['Comment_count'], video['Duration'],video['Thumbnail'], video['Caption_status']) 
                    for video in video_data]
        mycursor.executemany(video_insert_query, values)
        mydb.commit()
    except Exception as e:
        st.error(f"Error inserting videos: {e}")
        mydb.rollback()

def get_channel_id(channel_name):
    try:
        query = "SELECT Channel_id FROM channels WHERE Channel_name = %s"
        mycursor.execute(query, (channel_name,))
        result = mycursor.fetchone()
        if result:
            return result[0]  # Return Channel_id if found
        else:
            return None  # Return None if channel not found
    except Exception as e:
        st.error(f"Error retrieving Channel_id: {e}")
        return None
    
# Function to get comments details
def get_comments_details(video_ids):
    comment_data = []
    try:
        for video_id in video_ids:
            response = youtube.commentThreads().list(
                part="snippet,replies",
                videoId=video_id,
                maxResults=100
            ).execute()

            for item in response['items']:
                snippet = item.get('snippet', {}).get('topLevelComment', {}).get('snippet', {})  
                comment_id = item.get('id')
                comment_text = snippet.get('textDisplay')
                comment_author = snippet.get('authorDisplayName')
                # Extract and format comment published date
                comment_published_at = snippet.get('publishedAt')
                comment_published_date = None
                if comment_published_at:
                    comment_published_date = datetime.strptime(comment_published_at, '%Y-%m-%dT%H:%M:%SZ')
                
                data = {
                    'Comment_id': comment_id,
                    'Video_id': video_id,
                    'Comment_text': snippet['textDisplay'],
                    'Comment_author': comment_author,
                    'Comment_published_date': comment_published_date
                }
                comment_data.append(data)
    except HttpError as e:
        st.error(f"Error getting comment details: {e}")
    existing_video_ids = set()
    
    try:
        mycursor.execute("SELECT Video_id FROM videos")
        existing_video_ids = {row[0] for row in mycursor.fetchall()}
    except Exception as e:
        st.error(f"Error fetching existing video ids: {e}")
    
    valid_comment_data = [comment for comment in comment_data if comment['Video_id'] in existing_video_ids]
    return valid_comment_data

# Function to insert comments into the database
def insert_comments(comment_data):
    try:
        comment_insert_query = """
        INSERT INTO comments (Comment_id, Video_id, Comment_text, Comment_author, Comment_published_date)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = [(comment['Comment_id'], comment['Video_id'], comment['Comment_text'],
                   comment['Comment_author'], (comment['Comment_published_date'])) for comment in comment_data]
        mycursor.executemany(comment_insert_query, values)
        mydb.commit()
    except Exception as e:
        st.error(f"Error inserting comments: {e}")
        mydb.rollback()

# Function to view data
def view_data(table_name):
    try:
        query = f"SELECT * FROM {table_name}"
        mycursor.execute(query)
        data = mycursor.fetchall()
        df = pd.DataFrame(data, columns=[desc[0] for desc in mycursor.description])
        st.write(df)
    except Exception as e:
        st.error(f"Error viewing data: {e}")

# Streamlit interface
def main():
    st.sidebar.title("Menu")
    selected_option = st.sidebar.selectbox("", ["Home", "Extract and Transform", "View"])

    if selected_option == "Home":
        st.title("Welcome to YouTube Data Analysis")

    elif selected_option == "Extract and Transform":
        st.title("Extract and Transform Data")
        channel_id = st.text_input("Enter YouTube Channel ID:")
        if st.button("Extract Data"):
            channel_details = get_channel_details(channel_id)
            if channel_details:
                st.success("Channel details extracted successfully!")
                insert_channels(channel_details)
                video_ids = get_videos_from_channel(channel_id)
                if video_ids:
                    st.success("Videos extracted successfully!")
                    video_data = get_video_details(video_ids)
                    if video_data:
                        st.success("Video details extracted successfully!")
                        insert_videos(video_data)
                        comment_data = []
                        for video_id in video_ids:
                            comment_data.extend(get_comments_details([video_id]))
                        if comment_data:
                            st.success("Comment details extracted successfully!")
                            insert_comments(comment_data)
                        else:
                            st.warning("No comment data extracted.")
                    else:
                        st.warning("No video data extracted.")
                else:
                    st.warning("No videos found for the given channel ID.")
            else:
                st.warning("No channel details extracted.")

    elif selected_option == "View":
     st.title("View Data")
    
    # Define the view_data function
    def view_data(query):
        try:
            mycursor.execute(query)
            data = mycursor.fetchall()
            df = pd.DataFrame(data, columns=[desc[0] for desc in mycursor.description])
            st.write(df)
        except Exception as e:
            st.error(f"Error viewing data: {e}")

    # Define the questions selectbox
        questions = st.selectbox('Questions', [
            'Click the question that you would like to query',
            '1. What are the names of all the videos and their corresponding channels?',
            '2. Which channels have the most number of videos, and how many videos do they have?',
            '3. What are the top 10 most viewed videos and their respective channels?',
            '4. How many comments were made on each video, and what are their corresponding video names?',
            '5. Which videos have the highest number of likes, and what are their corresponding channel names?',
            '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
            '7. What is the total number of views for each channel, and what are their corresponding channel names?',
            '8. What are the names of all the channels that have published videos in the year 2022?',
            '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?',
            '10. Which videos have the highest number of comments, and what are their corresponding channel names?'
        ])

        # Handle different question selections
        if questions == '1. What are the names of all the videos and their corresponding channels?':
            query = """SELECT v.Video_name, c.Channel_name 
                    FROM videos v 
                    INNER JOIN channels c ON v.Channel_id = c.Channel_id"""
            view_data(query)
        
        elif questions == '2. Which channels have the most number of videos, and how many videos do they have?':
            query = """SELECT Channel_name, COUNT(*) AS Total_Videos
                    FROM videos
                    GROUP BY Channel_name
                    ORDER BY Total_Videos DESC"""
            view_data(query)
                    
        elif questions == '3. What are the top 10 most viewed videos and their respective channels?':
            query = """SELECT v.Video_name, c.Channel_name, v.View_count
                    FROM videos v
                    INNER JOIN channels c ON v.Channel_id = c.Channel_id
                    ORDER BY v.View_count DESC
                    LIMIT 10"""
            view_data(query)
        
        elif questions == '4. How many comments were made on each video, and what are their corresponding video names?':
            query = """SELECT v.Video_name, COUNT(c.Comment_id) AS Total_Comments
                    FROM videos v
                    LEFT JOIN comments c ON v.Video_id = c.Video_id
                    GROUP BY v.Video_name"""
            view_data(query)
                    
        elif questions == '5. Which videos have the highest number of likes, and what are their corresponding channel names?':
            query = """SELECT v.Video_name, c.Channel_name, v.Like_count
                    FROM videos v
                    INNER JOIN channels c ON v.Channel_id = c.Channel_id
                    ORDER BY v.Like_count DESC
                    LIMIT 10"""
            view_data(query)
                    
        elif questions == '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?':
            query = """SELECT Video_name, Like_count, Dislike_count
                    FROM videos"""
            view_data(query)
                    
        elif questions == '7. What is the total number of views for each channel, and what are their corresponding channel names?':
            query = """SELECT c.Channel_name, SUM(v.View_count) AS Total_Views
                    FROM videos v
                    INNER JOIN channels c ON v.Channel_id = c.Channel_id
                    GROUP BY c.Channel_name"""
            view_data(query)
                    
        elif questions == '8. What are the names of all the channels that have published videos in the year 2022?':
            query = """SELECT DISTINCT c.Channel_name
                    FROM videos v
                    INNER JOIN channels c ON v.Channel_id = c.Channel_id
                    WHERE YEAR(v.Published_at) = 2022"""
            view_data(query)
        
        elif questions == '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?':
            query = """SELECT c.Channel_name, AVG(v.Duration) AS Average_Duration
                    FROM videos v
                    INNER JOIN channels c ON v.Channel_id = c.Channel_id
                    GROUP BY c.Channel_name"""
            view_data(query)
                    
        elif questions == '10. Which videos have the highest number of comments, and what are their corresponding channel names?':
            query = """SELECT v.Video_name, c.Channel_name, COUNT(cm.Comment_id) AS Total_Comments
                    FROM videos v
                    INNER JOIN channels c ON v.Channel_id = c.Channel_id
                    LEFT JOIN comments cm ON v.Video_id = cm.Video_id
                    GROUP BY v.Video_name
                    ORDER BY Total_Comments DESC
                    LIMIT 10"""
            view_data(query)



if __name__ == "__main__":
    main()