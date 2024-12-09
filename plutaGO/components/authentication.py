from controllers.UserController import UserController
from models.User import User
userController = UserController('plutaGO.db')

import streamlit as st
def sign_up_form(key):
    sign_up_data = {
        "name": None,
        "surname": None,
        "email": None,
        "password": None,
        "role": None,
    }
    with st.form(key=key):
        sign_up_data['name'] = st.text_input('Enter name')
        sign_up_data['surname'] = st.text_input('Enter surname')
        sign_up_data['email'] = st.text_input('Enter email')
        sign_up_data['password'] = st.text_input('Enter password')
        sign_up_data['role'] = st.text_input('Enter role')

        submit_button = st.form_submit_button(label='Sign up')

        if submit_button:
            if not all(sign_up_data.values()):
                st.warning('Please provide all data')
            else:
                new_user = User(**{"id": None,"amount_of_pluts": 0, **sign_up_data})
                userController.create(new_user)
                sign_in(new_user)
                st.success('Great')
                

def sign_in(user: User):
    st.session_state['auth_data'] = {
        "user": user
    }
def sign_in_form(key):
    with st.form(key=key):
        email = st.text_input('Enter email')
        password = st.text_input('Enter password')

        submit_button = st.form_submit_button(label='Sign in')

        if submit_button:
            if len(email) < 4 or len(password) < 4:
                st.warning('Please fill all the field')
            else:
                user = userController.login(email=email, password=password)
                if not user:
                    st.error('Invalid email or password')
                    return None, None
                else:
                    sign_in(user)
                    st.success("Great!")
