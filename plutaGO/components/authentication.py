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
        sign_up_data['name'] = st.text_input('Imię')
        sign_up_data['surname'] = st.text_input('Nazwisko')
        sign_up_data['email'] = st.text_input('Email')
        sign_up_data['password'] = st.text_input('Hasło')
        sign_up_data['role'] = st.text_input('rola')

        submit_button = st.form_submit_button(label='Zarejestruj się')

        if submit_button:
            if not all(sign_up_data.values()):
                st.warning('Podaj wszystkie dane')
            else:
                new_user = User(**{"id": None,"amount_of_pluts": 0, **sign_up_data})
                userController.create(new_user)
                sign_in(new_user)
                st.success('Pomyślnie zarejestrowano')
                

def sign_in(user: User):
    st.session_state['auth_data'] = {
        "user": user
    }
def sign_in_form(key):
    with st.form(key=key):
        email = st.text_input('Email')
        password = st.text_input('Hasło')

        submit_button = st.form_submit_button(label='Zaloguj się')

        if submit_button:
            if len(email) < 4 or len(password) < 4:
                st.warning('Podaj wszystkie dane')
            else:
                user = userController.login(email=email, password=password)
                if not user:
                    st.error('Niepoprawny email lub hasło')
                    return None, None
                else:
                    sign_in(user)
                    st.success("Pomyślnie zalogowano!")
