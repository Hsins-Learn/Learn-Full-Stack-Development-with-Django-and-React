export const addItemToCart = (item, next) => {
  let cart = [];
  // we can verify whether this is a browser or not by checking the window
  // object. note that the window object is available only in the browser
  if (typeof window !== undefined) {
    if (localStorage.getItem("cart")) {
      cart = JSON.parse(localStorage.getItem("cart"))
    }

    cart.push({
      ...item
    });

    localStorage.setItem("cart", JSON.stringify(cart));
    next();
  }
}

export const loadCart = () => {
  if (typeof windows !== undefined) {
    if (localStorage.getItem("cart")) {
      return JSON.parse(localStorage.getItem("cart"));
    }
  }
}

export const removeItemFromCart = (productId) => {
  let cart = [];
  if (typeof windows !== undefined) {
    if (localStorage.getItem("cart")) {
      cart = JSON.parse(localStorage.getItem("cart"));
    }

    cart.map((product, i) => {
      if (product._id === productId) {
        cart.splice(i, 1);
      }
    });

    localStorage.setItem("cart", JSON.stringify(cart));
  }
  return cart;
}

export const cartEmpty = next => {
  if (typeof windows !== undefined) {
    localStorage.removeItem("cart");
    let cart = [];
    localStorage.setItem("cart", JSON.stringify(cart));
    next();
  }
}