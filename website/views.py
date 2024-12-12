from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')

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
    {'user': 'João', 'text': 'Muito bom, recomendo!', 'rating': 4},
    {'user': 'Maria', 'text': 'Ótimo produto! Vale a pena!', 'rating': 5},
    {'user': 'Carlos', 'text': 'Gostei bastante, mas poderia ser mais barato.', 'rating': 3}
]

    
    # Renderizando o template com as informações
    return render_template('productDetails.html', product=product, comments=comments)

@views.route('/checkout')
def checkout():
    return render_template('checkout.html')

@views.route('/cart')
def cart():
    return render_template('cart.html')


@views.route('/userDetails')
def userDetails():
    return render_template('userDetails.html')

@views.route('/confirmacao')
def confirmacao():
    return render_template('confirmacao.html')

@views.route('/processarPagamento')
def processarPagamento():
    return render_template('processarPagamento.html')


@views.route('/homeSearch')
def homeSearch():
    return render_template('homeSearch.html')

# TERMOS
@views.route('/termos')
def termos():
    return render_template('termos.html')


@views.route('/help')
def help():
    return render_template('help.html')


# user - costumer 
# ACTIVE ORDERS 
@views.route('/activeOrders')
def activeOrders():
    return render_template('activeOrders.html')

# ORDERS & REVIEWS 
@views.route('/ordersReview')
def ordersReview():
    return render_template('ordersReview.html')

#user -  Warehouse Manager 
@views.route('/warehouseManager')
def warehouseManager():
    return render_template('warehouseManager.html')


#user -  Delivery Order Manager 
@views.route('/deliveryOrderManager')
def deliveryOrderManager():
    return render_template('deliveryOrderManager.html')


#user - Manager 
@views.route('/manager')
def manager():
    return render_template('manager.html')

#user - CIO
@views.route('/cio')
def cio():
    return render_template('cio.html')