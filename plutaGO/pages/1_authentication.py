import streamlit as st
from components.authentication import sign_up_form, sign_in_form
from models.Address import Address
from controllers.AddressController import AddressController
from controllers.UserController import UserController
from controllers.PaymentController import PaymentController
addressController = AddressController(db_path='plutaGO.db')
if 'auth_data' not in st.session_state:
    st.session_state.auth_data = {}
    

signin_tab, signup_tab = st.tabs(['Sign in ', 'Sign Up'])
with signin_tab:
    st.subheader('Sign in')
    sign_in_form(key='sign_in')
    
def address_form(user_id):
    address_data = {
        "city": None,
        "street": None,
        "local_number": None
    }
    with st.form(key='add_address_form'):
        address_data['city'] = st.text_input('Enter city')
        address_data['street'] = st.text_input('Enter street')
        address_data['local_number'] = st.text_input('Enter local number')

        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            if not all(address_data.values()):
                st.warning('Plaese provide all data')
            else:
                new_address = Address(**{"id": None, "user_id": user_id, **address_data})
                addressController.create(new_address)
                st.success('Great!')

with signup_tab:   
    st.subheader('Sign up') 
    
    sign_up_form(key='sign_up')

with st.container():
    if 'user' in st.session_state.auth_data:
        user = st.session_state.auth_data['user']
        if user:
            st.subheader('You adress')
            address = addressController.get_address_by_user_id(user.id)
            if address:
                st.write(address.__dict__)
            else:
                st.write('You did not provide your addres. Please fill up the form below')
                address_form(user.id)

        else:
            st.subheader('You are not logged in')

with st.container():
    if 'user' in st.session_state.auth_data:
        user = st.session_state.auth_data['user']
        if user:
            st.subheader('Manage your balance')
            st.write(f'Your balance: {user.amount_of_pluts} PLT')

            with st.form(key='add_plutas_form'):
                plutas_to_add = st.number_input('Enter value [PLT]')
                submit_button = st.form_submit_button(label='Add pluts')
                
                if submit_button:
                    if plutas_to_add > 0:
                        userController = UserController(db_path='plutaGO.db')
                        user.increase_pluts(plutas_to_add)
                        userController.update(user_id=user.id, new_data=user)
                        st.rerun()
                    else:
                        st.warning('Please provide correct number of PLT')

with st.container():
    if 'user' in st.session_state.auth_data:
        user = st.session_state.auth_data['user']
        if user:
            paymentController = PaymentController(db_path='plutaGO.db')
            payments = paymentController.get_all_payments_for_user(user.id)