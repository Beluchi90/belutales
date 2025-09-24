# PayPal Integration Setup Guide for BeluTales

## Overview
BeluTales now includes PayPal integration for premium story purchases. Users can unlock premium content for $9.99/month with secure PayPal payments.

## 🚀 Setup Instructions

### 1. Get PayPal Credentials

#### For Testing (Sandbox):
1. Go to [PayPal Developer](https://developer.paypal.com/)
2. Login or create a developer account
3. Go to "My Apps & Credentials"
4. Create a new app in **Sandbox** environment
5. Copy your **Client ID** and **Secret**

#### For Production (Live):
1. Create an app in **Live** environment
2. Copy your **Live Client ID** and **Secret**

### 2. Configure BeluTales

Edit `paypal_integration.py`:

```python
# PayPal Configuration
PAYPAL_CLIENT_ID = "YOUR_ACTUAL_PAYPAL_CLIENT_ID"  # Replace with your Client ID
PAYPAL_ENVIRONMENT = "sandbox"  # Change to "production" for live
PREMIUM_PRICE = "9.99"  # USD price for premium access
```

### 3. Test the Integration

1. **Start BeluTales:**
   ```bash
   streamlit run app.py
   ```

2. **Find a Premium Story:**
   - Look for stories with 🔒 icon in the list
   - Click on a premium story

3. **Test PayPal Payment:**
   - You'll see the premium unlock page
   - Click the PayPal button
   - Use sandbox test credentials to complete payment

#### PayPal Sandbox Test Accounts:
- **Email:** sb-buyer@personal.example.com
- **Password:** password123
- **Card:** 4111 1111 1111 1111

### 4. Premium Features

Once payment is successful:
- ✅ **Access to all premium stories**
- ✅ **30-day access period**
- ✅ **Premium status in settings**
- ✅ **Payment persistence**

## 🎯 How It Works

### User Experience:
1. User clicks on premium story (🔒)
2. Sees premium unlock page with benefits
3. Clicks PayPal button
4. Completes secure payment via PayPal
5. Automatically redirected with premium access
6. Can read all premium stories for 30 days

### Technical Flow:
1. **Payment Processing:** PayPal handles secure payment
2. **Verification:** PayPal confirms payment success
3. **Access Grant:** BeluTales unlocks premium content
4. **Persistence:** Payment stored in browser + session
5. **Expiration:** 30-day automatic expiration

## 💎 Premium Content

### Current Premium Stories:
- "The Teddy Bear's Secret Mission"
- "The Girl Who Traded Wishes" 
- Other stories marked with `"is_premium": true`

### Adding More Premium Stories:
Edit `stories.json` and add:
```json
{
  "title": "Your Story Title",
  "content": "Story content...",
  "is_premium": true,
  ...
}
```

## 🔧 Customization

### Pricing:
Change `PREMIUM_PRICE` in `paypal_integration.py`

### Access Duration:
Modify the timedelta in:
```python
st.session_state.premium_expires = datetime.now() + timedelta(days=30)  # Change days
```

### Styling:
Customize the premium unlock page in `render_premium_unlock_page()`

## 🛡️ Security Features

- ✅ **Secure PayPal Processing:** All payments via PayPal's secure API
- ✅ **Client-Side Validation:** Payment verification before access
- ✅ **Expiration Management:** Automatic premium expiry
- ✅ **Fallback Protection:** Graceful handling if PayPal unavailable

## 📊 Analytics & Tracking

### Payment Records:
Payments are saved to `payments.json` for record keeping:
```json
[
  {
    "orderID": "PAYPAL_ORDER_ID",
    "amount": "9.99",
    "currency": "USD",
    "timestamp": "2025-01-01T12:00:00Z",
    "payer_name": "Customer Name",
    "payer_email": "customer@email.com"
  }
]
```

### Premium Statistics:
Access via settings panel:
- Active premium status
- Expiration date
- Total payments processed

## 🎨 UI Components

### Premium Story Indicators:
- 🔒 **Lock icon** in story list
- **"Premium"** badge on story cards
- **Gold styling** for premium content

### Unlock Page Features:
- 🔒 **Large lock visual**
- 💎 **Premium benefits showcase**
- 💳 **Secure PayPal button**
- 🎭 **Demo access** (for testing)

## 🚨 Troubleshooting

### Common Issues:

#### PayPal Button Not Showing:
- Check internet connection
- Verify `PAYPAL_CLIENT_ID` is correct
- Ensure PayPal SDK loads (check browser console)

#### Payment Not Processing:
- Check PayPal sandbox vs live environment
- Verify test account credentials
- Check browser popup blockers

#### Premium Not Unlocking:
- Refresh the page after payment
- Check browser local storage for payment data
- Verify payment success in PayPal dashboard

### Debug Mode:
Enable console logging in `paypal_integration.py`:
```javascript
console.log('Payment data:', paymentData);
```

## 🔄 Migration from Current System

If upgrading from the placeholder system:
1. **Backup existing data**
2. **Update `paypal_integration.py` with your credentials**
3. **Test in sandbox environment**
4. **Deploy to production when ready**

## 📞 Support

For PayPal integration issues:
- Check PayPal Developer Documentation
- Use PayPal's sandbox testing tools
- Monitor browser console for JavaScript errors

For BeluTales integration:
- Check `payments.json` for payment records
- Verify premium story data in `stories.json`
- Test demo access feature first

---

**Ready to monetize your magical stories! 🌟💰**

