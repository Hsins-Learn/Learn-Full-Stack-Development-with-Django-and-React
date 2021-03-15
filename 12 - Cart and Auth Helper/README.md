# Section 12: Cart and Auth Helper

- [Adding Item to Cart Helper](#adding-item-to-cart-helper)
- [Load and Remove Items from Cart](#load-and-remove-items-from-cart)
  - [`loadCart` Method](#loadcart-method)
  - [`removeItemFromCart` Method](#removeitemfromcart-method)
  - [`cartEmpty` Method](#cartempty-method)
- [SignIn and SignUp Helpers.](#signin-and-signup-helpers)
  - [`signup` Method](#signup-method)
  - [`signup` Method](#signup-method-1)
- [Signout and Authenticated User](#signout-and-authenticated-user)
  - [`authenticate` Method](#authenticate-method)
  - [`isAuthenticated` Method](#isauthenticated-method)
  - [`signout` Method](#signout-method)
- [Handling Private Routes in React](#handling-private-routes-in-react)

## Adding Item to Cart Helper

When we're developing with separation of frontend and backend, we should keep the extremely separate from the component: "Components should just know about the method which is coming from somewhere and have no idea about who is talking to API."

Keeping the components in separate file make our code more robust as well as more scalable. In this section, we will have a couple of mothods which will be adding things into our cart. Let's edit the `cartHelper.js` file.

```javascript
export const addItemToCart = (item, next) => {
  let cart = [];
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
```

The `next` is a classic method in the JavaScript and especially in the React world where we use it to provide a callback functionality to anybody who is using this method. But all we care about here is it gives the user a functionality where he can add his own callback and can chain on other things that he want to do.

Furthermore, We can verify whether this is a browser or not by checking the window object. Note that the window object is available only in the browser.

In the end of this section, we can add the `addItemToCart` function to the `Card` component.

<br/>
<div align="right">
  <b><a href="#section-12-cart-and-auth-helper">[ ↥ Back To Top ]</a></b>
</div>
<br/>

## Load and Remove Items from Cart

Let's say that the user has made a purchase and we need to emptied the cart. In the case, we need to implement another method which will be emptied out the cart.

Now, we're going to add the `loadCart()`, `removeItemFromCart()` and `cartEmpty()` function to the `cartHelper.js` file.

### `loadCart` Method

```javascript
export const loadCart = () => {
  if (typeof windows !== undefined) {
    if (localStorage.getItem("cart")) {
      return JSON.parse(localStorage.getItem("cart"));
    }
  }
}
```

<br/>
<div align="right">
  <b><a href="#section-12-cart-and-auth-helper">[ ↥ Back To Top ]</a></b>
</div>
<br/>

### `removeItemFromCart` Method

```javascript
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
    })

    localStorage.setItem("cart", JSON.stringify(cart));
  }
  return cart;
}
```

Note that we can use `product._id` or `product._id` here, both of them are work well. It's a classic thing which is recently updated and escalate as well as in the MongoDB to keep the consistency with the majority (like in many of the modern databases).

<br/>
<div align="right">
  <b><a href="#section-12-cart-and-auth-helper">[ ↥ Back To Top ]</a></b>
</div>
<br/>

### `cartEmpty` Method

```javascript
export const cartEmpty = next => {
  if (typeof windows !== undefined) {
    localStorage.removeItem("cart");
    let cart = [];
    localStorage.setItem("cart", JSON.stringify(cart));
    next();
  }
}
```

<br/>
<div align="right">
  <b><a href="#section-12-cart-and-auth-helper">[ ↥ Back To Top ]</a></b>
</div>
<br/>

## SignIn and SignUp Helpers.

Our server is ready to make some of the post request where we can do things like signup, signin and signout. What are the things we receive from the server that we are running so that we can just storing it and returning it?

### `signup` Method

```javascript
export const signup = user => {
  return fetch(`${API}/user/`, {
    method: "POST",
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify(user)
  })
    .then((response) => response.json())
    .catch(err => console.log(err))
}
```

<br/>
<div align="right">
  <b><a href="#section-12-cart-and-auth-helper">[ ↥ Back To Top ]</a></b>
</div>
<br/>

### `signup` Method

```javascript
export const signin = user => {
  const formData = new FormData();

  for (const name in user) {
    formData.append(name, user[name]);
  }

  return fetch(`${API}/user/login/`, {
    method: "POST",
    body: FormData
  })
    .then(response => response.json())
    .catch(err => console.log(err))
}
```

<br/>
<div align="right">
  <b><a href="#section-12-cart-and-auth-helper">[ ↥ Back To Top ]</a></b>
</div>
<br/>

## Signout and Authenticated User

### `authenticate` Method

```javascript
export const authenticate = (data, next) => {
  if (typeof window !== undefined) {
    localStorage.setItem("jwt", JSON.stringify(data));
    next()
  }
}
```

<br/>
<div align="right">
  <b><a href="#section-12-cart-and-auth-helper">[ ↥ Back To Top ]</a></b>
</div>
<br/>

### `isAuthenticated` Method

```javascript
export const isAuthenticated = () => {
  if (typeof window == undefined) {
    return false;
  }

  if (localStorage.getItem("jwet")) {
    return JSON.parse(localStorage.getItem("jwt"));
  } else {
    return false;
  }
}
```

<br/>
<div align="right">
  <b><a href="#section-12-cart-and-auth-helper">[ ↥ Back To Top ]</a></b>
</div>
<br/>

### `signout` Method

```javascript
export const signout = next => {
  const userId = isAuthenticated() && isAuthenticated.user.id;

  if (typeof window !== undefined) {
    localStorage.removeItem("jwt");
    cartEmpty(() => { });

    return fetch(`${API}/user/logout/${userId}`, {
      method: "GET"
    })
      .then(response => {
        console.log("Signout success");
        next();
      })
      .catch(err => console.log(err));
  }
}
```

<br/>
<div align="right">
  <b><a href="#section-12-cart-and-auth-helper">[ ↥ Back To Top ]</a></b>
</div>
<br/>

## Handling Private Routes in React

The seciton we're going to talk about how we can restrict some of the routes. Route Restriction is one of the most important thing to do if our application is role based. Let's edit the `PrivateRoutes.js` file.

```javascript
const PrivateRoutes = ({ children, ...rest }) => {
  return (
    <Route {...rest}
      render={({ props }) =>
        isAuthenticated
          ? (<Component {...props} />)
          : (<Redirect to={{ pathname: "/signin", state: { from: props.location } }} />)
      } />
  )
}
```

Then we can add the `PrivateRoutes` to the `Routes.js`.

<br/>
<div align="right">
  <b><a href="#section-12-cart-and-auth-helper">[ ↥ Back To Top ]</a></b>
</div>
<br/>