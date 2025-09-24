"""
FastAPI Backend for BeluTales PayPal Integration
Handles PayPal payment orders, capture, and webhooks
"""

from dotenv import load_dotenv
import os
load_dotenv()

import json
import hmac
import hashlib
import logging
from typing import Dict, Any
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# PayPal Configuration from environment
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_SECRET = os.getenv("PAYPAL_SECRET")
PAYPAL_ENV = os.getenv("PAYPAL_ENV", "sandbox")

# Debug logging for PayPal environment variables
print("PayPal ENV:", PAYPAL_ENV)
print("PayPal Client ID loaded:", bool(PAYPAL_CLIENT_ID))
print("PayPal Secret loaded:", bool(PAYPAL_SECRET))

if not PAYPAL_CLIENT_ID or not PAYPAL_SECRET:
    raise ValueError("PAYPAL_CLIENT_ID and PAYPAL_SECRET must be set in environment variables")

# PayPal API URLs
PAYPAL_BASE_URL = {
    "sandbox": "https://api-m.sandbox.paypal.com",
    "live": "https://api-m.paypal.com"
}[PAYPAL_ENV]

app = FastAPI(title="BeluTales PayPal API", version="1.0.0")

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class CreateOrderRequest(BaseModel):
    amount: str = "9.99"
    currency: str = "USD"
    description: str = "BeluTales Premium Access"

class CaptureOrderRequest(BaseModel):
    order_id: str

# PayPal API helpers
async def get_paypal_access_token() -> str:
    """Get access token from PayPal"""
    url = f"{PAYPAL_BASE_URL}/v1/oauth2/token"
    
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en_US",
    }
    
    data = "grant_type=client_credentials"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers=headers,
            data=data,
            auth=(PAYPAL_CLIENT_ID, PAYPAL_SECRET)
        )
        
        if response.status_code != 200:
            logger.error(f"Failed to get PayPal access token: {response.text}")
            raise HTTPException(status_code=500, detail="Failed to authenticate with PayPal")
        
        token_data = response.json()
        return token_data["access_token"]

async def make_paypal_request(method: str, endpoint: str, data: Dict = None) -> Dict[str, Any]:
    """Make authenticated request to PayPal API"""
    access_token = await get_paypal_access_token()
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "PayPal-Request-Id": f"belutales-{datetime.now().isoformat()}"
    }
    
    url = f"{PAYPAL_BASE_URL}{endpoint}"
    
    async with httpx.AsyncClient() as client:
        if method.upper() == "POST":
            response = await client.post(url, headers=headers, json=data)
        elif method.upper() == "GET":
            response = await client.get(url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        if response.status_code not in [200, 201]:
            logger.error(f"PayPal API error: {response.status_code} - {response.text}")
            raise HTTPException(
                status_code=response.status_code,
                detail=f"PayPal API error: {response.text}"
            )
        
        return response.json()

# API Routes
@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "BeluTales PayPal API is running", "environment": PAYPAL_ENV}

@app.post("/paypal/create-order")
async def create_paypal_order(request: CreateOrderRequest):
    """Create a PayPal order for premium access"""
    try:
        order_data = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": request.currency,
                        "value": request.amount
                    },
                    "description": request.description,
                    "custom_id": f"belutales-premium-{datetime.now().timestamp()}"
                }
            ],
            "application_context": {
                # IMPORTANT: When deploying to production, replace http://localhost:8502 with your real domain
                # Example: https://belutales.com/success and https://belutales.com/cancel
                "return_url": "http://localhost:8502/success",
                "cancel_url": "http://localhost:8502/cancel",
                "brand_name": "BeluTales",
                "landing_page": "BILLING",
                "user_action": "PAY_NOW"
            }
        }
        
        result = await make_paypal_request("POST", "/v2/checkout/orders", order_data)
        
        logger.info(f"Created PayPal order: {result['id']}")
        
        return {
            "order_id": result["id"],
            "status": result["status"],
            "links": result.get("links", [])
        }
        
    except Exception as e:
        logger.error(f"Error creating PayPal order: {e}")
        raise HTTPException(status_code=500, detail="Failed to create PayPal order")

@app.post("/paypal/capture-order/{order_id}")
async def capture_paypal_order(order_id: str):
    """Capture a PayPal order after approval"""
    try:
        result = await make_paypal_request("POST", f"/v2/checkout/orders/{order_id}/capture")
        
        logger.info(f"Captured PayPal order: {order_id}")
        
        # Check if payment was successful
        if result.get("status") == "COMPLETED":
            return {
                "order_id": order_id,
                "status": "COMPLETED",
                "payer_email": result.get("payer", {}).get("email_address"),
                "amount": result.get("purchase_units", [{}])[0].get("payments", {}).get("captures", [{}])[0].get("amount", {}),
                "transaction_id": result.get("purchase_units", [{}])[0].get("payments", {}).get("captures", [{}])[0].get("id")
            }
        else:
            raise HTTPException(status_code=400, detail=f"Payment not completed. Status: {result.get('status')}")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error capturing PayPal order {order_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to capture PayPal order")

@app.post("/paypal/webhook")
async def handle_paypal_webhook(request: Request):
    """Handle PayPal webhook events"""
    try:
        # Get raw body for signature verification
        body = await request.body()
        headers = dict(request.headers)
        
        # Log webhook received
        logger.info(f"Received PayPal webhook: {headers.get('paypal-transmission-id')}")
        
        # Parse the webhook data
        webhook_data = json.loads(body.decode())
        event_type = webhook_data.get("event_type")
        resource = webhook_data.get("resource", {})
        
        logger.info(f"Webhook event type: {event_type}")
        
        # Handle different webhook events
        if event_type == "PAYMENT.CAPTURE.COMPLETED":
            # Payment was successfully captured
            order_id = resource.get("supplementary_data", {}).get("related_ids", {}).get("order_id")
            payer_email = resource.get("payer", {}).get("email_address")
            amount = resource.get("amount", {})
            
            logger.info(f"Payment completed for order {order_id}, payer: {payer_email}")
            
            # Here you would typically:
            # 1. Update your database to grant premium access
            # 2. Send confirmation email
            # 3. Log the transaction
            
            return {"status": "success", "message": "Payment completed webhook processed"}
            
        elif event_type == "PAYMENT.CAPTURE.DENIED":
            # Payment was denied
            order_id = resource.get("supplementary_data", {}).get("related_ids", {}).get("order_id")
            logger.warning(f"Payment denied for order {order_id}")
            
            return {"status": "success", "message": "Payment denied webhook processed"}
            
        elif event_type == "PAYMENT.CAPTURE.REFUNDED":
            # Payment was refunded
            order_id = resource.get("supplementary_data", {}).get("related_ids", {}).get("order_id")
            logger.info(f"Payment refunded for order {order_id}")
            
            # Here you would revoke premium access
            
            return {"status": "success", "message": "Payment refunded webhook processed"}
            
        else:
            logger.info(f"Unhandled webhook event: {event_type}")
            return {"status": "success", "message": f"Webhook event {event_type} received but not processed"}
            
    except Exception as e:
        logger.error(f"Error processing PayPal webhook: {e}")
        return {"status": "error", "message": "Failed to process webhook"}

@app.get("/paypal/order/{order_id}")
async def get_order_details(order_id: str):
    """Get details of a PayPal order"""
    try:
        result = await make_paypal_request("GET", f"/v2/checkout/orders/{order_id}")
        return result
    except Exception as e:
        logger.error(f"Error getting order details for {order_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get order details")

if __name__ == "__main__":
    import uvicorn
    
    # Run the server
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
