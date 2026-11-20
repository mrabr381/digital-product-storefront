/* Digital Product Storefront — cart + license keys, fully client-side.
   No network calls. Prices are integer cents so totals are exact. */
(function () {
  'use strict';

  var CART_KEY = 'storefront-cart-v1';
  var KEY_CHARS = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; // no 0/O, 1/I

  function loadCart() {
    try {
      var raw = localStorage.getItem(CART_KEY);
      if (!raw) return {};
      var cart = JSON.parse(raw);
      return cart && typeof cart === 'object' ? cart : {};
    } catch (e) { return {}; }
  }

  function saveCart(cart) {
    try { localStorage.setItem(CART_KEY, JSON.stringify(cart)); } catch (e) { /* storage full/blocked: cart just won't persist */ }
  }

  // cart: {productId: quantity}. Quantities are clamped to 1..99.
  function addToCart(cart, productId, qty) {
    qty = Math.floor(Number(qty) || 1);
    if (qty < 1) qty = 1;
    if (qty > 99) qty = 99;
    cart[productId] = Math.min(99, (cart[productId] || 0) + qty);
    return cart;
  }

  function setQuantity(cart, productId, qty) {
    qty = Math.floor(Number(qty) || 0);
    if (qty <= 0) { delete cart[productId]; } else { cart[productId] = Math.min(99, qty); }
    return cart;
  }

  function removeFromCart(cart, productId) {
    delete cart[productId];
    return cart;
  }

  function cartItemCount(cart) {
    var n = 0;
    for (var id in cart) n += cart[id];
    return n;
  }

  // products: [{id, price_cents}]. Unknown ids are ignored (defensive).
  function cartTotalCents(cart, products) {
    var byId = {};
    products.forEach(function (p) { byId[p.id] = p.price_cents; });
    var total = 0;
    for (var id in cart) {
      if (byId[id] !== undefined) total += byId[id] * cart[id];
    }
    return total;
  }

  function formatPrice(cents, currency) {
    currency = currency || 'USD';
    var symbol = currency === 'USD' ? '$' : currency + ' ';
    return symbol + (cents / 100).toFixed(2);
  }

  // Demo-grade license key: 4 groups of 4, e.g. 7KQ2-9X4M-T8PW-2D6N.
  // NOT DRM — anyone can generate one. Real delivery should come from the
  // seller's email / payment processor, not from this button.
  function generateLicenseKey() {
    var groups = [];
    for (var g = 0; g < 4; g++) {
      var group = '';
      for (var i = 0; i < 4; i++) {
        group += KEY_CHARS.charAt(Math.floor(Math.random() * KEY_CHARS.length));
      }
      groups.push(group);
    }
    return groups.join('-');
  }

  function isValidLicenseKey(key) {
    return /^[A-HJ-NP-Z2-9]{4}(-[A-HJ-NP-Z2-9]{4}){3}$/.test(key);
  }

  // ---- DOM wiring (browser only) ----
  function initDom() {
    var products = window.STOREFRONT_PRODUCTS || [];
    var cart = loadCart();

    function renderCart() {
      var countEl = document.getElementById('cart-count');
      if (countEl) countEl.textContent = String(cartItemCount(cart));
      var body = document.getElementById('cart-items');
      var totalEl = document.getElementById('cart-total');
      var emptyEl = document.getElementById('cart-empty');
      if (!body) return;
      var byId = {};
      products.forEach(function (p) { byId[p.id] = p; });
      var rows = '';
      var hasItems = false;
      for (var id in cart) {
        if (!byId[id]) continue;
        hasItems = true;
        var p = byId[id];
        rows += '<tr><td>' + escapeHtml(p.name) + '</td>'
          + '<td class="qty"><button data-dec="' + id + '" aria-label="Decrease quantity">−</button> '
          + cart[id]
          + ' <button data-inc="' + id + '" aria-label="Increase quantity">+</button></td>'
          + '<td>' + formatPrice(p.price_cents * cart[id], p.currency) + '</td>'
          + '<td><button data-remove="' + id + '">Remove</button></td></tr>';
      }
      body.innerHTML = rows;
      if (totalEl) totalEl.textContent = formatPrice(cartTotalCents(cart, products));
      if (emptyEl) emptyEl.style.display = hasItems ? 'none' : 'block';
      var tableEl = document.getElementById('cart-table');
      if (tableEl) tableEl.style.display = hasItems ? '' : 'none';
    }

    function escapeHtml(s) {
      return String(s).replace(/[&<>"']/g, function (c) {
        return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
      });
    }

    document.addEventListener('click', function (e) {
      var t = e.target;
      if (t.hasAttribute('data-add')) {
        addToCart(cart, t.getAttribute('data-add'), 1);
        saveCart(cart); renderCart();
      } else if (t.hasAttribute('data-inc')) {
        addToCart(cart, t.getAttribute('data-inc'), 1);
        saveCart(cart); renderCart();
      } else if (t.hasAttribute('data-dec')) {
        var id = t.getAttribute('data-dec');
        setQuantity(cart, id, (cart[id] || 1) - 1);
        saveCart(cart); renderCart();
      } else if (t.hasAttribute('data-remove')) {
        removeFromCart(cart, t.getAttribute('data-remove'));
        saveCart(cart); renderCart();
      } else if (t.id === 'demo-key-btn') {
        var out = document.getElementById('demo-key-out');
        if (out) out.textContent = generateLicenseKey();
      }
    });

    renderCart();
  }

  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initDom);
    } else { initDom(); }
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
      loadCart: loadCart, saveCart: saveCart, addToCart: addToCart,
      setQuantity: setQuantity, removeFromCart: removeFromCart,
      cartItemCount: cartItemCount, cartTotalCents: cartTotalCents,
      formatPrice: formatPrice, generateLicenseKey: generateLicenseKey,
      isValidLicenseKey: isValidLicenseKey
    };
  }
})();
