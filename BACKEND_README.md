# BeluTales Backend Setup Guide 🦉

This guide covers setting up the FastAPI backend for PayPal integration.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install fastapi uvicorn httpx python-dotenv
```

### 2. Configure Environment
```bash
cp env.example .env
```

Edit `.env` with your PayPal credentials:
```env
PAYPAL_CLIENT_ID=your_paypal_client_id_here
PAYPAL_SECRET=your_paypal_secret_here
PAYPAL_ENV=sandbox  # or "live" for production
```

### 3. Run the Server
```bash
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## 📋 API Documentation

Once running, visit:
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 Endpoints

### Health Check
```
GET /
```

### Create PayPal Order
```
POST /paypal/create-order
Content-Type: application/json

{
  "amount": "9.99",
  "currency": "USD",
  "description": "BeluTales Premium Access"
}
```

### Capture PayPal Order
```
POST /paypal/capture-order/{order_id}
```

### PayPal Webhook
```
POST /paypal/webhook
```

## 🚢 Deployment

### Railway
```bash
railway login
railway init
railway up
```

### Heroku
```bash
heroku create belutales-api
git push heroku main
```

### DigitalOcean App Platform
1. Connect GitHub repository
2. Set environment variables
3. Deploy

## 🔧 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `PAYPAL_CLIENT_ID` | PayPal Client ID | `AXxxx...` |
| `PAYPAL_SECRET` | PayPal Secret | `EPxxx...` |
| `PAYPAL_ENV` | Environment | `sandbox` or `live` |
| `LOG_LEVEL` | Logging level | `INFO` |

## 🔗 PayPal Webhook Setup

1. **PayPal Developer Dashboard**:
   - Go to https://developer.paypal.com/
   - Select your app
   - Add webhook URL: `https://your-api-domain.com/paypal/webhook`

2. **Subscribe to Events**:
   - `PAYMENT.CAPTURE.COMPLETED`
   - `PAYMENT.CAPTURE.DENIED`
   - `PAYMENT.CAPTURE.REFUNDED`

## 🧪 Testing

### Test Health Check
```bash
curl http://localhost:8000/
```

### Test with Streamlit
1. Update `BACKEND_URL` in `paypal_integration.py`
2. Start Streamlit: `streamlit run app.py`
3. Try to access a premium story

### PayPal Sandbox
- Use sandbox credentials for testing
- Test payments won't charge real money
- Use PayPal's test credit cards

## 🔍 Monitoring

### Logs
```bash
# Development
uvicorn server:app --log-level debug

# Production
uvicorn server:app --log-level info
```

### Health Monitoring
Set up monitoring on:
- `GET /` endpoint
- Response time < 2s
- Uptime > 99%

## 🔒 Security

- ✅ CORS configured for frontend domain
- ✅ PayPal credentials in environment variables
- ✅ Webhook signature verification (implement as needed)
- ✅ Input validation with Pydantic models

## 🐛 Troubleshooting

### Common Issues

1. **"Failed to authenticate with PayPal"**
   - Check `PAYPAL_CLIENT_ID` and `PAYPAL_SECRET`
   - Verify environment (`sandbox` vs `live`)

2. **"Cannot connect to payment service"**
   - Ensure backend is running on correct port
   - Check `BACKEND_URL` in frontend

3. **CORS errors**
   - Verify frontend domain in CORS settings
   - Check browser console for exact error

### Debug Mode
```bash
uvicorn server:app --reload --log-level debug
```

---

Need help? Check the main [MIGRATION_NOTES.md](./MIGRATION_NOTES.md) for complete setup instructions.
