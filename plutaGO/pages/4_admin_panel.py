import streamlit as st
import pandas as pd
from controllers.categoryController import CategoryController
from models.Category import Category
from controllers.ProductController import ProductController
from models.Product import Product


product_categories_tab, products_tab, orders_tab = st.tabs(['Product categories', 'Products', 'Orders'])
categoryController = CategoryController(db_path='plutaGO.db')
categories = categoryController.get_all()

with product_categories_tab:
    with st.container(border=True):
        st.subheader('Categories')
        categories_dict = [category.__dict__ for category in categories]
        df = pd.DataFrame(categories_dict)
        st.table(df)
    category = {
        "name": None
    }
    with st.form(key='create_category_form'):
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
            

    category_to_edit = {
        "id": categories[0].id,
        "name": categories[0].name
    }
    with st.form(key='edit_category_form'):
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
    
    def deleteHandler(id):
        categoryController.delete(id)
    with st.container(border=True):
        for category in categories:
            c_id, c_name, c_button = st.columns(3)
            with c_id:
                st.write(category.id)
            with c_name:
                st.write(category.name)
            with c_button:
                st.button('Delete', key=f'button_{category.id}', on_click=deleteHandler, args=(category.id, ))


with products_tab:
    productController = ProductController('PlutaGO.db')
    with st.container(border=True):
        products = productController.get_all()
        products_dict = [product.__dict__ for product in products]
        df = pd.DataFrame(products_dict)
        df = df.set_index('id')
        st.table(df) 
    
    product = {
        'name': None,
        'description': None,
        'category_id': None,
        'photo': None,
        'price': None,
    }
    with st.form(key='create_product_form'):
        st.subheader('Create product')
        product['name'] = st.text_input('Enter product name')
        product['description'] = st.text_area('Enter product description')
        selected_name = st.selectbox('categoryId', [category.name for category in categories])
        product['category_id'] = [category for category in categories if category.name == selected_name][0].id
        product['photo'] = st.text_input('Enter link to product photo')
        product['price'] = st.number_input('Enter product price (PLT)')

        submit_button = st.form_submit_button(label='Create')
        
        if submit_button:
            if not all (product.values()):
                st.warning('Please fill all the field')
            else:
                pass
                product = Product(**{"id": None, **product})
                productController.create(product)
                st.success("Great!")






# product = {
#     name: None,
#     description: None,
#     category_id: None,
#     photo: None,
#     price: None,
# }
# with st.form(key='add_product_form'):
    