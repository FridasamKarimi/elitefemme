let cart = [];
const stripe = Stripe('publishable key')

document.querySelectorAll('.add-to-cart').forEach(button => {
    button.addEventListener('click', () => {
        const item = {
            id: button.getAttribute('data-id'),
            name: button.getAttribute('data-name'),
            price: parseFloat(button.getAttribute('data-price'))

        };
        cart.push(item);
        updateCart();
    });
});

function updateCart() {
    const cartItems = document.getElementById('cart-items');
    constcartTotal = document.getElementById('cart-total');
    cartItems.innerHTML = '';
    cart.forEach(item => {
        const li = document.createElement('li');
        li.textContent = '${item.name} - $${item.price}';
        cartItems.appendChild(li);

    });
    const total = cart.reduce((sum, item) => sum + item.price, 0);
    cartTotal.textContent = total.toFixed(2);
    
}

document.getElementById('checkout').addEventListener('click', () => {
    if (cart.length === 0) {
        alert('Your cart is empty!');
        return;
    }
    fetch('/create-checkout-session', {
        method: 'POST',
        headers: {'Content-Type': 'application/json' },
        body: JSON.stringify({ cart: cart})
    })
    .then(response => response.json())
    .then(session => stripe.redirectToCheckout({ sessionId: sessionId }))
    .catch(error => console.error('Error:', error));
});