import streamlit as st
import re
import secrets
import string
import math
import smtplib
from email.message import EmailMessage
import random
import os

# Common passwords list for strict security
COMMON_PASSWORDS = {"password", "123456", "qwerty", "admin", "letmein", "abc123", "iloveyou", "monkey"}

# Function to calculate password entropy
def calculate_entropy(password):
    unique_chars = len(set(password))
    entropy = len(password) * math.log2(unique_chars)
    return entropy

# Function to check password strength
def check_password_strength(password):
    score = 0
    feedback = []
    
    # Length Check (1 point)
    if len(password) >= 12:
        score += 1
    else:
        feedback.append("❌ Password should be at least 12 characters long.")
    
    # Upper & Lowercase Check (1 point)
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")
    
    # Digit Check (1 point)
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")
    
    # Special Character Check (1 point)
    if re.search(r"[!@#$%^&*()_+={}:;'<>?,./\"\\|~`-]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*...).")
    
    # No Common Patterns (1 point)
    if password.lower() not in COMMON_PASSWORDS:
        score += 1
    else:
        feedback.append("❌ Avoid common passwords like 'password' or '123456'.")
    
    # Repeated Patterns Check
    if re.search(r"(.)\1{3,}", password):
        feedback.append("❌ Avoid repeated characters or patterns like 'aaaa' or '1111'.")
    
    # Entropy Check
    entropy = calculate_entropy(password)
    if entropy < 50:
        feedback.append("⚠️ Password entropy is low, try increasing randomness.")
    
    # Strength Rating
    if score == 5 and entropy >= 60:
        feedback.append("✅ Strong Password! 🎉")
    elif score >= 3:
        feedback.append("⚠️ Moderate Password - Consider adding more security features.")
    else:
        feedback.append("❌ Weak Password - Improve it using the suggestions above.")
    
    return score, feedback, entropy

# Function to generate a strong password
def generate_strong_password(length=16):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()_+={}:;'<>?,./\"\\|~`-"
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

# Streamlit App
def main():
    st.title("🔐 Advanced Password Manager")
    st.write("Check the strength of your password with enhanced security")

    # Input field for password
    password = st.text_input("Enter your password:", type="password")

    if password:
        # Check password strength
        score, feedback, entropy = check_password_strength(password)

        # Display feedback
        st.subheader("Password Analysis:")
        for message in feedback:
            st.write(message)

        # Display entropy
        st.subheader("Entropy Score:")
        st.write(f"🔢 Entropy: {entropy:.2f} bits (Higher is better)")

        # Display strength score
        st.subheader("Strength Score:")
        if score == 5 and entropy >= 60:
            st.success("Strong Password! 🎉")
        elif score >= 3:
            st.warning("Moderate Password ⚠️")
        else:
            st.error("Weak Password ❌")

    # Password Generator Section
    st.markdown("---")
    st.subheader("🔧 Password Generator")
    if st.button("Generate Strong Password"):
        strong_password = generate_strong_password()
        st.code(strong_password)

# Run the app
if __name__ == "__main__":
    main()

