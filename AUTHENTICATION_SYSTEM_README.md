# BeluTales Authentication System

## Overview
BeluTales now includes a complete login/signup system with SQLite database integration. Users can create accounts, log in, and have their premium status permanently saved to the database.

## Features

### 🔐 **User Authentication**
- **Signup**: Create new accounts with email and password
- **Login**: Secure authentication with password verification
- **Logout**: Clean session termination
- **Password Security**: Hashed passwords using Werkzeug security

### 💾 **Database Storage**
- **SQLite Database**: `belutales.db` with users table
- **User Data**: ID, email, password hash, premium status, creation timestamp
- **Permanent Storage**: User accounts and premium status persist across sessions

### 💎 **Premium Integration**
- **Database Premium**: Premium status saved to user's database record
- **Automatic Unlock**: Premium status restored on login
- **PayPal Integration**: Payment updates database for logged-in users
- **Fallback System**: JSON file storage for non-logged-in users

### 🎨 **User Interface**
- **Navigation Tabs**: Stories | Login | Sign Up
- **User Info**: Welcome message and logout button
- **Premium Badge**: Visual indicator for premium users
- **Authentication Gates**: Login required for premium stories

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    premium BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## User Flow

### 1. **New User Journey**
1. Visit BeluTales → See Stories tab
2. Click "Sign Up" tab → Create account
3. Enter email/password → Account created
4. Click "Login" tab → Sign in
5. Access free stories immediately
6. Click premium story → Login required message
7. Pay with PayPal → Premium unlocked in database
8. Access all premium stories

### 2. **Returning User Journey**
1. Visit BeluTales → Auto-login check
2. If logged in → Premium status restored
3. If not logged in → Click "Login" tab
4. Enter credentials → Premium status restored
5. Access all unlocked content

### 3. **Premium Story Access**
- **Not Logged In**: Shows login/signup buttons
- **Logged In + No Premium**: Shows PayPal payment button
- **Logged In + Premium**: Shows story content directly

## Technical Implementation

### **Database Functions**
```python
def init_database()                    # Initialize SQLite database
def create_user(email, password)       # Create new user account
def authenticate_user(email, password) # Verify login credentials
def update_user_premium(user_id, status) # Update premium status
def get_user_by_id(user_id)           # Get user information
def is_user_logged_in()               # Check login status
def get_current_user()                # Get current user data
def logout_user()                     # Clear session data
```

### **UI Components**
```python
def render_login_page()    # Login form with email/password
def render_signup_page()   # Signup form with validation
def render_header()        # Navigation tabs and user info
```

### **Integration Points**
- **PayPal Capture**: Updates database for logged-in users
- **Startup Logic**: Checks database for premium status
- **Story Gating**: Requires login for premium stories
- **Session Management**: Maintains user state across pages

## Security Features

### **Password Security**
- **Hashing**: Werkzeug's `generate_password_hash()`
- **Verification**: `check_password_hash()` for login
- **No Plain Text**: Passwords never stored in plain text

### **Session Security**
- **Session State**: User ID stored in `st.session_state`
- **Logout**: Complete session cleanup
- **Validation**: All database operations validated

### **Data Protection**
- **SQL Injection**: Parameterized queries prevent SQL injection
- **Error Handling**: Graceful error handling for all operations
- **Input Validation**: Email format and password length validation

## File Structure

```
belutales/
├── app.py                    # Main app with authentication
├── belutales.db             # SQLite database (auto-created)
├── payments.json            # Fallback for non-logged-in users
├── requirements.txt         # Updated with werkzeug
└── AUTHENTICATION_SYSTEM_README.md
```

## Configuration

### **Dependencies Added**
```
werkzeug  # Password hashing and security
```

### **Database File**
- **Location**: `belutales.db` in app root
- **Auto-created**: On first app run
- **Backup**: Include in version control for production

## Usage Examples

### **Creating a User**
```python
success, result = create_user("user@example.com", "password123")
if success:
    user_id = result
    print(f"User created with ID: {user_id}")
```

### **Authenticating a User**
```python
success, result = authenticate_user("user@example.com", "password123")
if success:
    user_id = result["user_id"]
    premium = result["premium"]
    print(f"User {user_id} logged in, premium: {premium}")
```

### **Updating Premium Status**
```python
success = update_user_premium(user_id, True)
if success:
    print("Premium status updated")
```

## Error Handling

### **Common Errors**
- **User Already Exists**: Signup with existing email
- **Invalid Credentials**: Wrong email/password combination
- **Database Errors**: Connection or query failures
- **Validation Errors**: Invalid email format or weak password

### **Error Messages**
- User-friendly error messages in UI
- Detailed error logging for debugging
- Graceful fallbacks for all operations

## Future Enhancements

### **Planned Features**
- **Password Reset**: Email-based password recovery
- **User Profiles**: Extended user information
- **Admin Panel**: User management interface
- **Session Timeout**: Automatic logout after inactivity
- **Two-Factor Auth**: Additional security layer

### **Database Improvements**
- **User Roles**: Admin, premium, free user levels
- **Payment History**: Track all transactions
- **Usage Analytics**: User behavior tracking
- **Data Encryption**: Encrypt sensitive data

## Testing

### **Test Coverage**
- ✅ Database initialization
- ✅ User creation and validation
- ✅ Authentication and authorization
- ✅ Premium status management
- ✅ Error handling and edge cases
- ✅ UI component rendering

### **Test Results**
All authentication tests pass successfully, confirming:
- Database operations work correctly
- Password hashing is secure
- User authentication is reliable
- Premium status updates properly
- Error handling is robust

## Production Considerations

### **Security**
- Use HTTPS in production
- Implement rate limiting for login attempts
- Add password complexity requirements
- Regular security audits

### **Performance**
- Database connection pooling
- Caching for frequent queries
- Index optimization
- Regular database maintenance

### **Monitoring**
- Log authentication attempts
- Monitor failed login attempts
- Track premium conversions
- Database performance metrics

The authentication system is now fully integrated and ready for production use!
