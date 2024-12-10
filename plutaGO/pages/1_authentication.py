import streamlit as st
from components.authentication import sign_up_form, sign_in_form
from models.Address import Address
from controllers.AddressController import AddressController
from controllers.UserController import UserController
from controllers.PaymentController import PaymentController
from controllers.OrderController import OrderController
from controllers.ProductController import ProductController
from controllers.OrderPositionController import OrderPositionController
addressController = AddressController(db_path='plutaGO.db')
import pandas as pd
if 'auth_data' not in st.session_state:
    st.session_state.auth_data = {}
    

signin_tab, signup_tab = st.tabs(['Logowanie', 'Rejestracja'])
with signin_tab:
    st.subheader('Zaloguj się')
    sign_in_form(key='sign_in')
    
def address_form(user_id):
    address_data = {
        "city": None,
        "street": None,
        "local_number": None
    }
    with st.form(key='add_address_form'):
        address_data['city'] = st.text_input('Miasto')
        address_data['street'] = st.text_input('Ulica')
        address_data['local_number'] = st.text_input('Nr domu/mieszkania')

        submit_button = st.form_submit_button(label='Zarejestruj się')

        if submit_button:
            if not all(address_data.values()):
                st.warning('Podaj wszystkie dane')
            else:
                new_address = Address(**{"id": None, "user_id": user_id, **address_data})
                addressController.create(new_address)
                st.success('Udało  CI się dodać adres!')
                st.rerun()

with signup_tab:   
    st.subheader('Zarejestruj się') 
    
    sign_up_form(key='sign_up')

with st.container():
    if 'user' in st.session_state.auth_data:
        user = st.session_state.auth_data['user']
        if user:
            st.subheader('Twój adres')
            address = addressController.get_address_by_user_id(user.id)
            if address:
                st.write(address.__dict__)
            else:
                st.write('Nie podałeś adresu. Podaj go poniżej')
                address_form(user.id)

        else:
            st.subheader('Zaloguj się.')

with st.container():
    if 'user' in st.session_state.auth_data:
        user = st.session_state.auth_data['user']
        if user:
            st.subheader('Zarządzaj twoim stanem plut')
            st.write(f'Stan plut: {user.amount_of_pluts} PLT')

            with st.form(key='add_plutas_form'):
                plutas_to_add = st.number_input('Podaj ilość [PLT]')
                submit_button = st.form_submit_button(label='Dodaj pluty')
                
                if submit_button:
                    if plutas_to_add > 0:
                        userController = UserController(db_path='plutaGO.db')
                        user.increase_pluts(plutas_to_add)
                        userController.update(user_id=user.id, new_data=user)
                        st.rerun()
                    else:
                        st.warning('Podaj prawidłową wartość plut')

with st.container():
    if 'user' in st.session_state.auth_data:
        user = st.session_state.auth_data['user']
        if user:
            paymentController = PaymentController(db_path='plutaGO.db')
            payments = paymentController.get_all_payments_for_user(user.id)

def mark_as_received(order_id):
    orderController.update_order_status(order_id=order_id, status='Odebrane')

def display_orders(orders, received):
    order_id = st.selectbox('id zamówienia', [order.id for order in orders])
    orderPositionController = OrderPositionController(db_path='plutaGO.db')
    order_positions = orderPositionController.get_order_positions_by_order_id(order_id)

    df = pd.DataFrame([order_position.__dict__ for order_position in order_positions])
    
    if df.size > 0:
        df = df.set_index('id')

        def get_product_details(product_id):
            product = productController.get_product_by_id(product_id)
            return product.name, product.price  

        df[['name', 'price']] = df['product_id'].apply(get_product_details).tolist()
        st.table(df)
        df['totalPrice'] = df['amount'] * df['price'].astype(float)
        totalPrice = round(df['totalPrice'].sum(), 2)
        st.subheader(f'Łączna cena: {totalPrice} PLT')

    if not received:
        st.button('Oznacz jako odebrane', on_click=mark_as_received, args=(order_id,))


with st.container(border=True):
    if 'user' in st.session_state.auth_data:
        user = st.session_state.auth_data['user']
        if user:
            st.subheader('Twoje zamówienia')
            received_orders_tab, not_received_orders_tab = st.tabs(['Odebrane zamówienia', 'Nie odebrane zamówienia'])
            orderController = OrderController(db_path='plutaGO.db')
            orders = orderController.get_orders_for_user(user_id=user.id)
            productController = ProductController(db_path='plutaGO.db')
            with received_orders_tab:
                display_orders([order for order in orders if order.status == 'Odebrane'], True)
            with not_received_orders_tab:
                display_orders([order for order in orders if not(order.status == 'Odebrane')], False)

            