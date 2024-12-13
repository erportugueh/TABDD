from flask import Blueprint, render_template, request, jsonify
from .models import Product, Item, Rating, Customer
import os
from .admin import dbmongo
from random import sample
import logging
from pymongo import DESCENDING

views = Blueprint('views', __name__)

@views.route('/')
def home():
    # Generate 6 random numbers (IDs) between 1 and 100
    random_ids = sample(range(1, 101), 9)
    products_data = []
    for id in random_ids:
        product = get_product(id)
        products_data.append(product)
    return render_template('home.html', products=products_data)


from flask import render_template, jsonify
from pymongo import DESCENDING


@views.route('/termos', methods=['GET'])
def termos():
    try:
        # Fetch the latest version of terms from MongoDB
        latest_terms = dbmongo['TermsAndConditions'].find_one({}, sort=[("Version", DESCENDING)])

        if not latest_terms:
            return jsonify({"error": "No terms found."}), 404

        # Pass the terms to the template
        return render_template('termos.html', terms=latest_terms)
    except Exception as e:
        logging.error(f"Error fetching terms: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500


@views.route('/search', methods=['GET'])
def search():

    search_query = request.args.get('query')  # Use 'form.get()' for POST method
    print(search_query)
    if search_query:
        # Perform the search
        products = Product.objects(category__icontains=search_query)
        if products:
            products_data = []
            for product in products:
                product = get_product(product.item_id)
                products_data.append(product)
            return render_template('home_search.html', products=products_data, result_string = f"Results for '{search_query}'")
        else:
            return render_template('home_search.html', products=[], result_string = f"No items that match '{search_query}' were found")

@views.route('/product/<int:item_id>', methods=['GET'])
def product_details(item_id):
    id = item_id
    # Fetch products matching the random IDs
    product = Product.objects(item_id=id).first()
    # Extract technical_info and physical_info into dictionaries

    tech_dict = {list(info.to_mongo().keys())[0]: list(info.to_mongo().values())[0] for info in product.technical_info}
    physical_dict = {list(info.to_mongo().keys())[0]: list(info.to_mongo().values())[0] for info in
                     product.physical_info}

    image_name_prefix = f"{id}"
    image_directory = r"C:\Git\TABDD\E-Commerce-Main-App\E-CommerceProject\website\static\images"
    # Find the image file that starts with the item_id
    image_file = next(
        (img for img in os.listdir(image_directory) if img.startswith(image_name_prefix)),
        "default.jpg"
    )
    image_path = f"../static/images/{image_file}"

    item = Item.query.filter_by(item_id=id).first()
    product = {
        "item_id": product.item_id,
        "name": item.name,
        "description": item.description,
        "type": item.type,
        "price": product.price,
        "discount": product.discount * 100,
        "category": product.category,
        "subcategory": product.subcategory,
        "tech": tech_dict,
        "physical": physical_dict,
        "image": image_path
    }


    # Query the Ratings collection for reviews with the given item_id
    reviews = Rating.objects(item_id=item_id)
    for review in reviews:
        customer = Customer.query.filter_by(customer_id=review.customer_id).first()
        review.user = customer.name

    return render_template('productDetails.html', product=product, reviews=reviews)

def get_product(id):
    # Fetch products matching the random IDs
    product = Product.objects(item_id=id).first()
    # Extract technical_info and physical_info into dictionaries

    tech_dict = {list(info.to_mongo().keys())[0]: list(info.to_mongo().values())[0] for info in product.technical_info}
    physical_dict = {list(info.to_mongo().keys())[0]: list(info.to_mongo().values())[0] for info in
                     product.physical_info}

    image_name_prefix = f"{id}"
    image_directory = r"C:\Git\TABDD\E-Commerce-Main-App\E-CommerceProject\website\static\images"
    # Find the image file that starts with the item_id
    image_file = next(
        (img for img in os.listdir(image_directory) if img.startswith(image_name_prefix)),
        "default.jpg"
    )
    image_path = f"../static/images/{image_file}"

    item = Item.query.filter_by(item_id=id).first()

    product = {
        "item_id": product.item_id,
        "name": item.name,
        "price": product.price,
        "category": product.category,
        "subcategory": product.subcategory,
        "tech": tech_dict,
        "physical": physical_dict,
        "image": image_path
    }
    return product

