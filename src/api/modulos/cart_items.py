from flask import Blueprint, jsonify, request
from app import db
from models import Cart, Product, CartItem
from schemas import CartItemSchema

cart_items_bp = Blueprint('cart_items', __name__, url_prefix='/carts/<int:cart_id>/items')
cart_item_schema = CartItemSchema()

# Endpoint para crear un nuevo item de carrito
@cart_items_bp.route('', methods=['POST'])
def create_cart_item(cart_id):
    # Verificar si el carrito existe
    cart = Cart.query.get_or_404(cart_id)

    # Obtener los datos del item de carrito a través del JSON de la solicitud
    request_data = request.get_json()

    # Verificar si el producto existe
    product = Product.query.get_or_404(request_data['product_id'])

    # Crear el nuevo item de carrito
    new_cart_item = CartItem(cart_id=cart_id, product_id=request_data['product_id'], quantity=request_data['quantity'])
    db.session.add(new_cart_item)
    db.session.commit()

    # Serializar el item de carrito y retornarlo en la respuesta
    result = cart_item_schema.dump(new_cart_item)
    return jsonify(result)

# Endpoint para actualizar un item de carrito existente
@cart_items_bp.route('/<int:item_id>', methods=['PUT'])
def update_cart_item(cart_id, item_id):
    # Verificar si el carrito existe
    Cart.query.get_or_404(cart_id)

    # Verificar si el item de carrito existe
    cart_item = CartItem.query.filter_by(id=item_id, cart_id=cart_id).first_or_404()

    # Obtener los datos actualizados del item de carrito a través del JSON de la solicitud
    request_data = request.get_json()

    # Actualizar los datos del item de carrito y guardarlos en la base de datos
    cart_item.product_id = request_data['product_id']
    cart_item.quantity = request_data['quantity']
    db.session.commit()

    # Serializar el item de carrito actualizado y retornarlo en la respuesta
    result = cart_item_schema.dump(cart_item)
    return jsonify(result)

# Endpoint para eliminar un item de carrito existente
@cart_items_bp.route('/<int:item_id>', methods=['DELETE'])
def delete_cart_item(cart_id, item_id):
    # Verificar si el carrito existe
    Cart.query.get_or_404(cart_id)

    # Verificar si el item de carrito existe
    cart_item = CartItem.query.filter_by(id=item_id, cart_id=cart_id).first_or_404()

    # Eliminar el item de carrito de la base de datos
    db.session.delete(cart_item)
    db.session.commit()

    # Retornar una respuesta vacía con un código de estado 204 (sin contenido)
    return '', 204
