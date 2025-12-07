"""
Streamlit Web UI for Agent Chatbot
Allows users to input their API key and chat with the agent through a web interface.
"""

import streamlit as st
import asyncio
import json
import os
from datetime import datetime
from agent import (
    get_agent,
    add_to_chat_history,
    get_chat_history,
    clear_chat_history,
    pulse_button,
    OWNER_ADDRESS
)

# Page configuration
st.set_page_config(
    page_title="Agent Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: 20%;
    }
    .assistant-message {
        background-color: #f5f5f5;
        margin-right: 20%;
    }
    .stButton>button {
        width: 100%;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = None
if "api_key_set" not in st.session_state:
    st.session_state.api_key_set = False
if "chat_history_loaded" not in st.session_state:
    st.session_state.chat_history_loaded = False

def load_chat_history_to_session():
    """Load chat history from agent module to session state."""
    if not st.session_state.chat_history_loaded:
        history = get_chat_history()
        st.session_state.messages = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "assistant"
            st.session_state.messages.append({
                "role": role,
                "content": msg["content"]
            })
        st.session_state.chat_history_loaded = True

def initialize_agent(api_key: str, model_id: str = "gpt-4o-mini"):
    """Initialize the agent with the provided API key."""
    try:
        agent = get_agent(api_key=api_key, model_id=model_id)
        st.session_state.agent = agent
        st.session_state.api_key_set = True
        return True
    except Exception as e:
        st.error(f"Error initializing agent: {str(e)}")
        return False

# Sidebar for API key and settings
with st.sidebar:
    st.title("⚙️ Settings")
    
    # API Key Input
    st.subheader("🔑 API Key")
    api_key = st.text_input(
        "Enter your OpenAI API Key",
        type="password",
        placeholder="sk-...",
        help="Enter your OpenAI API key to start chatting with the agent."
    )
    
    # Model selection
    model_id = st.selectbox(
        "Select Model",
        ["gpt-4o-mini", "gpt-4o", "gpt-4", "gpt-3.5-turbo"],
        index=0,
        help="Choose the OpenAI model to use"
    )
    
    # Initialize button
    if st.button("🚀 Initialize Agent", use_container_width=True):
        if api_key:
            with st.spinner("Initializing agent..."):
                if initialize_agent(api_key, model_id):
                    st.success("✅ Agent initialized successfully!")
                    st.rerun()
        else:
            st.warning("⚠️ Please enter your API key first")
    
    # Status
    st.divider()
    st.subheader("📊 Status")
    if st.session_state.api_key_set:
        st.success("✅ Agent Ready")
        st.info(f"🤖 Model: {model_id}")
    else:
        st.warning("⚠️ Agent Not Initialized")
    
    # Owner address info
    st.divider()
    st.subheader("🔐 Contract Info")
    st.code(OWNER_ADDRESS, language=None)
    st.caption("Hard-coded owner address for ERC721 contracts")
    
    # Actions
    st.divider()
    st.subheader("🛠️ Actions")
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        clear_chat_history()
        st.session_state.messages = []
        st.session_state.chat_history_loaded = False
        st.success("Chat history cleared!")
        st.rerun()
    
    # Pulse button
    if st.button("🔘 Generate ERC721 Contract", use_container_width=True, type="primary"):
        if st.session_state.api_key_set:
            with st.spinner("Generating ERC721 contract..."):
                result = pulse_button()
                st.success("✅ Contract generated!")
                st.info(result)
        else:
            st.warning("⚠️ Please initialize the agent first")

# Main content area
st.markdown('<div class="main-header">🤖 Agent Chatbot</div>', unsafe_allow_html=True)

# Load chat history if agent is initialized
if st.session_state.api_key_set:
    load_chat_history_to_session()

# Display chat messages
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input
if st.session_state.api_key_set:
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        add_to_chat_history("user", prompt)
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Run agent asynchronously
                    # Handle event loop for Streamlit compatibility
                    try:
                        loop = asyncio.get_event_loop()
                        if loop.is_running():
                            # Use nest_asyncio if loop is already running
                            import nest_asyncio
                            nest_asyncio.apply()
                            response = asyncio.run(st.session_state.agent.run(prompt))
                        else:
                            response = loop.run_until_complete(
                                st.session_state.agent.run(prompt)
                            )
                    except RuntimeError:
                        # No event loop exists, create one
                        response = asyncio.run(st.session_state.agent.run(prompt))
                    
                    st.markdown(response)
                    
                    # Add assistant response to chat
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    add_to_chat_history("assistant", response)
                    
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
else:
    st.info("👆 Please enter your API key in the sidebar and click 'Initialize Agent' to start chatting.")

# Footer
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption(f"💬 Messages: {len(st.session_state.messages)}")
with col2:
    if st.session_state.api_key_set:
        st.caption("✅ Agent Active")
    else:
        st.caption("⚠️ Agent Inactive")
with col3:
    st.caption(f"🔐 Owner: {OWNER_ADDRESS[:10]}...")

