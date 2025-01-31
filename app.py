import streamlit as st
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import openai
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Initialize YouTube API
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# Streamlit App
st.title("Mindy")
st.subheader("Discover mindfulness techniques and personalized video recommendations for relaxation.")

st.write("Enter your query to get recommendations.")

# Categories for user guidance
categories = {
    "Mindfulness and Meditation": ["mindfulness", "guided meditation", "focus meditation"],
    "Breathing Exercises" : ["deep breathing techniques", "4-7-8 breathing", "box breathing"], 
    "Somatic Practices":  ["yoga for relaxation", "tai chi", "progressive muscle relaxation"],
}

# Generate GPT-4 Recommendations
def generate_gpt_recommendations(query, selected_category):
    try:
        # Dynamically adjust the prompt based on the selected category
        if selected_category != "All":
            category_instruction = (
                f"Focus your recommendations specifically on the category: **{selected_category}**. "
                "Only suggest techniques and advice that are directly relevant to this category. "
                "If the query falls outside the scope of this category, state: 'The provided context does not contain this information.'"
            )
        else:
            category_instruction = (
                "Provide general recommendations not limited to any specific category. "
                "Cover a diverse range of actionable techniques related to mindfulness, relaxation, and self-help."
            )
            
        gpt_prompt = f"""
        ## SYSTEM ROLE
        You are an expert chatbot designed to provide actionable, insightful, and personalized advice on **Mindfulness**, **Relaxation**, and **Self-Help Techniques**. 
        If a query is unrelated to these topics, politely inform the user and avoid generating recommendations.
        Based on the user's query, provide **specific techniques** the user can apply, along with actionable advice

        ## USER QUESTION
        The user has asked: 
        "{query}"

        ## CATEGORY CONTEXT
        {category_instruction}

        ## GUIDELINES
        1. **Accuracy**:  
           - Provide actionable techniques tailored to the query 
           - Prioritize recommendations from CATEGORY CONTEXT and base your suggestions on the user's query.
           - If the answer cannot be found, explicitly state: "The provided context does not contain this information."
           - Use actionable language to recommend techniques for relaxation and mindfulness.
           
        2. **Actionable Techniques**: Suggest **specific techniques** the user can apply (e.g., guided breathing, mindfulness meditation, progressive muscle relaxation). Explain:
           - How the technique works.
           - How it helps address the query.
           - Steps to apply it.

        3. **Clarity**:  
           - Use simple, professional, and user-friendly language.  
           - Ensure the response is well-structured and formatted in Markdown for readability.  
           
        4. **Category Relevance**:  
           - If a category is provided, ensure all suggestions directly address that category.
           - For example:
             - For "Stress and Anxiety Relief", focus on techniques like deep breathing, mindfulness exercises, and calming practices.
             - For "Sleep and Rest", suggest techniques like guided sleep meditations, sleep hygiene tips, and relaxing yoga poses.

        5. **Response Format**:
           - Include at least two techniques.
           - Use the following structure:
    
        '''
        # [Custom Title Based on the Query]
        Provide a meaningful title based on the user’s query and CATEGORY CONTEXT (e.g., "How to Relax and Sleep Better").

        ## Recommendations
        1. **[Actionable Advice]**: Actionable and insightful advice.
        1. **[Technique Name]**: Detailed explanation of the technique, why it works, and how to apply it].
        2. **[Another Technique Name]**: [Detailed explanation].


        ## Note
        Focus on actionable advice. Avoid vague suggestions.
        '''
        """

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert assistant."},
                {"role": "user", "content": gpt_prompt},
            ],
            temperature=0.7,
            max_tokens=1500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating recommendations: {e}"

# Extract techniques from GPT recommendations
def extract_techniques_and_keywords(gpt_recommendations):
    try:
        techniques_with_keywords = []
        lines = gpt_recommendations.splitlines()
        
        # Step 1: Extract the custom title
        title_keywords = []
        for line in lines:
            if line.startswith("# "):  # Identify the custom title
                title = line[2:].strip()  # Remove the "# " prefix and extract the title
                # Extract keywords from the title
                title_keywords = [
                    word.lower()
                    for word in title.split()
                    if len(word) > 3  # Filter out short/common words
                ]
                break  # Title extraction is complete, no need to continue

        # Step 2: Extract technique name and add title keywords
        for i, line in enumerate(lines):
            if line.startswith("1.") or line.startswith("2."):
                technique_name = line.split("**")[1]  # Extract text within "**[Technique Name]**"

                # Extract additional keywords from the technique name
                technique_keywords = [
                    word.lower()
                    for word in technique_name.split()
                    if len(word) > 3
                ]

                # Combine title keywords and technique keywords
                combined_keywords = technique_keywords + title_keywords
                techniques_with_keywords.append({"technique": technique_name, "keywords": combined_keywords})
        
        return techniques_with_keywords
    except Exception as e:
        st.error(f"Error extracting techniques and keywords: {e}")
        return []


# Fetch videos from YouTube API
def fetch_youtube_videos(query, max_results=10, order="relevance", video_duration=None, video_definition=None):
    try:
        request_params = {
                "q": query,
                "part": "snippet",
                "type": "video",
                "maxResults": max_results,
                "order": order,
        }

        if video_duration:  # Add video duration filter if provided
            request_params["videoDuration"] = video_duration
        if video_definition:  # Add video definition filter if provided
            request_params["videoDefinition"] = video_definition

        response = youtube.search().list(**request_params).execute()

        videos = [
            {
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"],
                "video_id": item["id"]["videoId"],
                "link": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
            }
            for item in response.get("items", [])
        ]
        return videos
    except Exception as e:
        st.error(f"Error fetching videos: {e}")
        return []


def preprocess_text(text):
    # Convert to lowercase and remove special characters
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)  # Remove punctuation and special characters
    return text
    

# Rank videos by similarity to the technique
def rank_videos_by_query(query, videos):
    try:
        video_texts = [
            preprocess_text(video["title"] + " " + video["description"]) for video in videos
        ]
        query_text = preprocess_text(query)

        # Compute similarity using TF-IDF
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform([query_text] + video_texts)
        similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

        # Add similarity scores to videos
        for i, video in enumerate(videos):
            video["similarity_score"] = similarity_scores[i]
        if all(score == 0.0 for score in similarity_scores):
            st.warning("No meaningful matches found based on similarity. Displaying original YouTube ranking.")
            return videos  # Return videos without re-ranking
        return sorted(videos, key=lambda x: x["similarity_score"], reverse=True)
    except Exception as e:
        st.error(f"Error ranking videos: {e}")
        return videos

def build_enriched_query(technique_data):
    # Use only unique keywords for the query
    unique_keywords = list(set(technique_data["keywords"]))  # Remove duplicates
    return " ".join(unique_keywords)

    
# Streamlit Input and Display
query = st.text_input("Enter your query:")
selected_category = st.selectbox("Select a category (optional):", ["All"] + list(categories.keys()))
tab_chatbot, tab_videos = st.tabs(["Chatbot Recommendations", "Video Recommendations"])
with tab_chatbot:
    st.write("### GPT-4 Recommendations")
    generate_button = st.button("Generate Recommendations")
    # Reset button to clear input
    if st.button("Reset"):
        st.experimental_rerun()  # Reset the app
    if generate_button and query:
        with st.spinner("Generating recommendations..."):
            # Step 1: Generate GPT-4 recommendations using the original query and selected category
            gpt_recommendations = generate_gpt_recommendations(query, selected_category)
            st.markdown(gpt_recommendations)  # Display GPT recommendations
    
            # Step 2: Extract techniques and related keywords (including title keywords)
            techniques_with_keywords = extract_techniques_and_keywords(gpt_recommendations)

            # Save recommendations in session state
            st.session_state.techniques_with_keywords = techniques_with_keywords
            
            st.success("Recommendations generated successfully!")
            
with tab_videos:
    st.write("### Video Recommendations")
    if "techniques_with_keywords" not in st.session_state or not st.session_state.techniques_with_keywords:
        st.warning("Please generate recommendations in the 'Chatbot Recommendations' tab first.")
    else:
        with st.spinner("Fetching and ranking videos..."):
            for technique_data in st.session_state.techniques_with_keywords:
                technique = technique_data["technique"]
                enriched_query = build_enriched_query(technique_data)
                
                # Fetch and rank videos using the enriched query
                videos = fetch_youtube_videos(
                    enriched_query,
                    max_results=10,
                    order="relevance",  # Fetch the most-viewed videos
                    video_duration="medium",  # Fetch videos between 4 and 20 minutes
                    video_definition="high"  # Fetch only high-definition videos
                )
                ranked_videos = rank_videos_by_query(enriched_query, videos)
                
                # Display ranked videos
                st.subheader(f"Top Videos for: {technique}")
                for video in ranked_videos[:3]:  # Show top 3 videos per technique
                    st.markdown(f"""
                    - **{video['title']}**  
                      {video['description']}  
                      [Watch here]({video['link']})  
                      **Similarity Score**: {video['similarity_score']:.2f}
                        """)