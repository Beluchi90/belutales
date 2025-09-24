"""
PayPal Integration for BeluTales Premium Stories
Updated to use FastAPI backend
"""
from dotenv import load_dotenv
import os
load_dotenv()

import streamlit as st
import json
import time
import requests
from datetime import datetime, timedelta

# Configuration
BACKEND_URL = "http://localhost:8000"  # Update to your backend URL in production
PREMIUM_PRICE = "9.99"  # USD price for premium access

# Debug logging for PayPal environment variables
print("PayPal ENV:", os.getenv("PAYPAL_ENV", "sandbox"))
print("PayPal Client ID loaded:", bool(os.getenv("PAYPAL_CLIENT_ID")))
print("PayPal Secret loaded:", bool(os.getenv("PAYPAL_SECRET")))

def init_paypal_session():
    """Initialize PayPal session state"""
    if "paypal_payments" not in st.session_state:
        st.session_state.paypal_payments = {}
    if "premium_unlocked" not in st.session_state:
        st.session_state.premium_unlocked = False
    if "premium_expires" not in st.session_state:
        st.session_state.premium_expires = None

def is_premium_active():
    """Check if premium access is currently active"""
    if not st.session_state.premium_unlocked:
        return False
    
    if st.session_state.premium_expires:
        return datetime.now() < st.session_state.premium_expires
    
    return True

def create_paypal_button(story_title="Premium Stories"):
    """Create PayPal payment button using Streamlit and backend API"""
    
    # Inject enhanced PayPal button styling
    st.markdown("""
    <style>
    /* Enhanced PayPal Button Styling for Premium Paywall */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        width: 320px !important;
        height: 70px !important;
        border-radius: 35px !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        font-family: "Baloo 2", "Comic Neue", sans-serif !important;
        border: none !important;
        padding: 20px 40px !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.5), 0 0 25px rgba(118, 75, 162, 0.4), 0 0 40px rgba(255, 215, 0, 0.2) !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3) !important;
        letter-spacing: 0.5px !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button[kind="primary"]:before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent) !important;
        transition: left 0.5s !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: scale(1.05) !important;
        background: linear-gradient(135deg, #7c8ef0, #8a5fb8) !important;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.7), 0 0 35px rgba(118, 75, 162, 0.6), 0 0 50px rgba(255, 215, 0, 0.3) !important;
        text-shadow: 0 2px 6px rgba(0,0,0,0.4) !important;
    }
    
    .stButton > button[kind="primary"]:hover:before {
        left: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create a simple Streamlit button instead of JavaScript SDK
    st.markdown('<div class="belu-single-button-container">', unsafe_allow_html=True)
    
    if st.button("💳 Pay with PayPal", key="paypal_payment_btn", use_container_width=False, type="primary"):
            # Make POST request to backend to create order
            try:
                import requests
                
                # Prepare the request payload
                payload = {
                    "amount": PREMIUM_PRICE,
                    "currency": "USD", 
                    "description": f"BeluTales Premium Access - {story_title}"
                }
                
                # Make request to backend
                response = requests.post(
                    f"{BACKEND_URL}/paypal/create-order",
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Store order_id in session state for later capture
                    order_id = data.get("order_id")
                    if order_id:
                        st.session_state["paypal_order_id"] = order_id
                    
                    # Extract the approve link from the response
                    links = data.get("links", [])
                    approve_url = None
                    
                    for link in links:
                        if link.get("rel") == "approve":
                            approve_url = link.get("href")
                            break
                    
                    if approve_url:
                        # Automatically open PayPal approval URL in browser
                        import webbrowser
                        webbrowser.open(approve_url)
                        
                        st.success("🔄 Redirecting to PayPal... Please complete your payment in the new window.")
                        st.info("After payment, you'll be redirected back to BeluTales with premium access!")
                        
                    else:
                        st.error("❌ Failed to get PayPal approval URL. Please try again.")
                        
                else:
                    st.error(f"❌ Backend error: {response.status_code} - {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to payment service. Please ensure the backend server is running.")
                st.code("To start the backend: uvicorn server:app --reload")
                
            except requests.exceptions.Timeout:
                st.error("❌ Payment service timeout. Please try again.")
                
            except Exception as e:
                st.error(f"❌ Payment error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    return ""  # No HTML to return since we're using Streamlit buttons

def render_premium_unlock_page(story):
    """Render the premium unlock page with PayPal integration"""
    
    # Check if premium is already active
    if st.session_state.get("premium", False):
        st.markdown("""
        <div style="text-align: center; padding: 40px 20px; background: linear-gradient(135deg, #1e1b4b, #312e81); border-radius: 20px; margin: 20px 0;">
            <div style="font-size: 4rem; margin-bottom: 20px;">💎</div>
            <h2 style="color: #facc15; font-family: 'Baloo 2', cursive; font-weight: 800; margin-bottom: 10px;">
                Premium Story Unlocked
            </h2>
            <h3 style="color: white; margin-bottom: 30px;">
                {0}
            </h3>
            <p style="color: #d1d5db; font-size: 1.2rem; margin-bottom: 30px; max-width: 600px; margin-left: auto; margin-right: auto;">
                You have premium access! Enjoy this magical story and all premium content.
            </p>
        </div>
        """.format(story.get("title", "")), unsafe_allow_html=True)
        
        # Show back button only - centered
        st.markdown('<div class="belu-single-button-container">', unsafe_allow_html=True)
        if st.button("🏠 Back to Stories", key="premium_active_back_btn", type="secondary", use_container_width=False):
            st.session_state.view_mode = "list"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    st.markdown("""
    <div style="text-align: center; padding: 50px 30px; background: linear-gradient(135deg, #1e1b4b, #312e81); border-radius: 25px; margin: 30px 0; box-shadow: 0 20px 40px rgba(0,0,0,0.3);">
        <div style="font-size: 5rem; margin-bottom: 25px;">💎</div>
        <h1 style="color: #facc15; font-family: 'Baloo 2', cursive; font-weight: 800; margin-bottom: 15px; font-size: 2.5rem;">
            ✨ Premium Story
        </h1>
        <h2 style="color: white; margin-bottom: 20px; font-size: 1.5rem; font-weight: 400;">
            {0}
        </h2>
        <p style="color: #d1d5db; font-size: 1.3rem; margin-bottom: 25px; max-width: 700px; margin-left: auto; margin-right: auto; line-height: 1.6;">
            This magical story is part of our premium collection.
        </p>
        <p style="color: #facc15; font-size: 1.4rem; margin-bottom: 35px; max-width: 700px; margin-left: auto; margin-right: auto; line-height: 1.6; font-weight: 600;">
            Unlock all 100+ stories, quizzes, and narrations forever with a one-time payment of just <strong>${1}</strong>!
        </p>
    </div>
    """.format(story.get("title", ""), PREMIUM_PRICE), unsafe_allow_html=True)
    
    # PayPal payment section - directly under the main banner
    
    # Check if backend is available and render PayPal button
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=5)
        if response.status_code == 200:
            # Render PayPal button (now using native Streamlit button)
            create_paypal_button(story.get("title", ""))
            
            # Add reassuring message directly below the button
            st.markdown("""
            <div style="text-align: center; margin: 15px 0 30px 0;">
                <p style="color: #94a3b8; font-size: 0.9rem; font-style: italic; margin: 0;">
                    ✔ One-time payment, lifetime access, 7-day money-back guarantee.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Payment service is currently unavailable. Please try again later.")
    except requests.exceptions.RequestException:
        st.error("Cannot connect to payment service. Please ensure the backend server is running.")
        st.code("To start the backend: uvicorn server:app --reload")

def check_payment_status():
    """Check and process payment status - simplified for Streamlit native approach"""
    # This function is kept for compatibility but simplified
    # The payment flow now uses direct backend communication
    pass

def process_payment(payment_data):
    """Process successful payment"""
    try:
        # Store payment in session state
        st.session_state.paypal_payments[payment_data.get('orderID')] = payment_data
        
        # Activate premium access for this session
        st.session_state.premium_unlocked = True
        st.session_state.premium_expires = datetime.now() + timedelta(hours=24)  # 24-hour session
        
        return True
    except Exception as e:
        st.error(f"Error processing payment: {e}")
        return False

def get_premium_stats():
    """Get premium access statistics"""
    try:
        active = is_premium_active()
        expires = st.session_state.premium_expires
        
        return {
            "active": active,
            "expires": expires.strftime("%Y-%m-%d %H:%M:%S") if expires else None,
            "payments_count": len(st.session_state.paypal_payments)
        }
    except:
        return {"active": False, "expires": None, "payments_count": 0}