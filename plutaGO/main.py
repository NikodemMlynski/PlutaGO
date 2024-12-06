# from controllers.UserController import UserController
# db_path = 'plutaGO.db'
import sqlite3
# logged_user = userController.login('niko@spoko.pl', 'asdf')
# print(logged_user)
# print(logged_user.name)
# print(logged_user.email)
import streamlit as st
from controllers.ProductController import ProductController
from models.Product import Product
from models.User import User
from models.Category import Category
from controllers.categoryController import CategoryController

st.title('PlutaGO')

# st.title(st.session_state.auth_data)
st.write('tutaj trzeba dodac funkconalnosc dodawania do karty')
st.write('Jezeli uzytkownik jest zalogowany to moze kupic od razu')
st.write('jezeli nie to musi sie zarejstrowac i zalogowac przed zakupem')
st.write('podaj tego typu dane jak adres itp')

if "cart" not in st.session_state:
    st.session_state.cart = {
        "products": []
    }
else :
    st.session_state['cart']['products']
 
def add_product_to_cart(product: Product):
    products_in_cart = st.session_state['cart']['products']
    filtered_products = [product_in_cart for product_in_cart in products_in_cart if product.id == product_in_cart['product'].id]

    if filtered_products: 
        product_in_cart_index = st.session_state['cart']['products'].index(filtered_products[0])
        st.session_state['cart']['products'][product_in_cart_index]['quantity'] += 1
    else:
        new_product_in_cart = {"quantity": 1, "product": product}
        st.session_state['cart']['products'].append(new_product_in_cart)

def delete_product_from_cart(productId):
    products_in_cart = st.session_state['cart']['products']
    filtered_products = [product_in_cart for product_in_cart in products_in_cart if productId == product_in_cart['product'].id]
    product_in_cart_index = products_in_cart.index(filtered_products[0])
    print(product_in_cart_index)
    if products_in_cart[product_in_cart_index]['quantity'] > 1:
        st.session_state['cart']['products'][product_in_cart_index]['quantity'] -= 1
    else:
        filtered_products_in_cart = [product_in_cart for product_in_cart in products_in_cart if productId != product_in_cart['product'].id]
        st.session_state['cart']['products'] = filtered_products_in_cart

with st.container():
    st.subheader('Products')
    productController = ProductController(db_path='plutaGO.db')
    products = productController.get_all()
    
    for product in products:
        with st.container(border=True):
            name, description, category, price = st.columns(4)
            with name:
                st.write(product.name)
            with description:
                st.write(product.description)
            with category:
                categoryController = CategoryController(db_path='plutaGO.db')
                category = categoryController.get_category_by_id(product.category_id)
                st.write(category.name)
            with price:
                st.write(product.price)
            products_in_cart = st.session_state['cart']['products']
            product_in_cart = [product_in_cart for product_in_cart in products_in_cart if product.id == product_in_cart['product'].id]
            with st.container():
                if product_in_cart:
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.button(key=f'increase_cart{product.id}', label="++", on_click=add_product_to_cart, args=(product, ))
                    with c2:
                        st.write(product_in_cart[0]['quantity'])
                    with c3:
                        st.button(key=f'decrease_cart{product.id}', label='--', on_click=delete_product_from_cart, args=(product.id, ))
                else:
                    st.button(label='Kup', key=f'add_to_cart_{product.id}', on_click=add_product_to_cart, args=(product,))
            

    
# conn = sqlite3.connect('plutaGO.db')
# cursor = conn.cursor()
# cursor.execute('select name from sqlite_master where type="table";')


# tables = cursor.fetchall()

# for table in tables:
#     print(table[0])