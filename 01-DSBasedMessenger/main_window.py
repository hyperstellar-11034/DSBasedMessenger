# streamlit run main_window.py

import streamlit as st
from datetime import datetime, timezone, date

from Models.user import User
from Models.message import Message
from Storage.storage_handler import StorageHandler
from DataStructures.stack import Stack

storage = StorageHandler()

def safe_rerun():
    try:
        st.experimental_rerun()
    except AttributeError:
        st.stop()

def push_page(page):
    if 'nav_stack' not in st.session_state:
        st.session_state['nav_stack'] = []
    st.session_state['nav_stack'].append(page)

def pop_page():
    if 'nav_stack' in st.session_state and st.session_state['nav_stack']:
        return st.session_state['nav_stack'].pop()
    return None

def sign_up():
    st.header("Sign Up")
    phone_number = st.text_input("Phone Number (11 digits)", key="signup_phone")
    name = st.text_input("Name", key="signup_name")
    if st.button("Sign Up"):
        try:
            user = User(phone_number, name)
            storage.add_user(user)
            st.success("Sign up successful! Please sign in.")
        except ValueError as e:
            st.error(str(e))

def sign_in():
    st.header("Sign In")
    phone_number = st.text_input("Phone Number (11 digits)", key="signin_phone")
    if st.button("Sign In"):
        user = storage.get_user_by_phone(phone_number)
        if user:
            st.session_state['user'] = user
            st.success(f"Welcome back, {user.name}! Click on Sign In again.")
        else:
            st.error("User not found. Please sign up.")

def logout():
    if 'user' in st.session_state:
        del st.session_state['user']
    try:
        safe_rerun()
    except AttributeError:
        st.stop()

def show_contacts(user):
    st.subheader("Your Contacts")

    if not user.contacts:
        st.write("You have no contacts yet.")
    else:
        for idx, contact_phone in enumerate(user.contacts):
            contact_user = storage.get_user_by_phone(contact_phone)
            display_name = contact_user.name if contact_user else "Unknown contact"

            col1, col2, col3 = st.columns([4, 1, 1])
            with col1:
                st.write(f"{display_name} ({contact_phone})")
            with col2:
                if st.button(f"Message", key=f"message_contact_{idx}"):
                    st.session_state['message_to'] = contact_phone
                    st.session_state['nav_stack'].append(st.session_state.get('current_page', 'main'))
                    st.session_state['current_page'] = 'send_message'
                    safe_rerun()

            with col3:
                if st.button(f"Delete", key=f"delete_contact_{idx}"):
                    user.contacts.pop(idx)
                    storage.update_user(user)
                    st.success("Contact deleted.")
                    safe_rerun()

    # Add Contact form
    st.subheader("Add Contact")
    new_contact_phone = st.text_input("Contact's Phone Number (11 digits)", key="add_contact_phone")
    if st.button("Add Contact"):
        if len(new_contact_phone) != 11 or not new_contact_phone.isdigit():
            st.error("Phone number must be exactly 11 digits.")
        else:
            contact_user = storage.get_user_by_phone(new_contact_phone)
            if contact_user is None:
                st.error("This contact does not exist in the system.")
            else:
                if new_contact_phone in user.contacts:
                    st.warning("Contact already in your contacts list.")
                else:
                    user.add_contact(new_contact_phone)
                    storage.update_user(user)
                    st.success("Contact added successfully!")
                    safe_rerun()


def send_message_ui(user):
    to_phone = st.session_state.get('message_to')
    if not to_phone:
        return
    st.subheader(f"Send Message to {to_phone}")
    msg_content = st.text_area("Message content")
    if st.button("Send Message"):
        if not msg_content.strip():
            st.error("Message cannot be empty.")
        else:
            msg = Message(sender_id=user.phone_number, receiver_id=to_phone, content=msg_content, timestamp=datetime.now(timezone.utc))
            
            # Append message to sender's messages
            user.messages.append(msg)
            
            # Append message to receiver's messages
            receiver = storage.get_user_by_phone(to_phone)
            if receiver:
                receiver.messages.append(msg)
                storage.update_user(receiver)
            
            storage.update_user(user)
            
            st.success("Message sent!")
            del st.session_state['message_to']
            safe_rerun()
            '''
    if st.button("Cancel"):
        del st.session_state['message_to']
        safe_rerun() '''

def show_messages(user):
    st.subheader("Your Messages")

    search_date = st.date_input("Search messages by date (UTC)", value=None)

    filtered_messages = user.messages
    if search_date:
        filtered_messages = [m for m in user.messages if m.timestamp.date() == search_date]

    if not filtered_messages:
        st.write("No messages found for the selected date.")
        return

    # Sort by timestamp ascending (oldest to newest)
    filtered_messages.sort(key=lambda m: m.timestamp)

    # Using my own Stack Class to reverse the order (newest to olderst)
    msg_stack = Stack()
    for msg in filtered_messages:
        msg_stack.push(msg)

    idx = 0
    while not msg_stack.is_empty():
        message = msg_stack.pop()
        idx += 1
        timestamp_str = message.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")
        st.markdown(f"**Message #{idx}**")
        st.write(f"From: {message.sender_id}")
        st.write(f"Time: {timestamp_str}")
        st.write(f"Content: {message.content}")

        # Show replies if any
        if hasattr(message, "replies") and message.replies:
            st.markdown("**Replies:**")
            for r_idx, reply in enumerate(message.replies):
                r_time = reply.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")
                st.write(f"- [{r_time}] User {reply.sender_id}: {reply.content}")

        # Reply input
        reply_text = st.text_input(f"Reply to message #{idx+1}", key=f"reply_{idx}")
    if st.button(f"Send Reply to message #{idx+1}", key=f"send_reply_{idx}"):
        if reply_text.strip() == "":
            st.error("Reply cannot be empty.")
        else:
            reply_msg = Message(
                sender_id=user.phone_number,
                receiver_id=message.sender_id if user.phone_number != message.sender_id else message.receiver_id,
                content=reply_text,
                timestamp=datetime.now(timezone.utc),
                reply_to=message.timestamp.isoformat()
            )
            if not hasattr(message, "replies"):
                message.replies = []
            message.replies.append(reply_msg)

            # Update sender's data
            storage.update_user(user)

            # Update receiver's data
            receiver_phone = reply_msg.receiver_id
            receiver = storage.get_user_by_phone(receiver_phone)
            if receiver:
                # Find the original message in receiver's messages and append reply
                for m in receiver.messages:
                    if m.timestamp == message.timestamp:
                        if not hasattr(m, "replies"):
                            m.replies = []
                        m.replies.append(reply_msg)
                        break
                storage.update_user(receiver)

            st.success("Reply sent!")
            safe_rerun()


def developer_mode():
    st.header("Developer Mode")
    password = st.text_input("Enter developer password", type="password", key="dev_password")
    if st.button("Login as Developer"):
        if password == "4732":
            st.success("Developer mode activated")
            users = storage.get_all_users()
            st.subheader("All Registered Users")
            for idx, u in enumerate(users):
                col1, col2, col3 = st.columns([4, 2, 1])
                with col1:
                    st.write(f"{u.phone_number} - {u.name}")
                with col2:
                    pass  
        else:
            st.error("Incorrect password")

def main():
    st.title("DS Based Messenger")

    if 'nav_stack' not in st.session_state:
        st.session_state['nav_stack'] = []

    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'main'

    if 'user' not in st.session_state:
        mode = st.radio("Choose mode", ["Sign Up", "Sign In"])
        if mode == "Sign Up":
            sign_up()
        else:
            sign_in()
    else:
        user = st.session_state['user']
        st.write(f"Hello, {user.name}!")

        if st.button("Logout"):
            logout()
        st.markdown("If logout doesn't work on first click, please click twice.")
        
        # Show back button only if stack is not empty
        if st.session_state['nav_stack']:
            if st.button("← Back"):
                previous = st.session_state['nav_stack'].pop()
                st.session_state['current_page'] = previous
                safe_rerun()

        if st.session_state['current_page'] == 'main':
            show_contacts(user)
            if 'message_to' in st.session_state:
                st.session_state['nav_stack'].append('main')
                st.session_state['current_page'] = 'send_message'
                safe_rerun()
            else:
                show_messages(user)

        elif st.session_state['current_page'] == 'send_message':
            send_message_ui(user)


    st.markdown("---")
    developer_mode()

if __name__ == "__main__":
    main()
