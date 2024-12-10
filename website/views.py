from flask import Blueprint, render_template
from .models import Product

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')

<<<<<<< Updated upstream


=======

@views.route('/product')
def product_details():
    # Dados fictícios para o produto
    product = {
        'name': 'Produto Fictício',
        'image_url': 'https://via.placeholder.com/500',
        'price': 'R$ 29,99',
        'color': 'Azul',
        'description': 'Este é um produto de teste para visualizar o front-end.'
    }

    # Comentários fictícios
    comments = [
        {'user': 'João', 'text': 'Muito bom, recomendo!'},
        {'user': 'Maria', 'text': 'Ótimo produto! Vale a pena!'},
        {'user': 'Carlos', 'text': 'Gostei bastante, mas poderia ser mais barato.'}
    ]

    # Renderizando o template com as informações
    return render_template('productDetails.html', product=product, comments=comments)


@views.route('/checkout')
def checkout():
    return render_template('checkout.html')


@views.route('/cart')
def cart():
    return render_template('cart.html')

@views.route('/search', methods=['POST'])
def search():
    search_query = request.form.get('search')
    products = Product.objects(name__icontains=search_query)  # MongoDB query
    return render_template('home.html', products=products)


>>>>>>> Stashed changes
