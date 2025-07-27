import streamlit as st
import google.generativeai as genai
from datetime import datetime
import json
import os

# Configure page
st.set_page_config(
    page_title="✨ Wall-E AI Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for flashy UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* Custom gradient background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Main content area styling */
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 0 20px 20px 0;
    }
    
    /* Title styling */
    .main-title {
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Chat message styling */
    .stChatMessage {
        border-radius: 15px;
        margin: 1rem 0;
        padding: 1rem;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* User message styling */
    .stChatMessage[data-testid="user-message"] {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
    }
    
    /* Assistant message styling */
    .stChatMessage[data-testid="assistant-message"] {
        background: linear-gradient(135deg, #f093fb, #f5576c);
        color: white;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    /* New chat button special styling */
    .new-chat-btn {
        background: linear-gradient(45deg, #00c851, #007e33) !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
    }
    
    /* Chat history buttons */
    .chat-history-btn {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        color: white !important;
        margin: 0.25rem 0 !important;
        text-align: left !important;
        font-size: 0.9rem !important;
    }
    
    .chat-history-btn:hover {
        background: rgba(255, 255, 255, 0.2) !important;
        transform: translateX(5px) !important;
    }
    
    /* Delete button styling */
    .delete-btn {
        background: linear-gradient(45deg, #ff4757, #ff3838) !important;
        color: white !important;
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        padding: 0 !important;
        font-size: 1.2rem !important;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid transparent;
        border-radius: 15px;
        padding: 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
        background: white;
    }
    
    /* Chat input styling */
    .stChatInputContainer {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 25px;
        padding: 0.5rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }
    
    /* Sidebar title styling */
    .sidebar-title {
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Stats styling */
    .stats-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        color: white;
        text-align: center;
    }
    
    /* Warning and info box styling */
    .stAlert {
        border-radius: 15px;
        border: none;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Loading spinner custom */
    .stSpinner {
        text-align: center;
    }
    
    /* Custom emoji animations */
    .rotating-emoji {
        animation: rotate 2s linear infinite;
        display: inline-block;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    /* Pulse animation for new messages */
    .pulse {
        animation: pulse 1s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(45deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
        border-radius: 15px;
        margin-top: 2rem;
        color: #666;
        font-style: italic;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_sessions' not in st.session_state:
    st.session_state.chat_sessions = {}
if 'current_session_id' not in st.session_state:
    st.session_state.current_session_id = None
if 'gemini_api_key' not in st.session_state:
    st.session_state.gemini_api_key = "AIzaSyDlUN9wJ_Vvj5kCxC-YO-nRTtUHNeeHztg"

def create_new_session():
    """Create a new chat session"""
    session_id = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    st.session_state.chat_sessions[session_id] = {
        'messages': [],
        'title': f"✨ Chat {len(st.session_state.chat_sessions) + 1}",
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M')
    }
    st.session_state.current_session_id = session_id
    return session_id

def get_chat_title(messages):
    """Generate a title for the chat based on first message"""
    if messages:
        first_msg = messages[0]['content'][:40]
        return f"💬 {first_msg}..." if len(first_msg) > 37 else f"💬 {first_msg}"
    return "✨ New Chat"

def configure_gemini(api_key):
    """Configure Gemini API"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model
    except Exception as e:
        st.error(f"🚨 Error configuring API: {str(e)}")
        return None

# Sidebar with enhanced styling
with st.sidebar:
    st.markdown('<h1 class="sidebar-title">🤖 Wall-E AI Chat</h1>', unsafe_allow_html=True)
    
    # Show API connection status
    if st.session_state.gemini_api_key:
        st.success("🎉 API Key Connected!")
    
    st.markdown("---")
    
    # Enhanced New Chat button
    if st.button("🚀 Start New Chat", use_container_width=True, key="new_chat"):
        create_new_session()
        st.balloons()  # Fun animation!
        st.rerun()
    
    st.markdown("---")
    
    # Chat History with better styling
    st.markdown("### 📚 Chat History")
    
    if st.session_state.chat_sessions:
        for i, (session_id, session_data) in enumerate(reversed(list(st.session_state.chat_sessions.items()))):
            # Update title based on messages
            if session_data['messages']:
                session_data['title'] = get_chat_title(session_data['messages'])
            
            # Create columns for chat button and delete button
            col1, col2 = st.columns([4, 1])
            
            with col1:
                # Chat session button with enhanced styling
                button_text = f"{session_data['title']}\n📅 {session_data['created_at']}"
                
                if st.button(
                    button_text,
                    key=f"chat_{session_id}",
                    use_container_width=True,
                    help=f"Switch to {session_data['title']}"
                ):
                    st.session_state.current_session_id = session_id
                    st.success(f"🎯 Switched to {session_data['title']}")
                    st.rerun()
            
            with col2:
                # Delete button with confirmation
                if st.button("🗑️", key=f"delete_{session_id}", help="Delete this chat"):
                    del st.session_state.chat_sessions[session_id]
                    if st.session_state.current_session_id == session_id:
                        if st.session_state.chat_sessions:
                            st.session_state.current_session_id = list(st.session_state.chat_sessions.keys())[-1]
                        else:
                            st.session_state.current_session_id = None
                    st.success("🗑️ Chat deleted!")
                    st.rerun()
            
            if i < len(st.session_state.chat_sessions) - 1:
                st.markdown("---")
    else:
        st.markdown("""
        <div style='text-align: center; color: white; padding: 1rem;'>
            <h3>🌟 No chats yet!</h3>
            <p>Start your first conversation above</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Clear all history with confirmation
    st.markdown("")
    if st.button("🧹 Clear All History", use_container_width=True):
        st.session_state.chat_sessions = {}
        st.session_state.current_session_id = None
        st.success("✨ All history cleared!")
        st.snow()  # Fun animation!
        st.rerun()

    # Enhanced statistics
    if st.session_state.chat_sessions:
        current_session = st.session_state.chat_sessions.get(st.session_state.current_session_id, {})
        msg_count = len(current_session.get('messages', []))
        total_chats = len(st.session_state.chat_sessions)
        
        st.markdown(f"""
        <div class="stats-container">
            <h4>📊 Statistics</h4>
            <p><strong>💬 Current Chat:</strong> {msg_count} messages</p>
            <p><strong>📱 Total Chats:</strong> {total_chats}</p>
            <p><strong>🕒 Session:</strong> Active</p>
        </div>
        """, unsafe_allow_html=True)

# Main content area with enhanced styling
st.markdown('<h1 class="main-title">✨ Wall-E AI Assistant</h1>', unsafe_allow_html=True)

# Check if API key is provided
if not st.session_state.gemini_api_key:
    st.markdown("""
    <div style='text-align: center; padding: 3rem; background: linear-gradient(135deg, #ff9a9e, #fecfef); border-radius: 20px; color: white;'>
        <h2>🔑 API Key Required</h2>
        <p style='font-size: 1.2rem;'>Please provide an API key to start chatting!</p>
        <p><a href='https://makersuite.google.com/app/apikey' target='_blank' style='color: white; text-decoration: underline;'>🔗 Get your API key here</a></p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Configure Gemini model
model = configure_gemini(st.session_state.gemini_api_key)
if not model:
    st.stop()

# Create first session if none exists
if not st.session_state.chat_sessions:
    create_new_session()

# Get current session
current_session = st.session_state.chat_sessions.get(st.session_state.current_session_id)
if not current_session:
    create_new_session()
    current_session = st.session_state.chat_sessions[st.session_state.current_session_id]

# Display current chat info with better styling
if current_session:
    st.markdown(f"""
    <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)); border-radius: 15px; margin-bottom: 2rem;'>
        <h3 style='color: #667eea; margin: 0;'>💬 {current_session['title']}</h3>
        <p style='color: #666; margin: 0.5rem 0 0 0;'>📅 Started: {current_session['created_at']}</p>
    </div>
    """, unsafe_allow_html=True)

# Display chat messages with enhanced styling
if current_session['messages']:
    for i, message in enumerate(current_session['messages']):
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                st.markdown(f"👤 **You:** {message['content']}")
            else:
                st.markdown(f"🤖 **Wall-E:** {message['content']}")
else:
    # Welcome message for new chats
    st.markdown("""
    <div style='text-align: center; padding: 3rem; background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)); border-radius: 20px; margin: 2rem 0;'>
        <h2 style='color: #667eea;'>🎉 Welcome to Wall-E AI Chat!</h2>
        <p style='font-size: 1.2rem; color: #666;'>Start a conversation by typing your message below</p>
        <div style='font-size: 2rem; margin: 1rem 0;'>🤖✨💬🚀</div>
    </div>
    """, unsafe_allow_html=True)

# Enhanced chat input
if prompt := st.chat_input("✨ Type your message here... Ask me anything!", key="chat_input"):
    # Add user message to current session
    current_session['messages'].append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(f"👤 **You:** {prompt}")
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("🤖 Wall-E is thinking..."):
            try:
                # Create chat history for context
                chat_history = []
                for msg in current_session['messages'][:-1]:  # Exclude the current message
                    chat_history.append({
                        'role': 'user' if msg['role'] == 'user' else 'model',
                        'parts': [msg['content']]
                    })
                
                # Start chat with history
                chat = model.start_chat(history=chat_history)
                response = chat.send_message(prompt)
                
                # Display response with typing animation effect
                response_text = response.text
                st.markdown(f"🤖 **Wall-E:** {response_text}")
                
                # Add assistant response to current session
                current_session['messages'].append({"role": "assistant", "content": response_text})
                
                # Show success animation
                if len(current_session['messages']) == 2:  # First response
                    st.balloons()
                
            except Exception as e:
                error_msg = f"🚨 Error: {str(e)}"
                st.error(error_msg)
                current_session['messages'].append({"role": "assistant", "content": error_msg})
