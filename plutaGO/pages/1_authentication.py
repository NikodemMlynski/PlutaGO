import streamlit as st

from controllers.UserController import UserController
from models.User import User
signin_tab, signup_tab = st.tabs(['Sign in ', 'Sign Up'])
userController = UserController('plutaGO.db')

if 'auth_data' not in st.session_state:
    st.session_state.auth_data = None


with signin_tab:
    st.subheader('Sign in')
    with st.form(key='signin_form'):
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
                else:
                    st.session_state['auth_data'] = {
                        email: email,
                        password: password
                    }
                    st.success("Great!")

with signup_tab:   
    st.subheader('Sign up') 
    sign_up_data = {
        "name": None,
        "surname": None,
        "email": None,
        "password": None,
        "role": None,
    }
    with st.form(key='signup_form'):
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

