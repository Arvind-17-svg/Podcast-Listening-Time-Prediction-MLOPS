import streamlit as st
import requests
import json

# Page configuration
st.set_page_config(
    page_title="Podcast Listening Time Predictor",
    page_icon="🎧",
    layout="wide"
)

# API endpoint
API_URL = "http://127.0.0.1:5000/predict"

st.title("🎧 Podcast Listening Time Prediction")
st.write("Enter the podcast details to predict how long listeners will engage with your episode.")

# Create two columns for better layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Episode Information")
    podcast_name = st.text_input("Podcast Name", key="podcast_name", placeholder="e.g., Tech Talk Today")
    episode_title = st.text_input("Episode Title", key="episode_title", placeholder="e.g., Episode 42")
    
    # Genre selection
    genre = st.selectbox(
        "Genre", 
        options=["Comedy", "Technology", "Health", "Education", "True Crime", 
                "Business", "Sports", "News", "Entertainment", "Science", "History", "Music"],
        key="genre"
    )

with col2:
    st.subheader("📊 Publication & Popularity")
    
    # Publication details
    publication_day = st.selectbox(
        "Publication Day",
        options=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        key="publication_day"
    )
    
    publication_time = st.selectbox(
        "Publication Time",
        options=["Morning", "Afternoon", "Evening", "Night"],
        key="publication_time"
    )
    
    host_popularity = st.slider(
        "Host Popularity Percentage", 
        min_value=0.0, 
        max_value=120.0, 
        value=50.0,
        key="host_popularity",
        help="Host's popularity rating"
    )
    
    guest_popularity = st.slider(
        "Guest Popularity Percentage", 
        min_value=0.0, 
        max_value=120.0, 
        value=50.0,
        key="guest_popularity",
        help="Guest's popularity rating"
    )

# Info box about defaults
st.info("ℹ️ **Default values used**: Episode Length: 60 mins, Number of Ads: 1, Sentiment: Positive")

# Prediction section
st.markdown("---")
st.subheader("🔮 Make Prediction")

if st.button("🚀 Predict Listening Time", type="primary", use_container_width=True):
    # Validate required fields
    if not all([podcast_name, episode_title]):
        st.error("❌ Please fill in Podcast Name and Episode Title!")
    else:
        # Prepare data for API call
        prediction_data = {
            "Podcast_Name": podcast_name,
            "Episode_Title": episode_title,
            "Genre": genre,
            "Publication_Day": publication_day,
            "Publication_Time": publication_time,
            "Guest_Popularity_percentage": guest_popularity,
            "Host_Popularity_percentage": host_popularity
        }
        
        # Show loading spinner
        with st.spinner("🤖 Making prediction..."):
            try:
                # Make API call
                response = requests.post(
                    API_URL,
                    json=prediction_data,
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    predicted_time = result["Predicted_Listening_Time"]
                    
                    # Display results
                    st.success("✅ Prediction completed!")
                    
                    # Create metrics display
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(
                            label="🎯 Predicted Listening Time",
                            value=f"{predicted_time:.1f} minutes"
                        )
                    
                    with col2:
                        # Using default episode length of 60 minutes for retention calculation
                        retention_rate = (predicted_time / 60.0) * 100
                        st.metric(
                            label="📈 Retention Rate",
                            value=f"{retention_rate:.1f}%"
                        )
                    
                    with col3:
                        if retention_rate >= 70:
                            engagement = "🔥 High"
                        elif retention_rate >= 50:
                            engagement = "👍 Good"
                        else:
                            engagement = "📉 Low"
                        
                        st.metric(
                            label="💪 Engagement Level",
                            value=engagement
                        )
                    
                    # Additional insights
                    st.markdown("### 📊 Insights")
                    
                    insights = []
                    
                    if retention_rate >= 80:
                        insights.append("🎉 Excellent! This episode is predicted to have very high listener retention.")
                    elif retention_rate >= 60:
                        insights.append("👏 Good retention expected. Consider promoting this episode more heavily.")
                    else:
                        insights.append("🤔 Lower retention predicted. Consider optimizing content or format.")
                    
                    if host_popularity > guest_popularity + 20:
                        insights.append("⭐ Host popularity is significantly higher - leverage this in marketing!")
                    elif guest_popularity > host_popularity + 20:
                        insights.append("🎤 Guest popularity is high - great choice for audience engagement!")
                    
                    if genre in ["Technology", "Education", "Business"]:
                        insights.append("🧠 Educational content - consider adding actionable takeaways.")
                    elif genre in ["Comedy", "Entertainment"]:
                        insights.append("😄 Entertainment focused - ensure good pacing and energy!")
                    
                    for insight in insights:
                        st.info(insight)
                
                else:
                    st.error(f"❌ API Error: {response.status_code}")
                    try:
                        error_detail = response.json()
                        st.error(f"Details: {error_detail.get('detail', 'Unknown error')}")
                    except:
                        st.error(f"Response: {response.text}")
                        
            except requests.exceptions.ConnectionError:
                st.error("❌ Connection Error: Make sure your FastAPI server is running on http://127.0.0.1:5000")
                st.info("💡 To start the FastAPI server, run: `python your_fastapi_file.py`")
                
            except requests.exceptions.Timeout:
                st.error("❌ Request Timeout: The API took too long to respond")
                
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Request Error: {str(e)}")
                
            except json.JSONDecodeError:
                st.error("❌ Invalid response format from API")
                
            except Exception as e:
                st.error(f"❌ Unexpected Error: {str(e)}")

# Sidebar with additional info
with st.sidebar:
    st.header("ℹ️ Required Fields Only")
    st.markdown("""
    This simplified version only requires:
    - **Podcast Name** 
    - **Episode Title**
    - **Genre** (dropdown)
    - **Publication Day** (dropdown)
    - **Publication Time** (dropdown)
    - **Host Popularity** (slider)
    - **Guest Popularity** (slider)
    """)
    
    st.header("🔧 Default Values Used")
    st.markdown("""
    - **Episode Length**: 60 minutes
    - **Number of Ads**: 1
    - **Episode Sentiment**: Positive
    """)
    
    st.header("📈 Quick Tips")
    st.markdown("""
    - Higher popularity scores generally improve retention
    - Monday mornings and Tuesday evenings often perform well
    - Technology and Education genres tend to have good engagement
    """)
    
    # API status check
    st.header("🔗 API Status")
    try:
        health_response = requests.get("http://127.0.0.1:5000/health", timeout=5)
        if health_response.status_code == 200:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Issues")
    except:
        st.error("❌ API Offline")
        st.caption("Start FastAPI server first")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "🎧 Simple Podcast Predictor | Only 7 Required Fields"
    "</div>",
    unsafe_allow_html=True
)