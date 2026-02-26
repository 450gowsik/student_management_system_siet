"""
Quick Email Configuration Helper
Run this script to update your email credentials in app.py
"""

def configure_email():
    print("=" * 60)
    print("📧 Email Configuration Setup")
    print("=" * 60)
    print()
    print("To send email notifications, you need:")
    print("1. A Gmail account")
    print("2. An App Password (not your regular password)")
    print()
    print("How to get Gmail App Password:")
    print("1. Go to: https://myaccount.google.com/security")
    print("2. Enable 2-Step Verification (if not already enabled)")
    print("3. Go to: https://myaccount.google.com/apppasswords")
    print("4. Create an app password for 'Mail'")
    print("5. Copy the 16-character password")
    print()
    print("-" * 60)
    print()
    
    # Get user input
    sender_email = input("Enter your Gmail address: ").strip()
    sender_password = input("Enter your App Password (16 chars, no spaces): ").strip().replace(" ", "")
    
    # Validate
    if not sender_email or '@' not in sender_email:
        print("\n❌ Invalid email address!")
        return
    
    if len(sender_password) < 10:
        print("\n❌ Password seems too short. Make sure it's your App Password!")
        return
    
    # Read current app.py
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace email config
        import re
        
        # Replace sender email
        content = re.sub(
            r"'SENDER_EMAIL':\s*'[^']*'",
            f"'SENDER_EMAIL': '{sender_email}'",
            content
        )
        
        # Replace sender password
        content = re.sub(
            r"'SENDER_PASSWORD':\s*'[^']*'",
            f"'SENDER_PASSWORD': '{sender_password}'",
            content
        )
        
        # Write back
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("\n✅ Email configuration updated successfully!")
        print("\n📝 Next steps:")
        print("1. Restart your Flask application (Ctrl+C, then 'python app.py')")
        print("2. Sign up a new user with a real email address")
        print("3. Login as admin and approve the user")
        print("4. Check your email inbox!")
        print()
        
    except Exception as e:
        print(f"\n❌ Error updating app.py: {e}")
        print("\nPlease manually update EMAIL_CONFIG in app.py:")
        print(f"  'SENDER_EMAIL': '{sender_email}',")
        print(f"  'SENDER_PASSWORD': '{sender_password}',")

if __name__ == '__main__':
    configure_email()
