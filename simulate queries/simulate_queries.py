import csv
from app_logic import generate_gpt_recommendations, extract_techniques_and_keywords, fetch_youtube_videos, rank_videos_by_query


user_queries = [
                
    "Ways to calm the mind after a stressful day",
    "Simple ways to feel more grounded",
    "How to achieve mental clarity",
    "Techniques to improve emotional resilience",
    "Tips for unwinding before bedtime",
    "How to reduce racing thoughts in the evening",
    "Daily habits to maintain inner peace",
    "Effective ways to relax after work",
    "Strategies to improve focus without distractions",
    "Ways to feel more present in daily life",
    "How to deal with a restless mind",
    "Simple steps to ease physical tension",
    "Techniques to quiet negative thoughts",
    "Tips for cultivating patience during stressful times",
    "How to center yourself during chaos",
    "Practices to develop self-awareness",
    "Steps to improve body-mind connection",
    "Tips for enhancing overall relaxation",
    "How to improve posture while sitting for long hours",
    "Strategies to reduce physical and mental fatigue",
    "Methods for slowing down a fast-paced life",
    "How to build a calming evening routine",
    "Ways to feel more in tune with your body",
    "How to create a sense of inner stillness",
    "Practical steps to improve mental health at home",
    "How to connect with your inner self",
    "Tips for recovering from burnout",
    "How to release pent-up energy effectively",
    "How to develop a positive mindset daily",
    "Practical ways to detach from digital distractions",
    "How to feel more at ease in social situations",
    "Tips for creating a tranquil home environment",
    "How to slow down your thoughts before bed",
    "How to feel refreshed during the day",
    "Ways to overcome decision-making fatigue",
    "Practical ways to enhance self-reflection",
    "How to embrace moments of stillness",
    "Steps to build resilience to daily stressors",
    "Tips for reducing overwhelm during a busy week",
    "How to find balance during challenging times",
    "Simple ways to encourage deeper relaxation",
    "Techniques to feel more present in conversations",
    "How to create a personal space for quiet time",
    "Steps to improve connection with your physical self",
    "How to transition to a peaceful state after arguments",
    "Tips for finding joy in everyday tasks",
    "Steps to stay calm in overwhelming environments",
    "Ways to develop a mindful morning routine",
    "How to foster gratitude during tough days",
    "Tips for building small moments of calm into my day"
]
# Predefined queries
user_queries = [
                
    "Ways to calm the mind after a stressful day",
    "Simple ways to feel more grounded",
]


# Log results into a CSV file
def simulate_queries_and_log_results(queries, categories, output_file="simulation_results.csv"):
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Query ID", "Query", "Category", "Technique", "Description", "Keywords", "Video Title", "Video Description", "Similarity Score", "Video Link"])

        query_id = 1
        
        for query in queries:
            for category in ["All"] + list(categories.keys()):  # Iterate over all categories, including "All"
                print(f"Processing Query ID {query_id}: '{query}' for Category: '{category}'")
                
                gpt_recommendations = generate_gpt_recommendations(query, category)
                print(f"GPT Recommendations: {gpt_recommendations}")
                techniques_with_details = extract_techniques_and_keywords(gpt_recommendations)
                print(f"Extracted Techniques: {techniques_with_details}")

                for technique_data in techniques_with_details:
                    technique = technique_data["technique"]
                    description = technique_data["description"]
                    enriched_query = " ".join([technique] + technique_data["keywords"])
                    print(f"Enriched Query: {enriched_query}")
                    
                    videos = fetch_youtube_videos(
                        enriched_query,
                        max_results=3,
                        order="relevance",  # Fetch the most-viewed videos
                        video_duration="medium",  # Fetch videos between 4 and 20 minutes
                        video_definition="high"  # Fetch only high-definition videos
                    )
                    print(f"Fetched Videos: {videos}")
                    
                    if not videos:
                        print(f"No videos found for query: {enriched_query}")
                        continue
                        
                    ranked_videos = rank_videos_by_query(enriched_query, videos)
                    print(f"Ranked Videos: {ranked_videos[:5]}")

                    for video in ranked_videos[:5]:  # Log top 5 videos per technique
                        writer.writerow([
                            query_id,
                            query,
                            category,
                            technique,
                            description,
                            " ".join(technique_data["keywords"]),
                            video["title"],
                            video["description"],
                            video.get("similarity_score", 0.0),
                            video["link"]
                        ])
            query_id += 1  # Increment the Query ID for the next query

# Run the simulation
if __name__ == "__main__":
    simulate_queries_and_log_results(user_queries, categories)