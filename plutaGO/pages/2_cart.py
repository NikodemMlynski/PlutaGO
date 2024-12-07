import streamlit as st
from datetime import datetime
from controllers.OrderController import OrderController
from models.Order import Order
from controllers.OrderPositionController import OrderPositionController
from models.Order_position import OrderPosition
from controllers.PaymentController import PaymentController
from components.authentication import sign_up_form, sign_in_form
from controllers.AddressController import AddressController
from models.Address import Address
st.title('Cart')
# st.write('Trzeba zaimplementowac funkcje tworzaca zamowienie')
# st.write('Tworzaca platnosc')
# st.write('I odejmowanie z konta uzytkownikowi')



def make_order(products):
    if 'auth_data' in st.session_state and 'user' in st.session_state['auth_data']:
        user = st.session_state['auth_data']['user']
        addressController = AddressController(db_path='plutaGO.db')
        user_address = addressController.get_address_by_user_id(user.id)
        if user_address:
            st.subheader('Teraz tu trzeba dodac juz logike zamowienia')
            orderController = OrderController(db_path='plutaGO.db')
            new_order = Order(id=None, user_id=user.id, date=datetime.now(), status='not_paid', address_id=user_address.id)
            new_order_id = orderController.create(new_order)
            for product in products:
                new_order_position = OrderPosition(id=None, order_id=new_order_id, product_id=product['product'].id, amount=product['quantity'])
                orderPositionController = OrderPositionController(db_path='plutaGO.db')
                orderPositionController.create(new_order_position)

        else:
            st.subheader('Dodaj adres do swojego konta na stronie authentication')
        # przechodzimy do tworzenia platnosci itp
        pass
    else:
        # zrobic logowanie i wywolac funkcje jeszcze raz
        st.subheader('Zaloguj się i wróć do karty')
        

if "cart" not in st.session_state or len(st.session_state['cart']['products']) == 0:
    st.write('Your cart is empty')
else:
    with st.container(border=True):
        products = st.session_state['cart']['products']
        for product in products:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(product['product'].name)
            with col2:
                st.write(product['product'].price)
            with col3:
                st.write(product['quantity'])
        total_cost = sum([float(product['product'].price) * product['quantity'] for product in products ])
        col_left, col_right = st.columns(2)
        with col_left:
            st.subheader(f'Total cost: {total_cost} PLT')
        with col_right:
            st.button(label='Buy', on_click=make_order, args=(products, ))
        

