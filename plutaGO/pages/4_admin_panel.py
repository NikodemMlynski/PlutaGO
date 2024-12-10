import streamlit as st
import pandas as pd
from controllers.categoryController import CategoryController
from models.Category import Category
from controllers.ProductController import ProductController
from models.Product import Product
from controllers.OrderPositionController import OrderPositionController
from models.Order_position import OrderPosition

from controllers.OrderController import OrderController


product_categories_tab, products_tab, orders_tab = st.tabs(['Product categories', 'Products', 'Orders'])
categoryController = CategoryController(db_path='plutaGO.db')
categories = categoryController.get_all()

with product_categories_tab:
    with st.container(border=True):
        st.subheader('Categories')
        categories_dict = [category.__dict__ for category in categories]
        df = pd.DataFrame(categories_dict)
        if df.size > 0:
            df = df.set_index('id')
            st.table(df) 
        else: 
            st.write('There are not orders yet')
    category = {
        "name": None
    }
    with st.form(key='create_category_form', clear_on_submit=True):
        st.subheader('Create category')
        category['name'] = st.text_input('Enter category name')

        submit_button = st.form_submit_button(label='Create')
        
        if submit_button:
            if not all (category.values()):
                st.warning('Please fill all the field')
            else:
                category = Category(id=None, name=category['name'])
                categoryController.create(category)
                st.success("Great!")
                st.rerun()
            

    category_to_edit = {
        "id": categories[0].id,
        "name": categories[0].name
    }
    with st.form(key='edit_category_form', clear_on_submit=True):
        st.subheader('Edit category')
        category_to_edit['id'] = st.selectbox('Id', [category.id for category in categories])
        category_to_edit['name'] = st.text_input('Enter category name', category_to_edit['name'])

        submit_button = st.form_submit_button(label='Edit')
        if submit_button:
            if not all(category_to_edit.values()):
                st.warning('Please fill all fields')
            else:
                updatedCategory = Category(**category_to_edit)
                categoryController.update(category_id=category_to_edit['id'], new_data=updatedCategory)
                st.success('Great')
                st.rerun()
    
    def deleteCategoryHandler(id):
        categoryController.delete(id)
        st.rerun()
    with st.container(border=True):
        for category in categories:
            c_id, c_name, c_button = st.columns(3)
            with c_id:
                st.write(category.id)
            with c_name:
                st.write(category.name)
            with c_button:
                st.button('Delete', key=f'button_category_{category.id}', on_click=deleteCategoryHandler, args=(category.id, ))


with products_tab:
    productController = ProductController('plutaGO.db')
    with st.container(border=True):
        products = productController.get_all()
        products_dict = [product.__dict__ for product in products]
        df = pd.DataFrame(products_dict)
        if df.size > 0:
            df = df.set_index('id')
            st.table(df) 
        else: 
            st.write('There are not orders yet')

        
    
    new_product = {
        'name': None,
        'description': None,
        'category_id': None,
        'photo': None,
        'price': None,
    }
    with st.form(key='create_product_form', clear_on_submit=True):
        st.subheader('Create product')
        new_product['name'] = st.text_input('Enter product name')
        new_product['description'] = st.text_area('Enter product description')
        selected_name = st.selectbox('categoryId', [category.name for category in categories])
        new_product['category_id'] = [category for category in categories if category.name == selected_name][0].id
        new_product['photo'] = st.text_input('Enter link to product photo')
        new_product['price'] = st.number_input('Enter product price (PLT)')

        submit_button = st.form_submit_button(label='Create')
        
        if submit_button:
            if not all (new_product.values()):
                st.warning('Please fill all the field')
            else:
                product = Product(**{"id": None, **new_product})
                productController.create(product)
                st.success("Great!")
                st.rerun()
    
    product_to_edit = {
        "id": products[0].id if products else None, 
        "name": None,
        "description": None,
        "category_id": None,
        "photo": None,
        "price": None,
    }
    with st.form(key='edit_product_form', clear_on_submit=True):
        st.subheader('Edit product')
        product_to_edit['id'] = st.selectbox('Id', [product.id for product in products])
        product_to_edit['name'] = st.text_input('Enter product name', product_to_edit['name'])
        product_to_edit['description'] = st.text_area('Enter product description', product_to_edit['description'])
        selected_name = st.selectbox('categoryId', [category.name for category in categories])
        product_to_edit['category_id'] = [category for category in categories if category.name == selected_name][0].id
        product_to_edit['photo'] = st.text_input('Enter product photo', product_to_edit['photo'])
        product_to_edit['price'] = st.number_input('Enter product price (PLT)', product_to_edit['price'])

        submit_button = st.form_submit_button(label='Edit')
        if submit_button:
            if not all(product_to_edit.values()):
                st.warning('Please fill all fields')
            else:
                updatedProduct = Product(**product_to_edit)
                print(updatedProduct)
                productController.update(product_id=product_to_edit['id'], new_data=updatedProduct)
                st.success('Great')
                st.rerun()
    
    def deleteProductHandler(id):
        productController.delete(id)
        st.rerun()
    with st.container(border=True):
        for product in products:
            c_id, c_name, c_button = st.columns(3)
            with c_id:
                st.write(product.id)
            with c_name:
                st.write(product.name)
            with c_button:
                st.button('Delete', key=f'button_product_{product.id}', on_click=deleteProductHandler, args=(product.id, ))

with orders_tab:
    orderController = OrderController('plutaGO.db')
    with st.container(border=True):
        orders = orderController.get_all()
        orders_dict = [order.__dict__ for order in orders]
        df = pd.DataFrame(orders_dict)
        if df.size > 0:
            # df = df.set_index('id')
            st.table(df) 
        else: 
            st.write('There are not orders yet')

    orders = orderController.get_all()
    def deleteOrderHandler(id):
        orderController.delete(id)
        orderPositionController.delete_by_order_id(id)
        st.rerun()
    with st.container(border=True):
        for order in orders:
            c_id, c_user_id, c_date, c_status, c_address_id, c_button = st.columns(6)
            with c_id:
                st.write(order.id)
            with c_user_id:
                st.write(order.user_id)
            with c_date:
                st.write(order.date)
            with c_address_id:
                st.write(order.address_id)
            with c_status:
                st.write(order.status)
            with c_button:
                st.button('Delete', key=f'button_order_{order.id}', on_click=deleteOrderHandler, args=(order.id, ))
    
    with st.container(border=True):
        st.subheader('Order positions')
        order_id = st.selectbox('orderId', [order.id for order in orders])
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
            st.subheader(f'Total price: {totalPrice} PLT')
                

    