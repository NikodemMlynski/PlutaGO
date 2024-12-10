import streamlit as st
from datetime import datetime
from controllers.OrderController import OrderController
from models.Order import Order
from controllers.OrderPositionController import OrderPositionController
from models.Order_position import OrderPosition
from controllers.PaymentController import PaymentController
from models.Payment import Payment
from components.authentication import sign_up_form, sign_in_form
from controllers.AddressController import AddressController
from models.Address import Address
from controllers.UserController import UserController
st.title('Cart')


def make_order(products):
    if 'auth_data' in st.session_state and 'user' in st.session_state['auth_data']:
        user = st.session_state['auth_data']['user']
        total_cost = round(sum([float(product['product'].price) * product['quantity'] for product in products ]))

        if user.amount_of_pluts >= total_cost:
            addressController = AddressController(db_path='plutaGO.db')
            user_address = addressController.get_address_by_user_id(user.id)
            if user_address:
                orderController = OrderController(db_path='plutaGO.db')
                order_date = datetime.now()
                new_order = Order(id=None, user_id=user.id, date=order_date, status='ordered', address_id=user_address.id)
                new_order_id = orderController.create(new_order)
                for product in products:
                    new_order_position = OrderPosition(id=None, order_id=new_order_id, product_id=product['product'].id, amount=product['quantity'])
                    orderPositionController = OrderPositionController(db_path='plutaGO.db')
                    orderPositionController.create(new_order_position)
                    st.session_state.cart = {
                        "products": []
                    }
                st.success('Zamówienia się powiodło')
                paymentController = PaymentController(db_path='plutaGO.db')
                userController = UserController(db_path='plutaGO.db')
                user.make_payment(total_cost)
                userController.update(user.id, user)
                payment = Payment(id=None, user_id=user.id, order_id=new_order_id, amount=total_cost, date=order_date)
                paymentController.create(payment)
            else:
                st.subheader('Dodaj adres do swojego konta na stronie authentication')
        else:
            st.error(f'UUUU masz za mało plut')

        
    else:
        # zrobic logowanie i wywolac funkcje jeszcze raz
        st.subheader('Zaloguj się i wróć do karty')
        

if "cart" not in st.session_state or len(st.session_state['cart']['products']) == 0:
    st.write('Dodaj coś do karty na stronie main')
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
            st.subheader(f'Łączna cena: {total_cost} PLT')
        with col_right:
            st.button(label='Kup', on_click=make_order, args=(products, ))
        

