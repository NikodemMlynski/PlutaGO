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

st.title(st.session_state.auth_data)
st.write('tutaj trzeba dodac funkconalnosc dodawania do karty')
st.write('Jezeli uzytkownik jest zalogowany to moze kupic od razu')
st.write('jezeli nie to musi sie zarejstrowac i zalogowac przed zakupem')
st.write('podaj tego typu dane jak adres itp')

def add_product_to_cart(product: Product):
    pass
with st.container():
    st.subheader('Products')
    productController = ProductController(db_path='PlutaGO.db')
    products = productController.get_all()
    
    for product in products:
        with st.container(border=True):
            name, description, category, price = st.columns(4)
            with name:
                st.write(product.name)
            with description:
                st.write(product.description)
            with category:
                categoryController = CategoryController(db_path='PlutaGO.db')
                category = categoryController.get_category_by_id(product.category_id)
                st.write(category.name)
            with price:
                st.write(product.price)
            st.button(label='Kup', key=f'add_to_cart_{product.id}')

    
# conn = sqlite3.connect('plutaGO.db')
# cursor = conn.cursor()
# cursor.execute('select name from sqlite_master where type="table";')


# tables = cursor.fetchall()

# for table in tables:
#     print(table[0])