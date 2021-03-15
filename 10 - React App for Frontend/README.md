# Section 10: React App for Frontend

- [Configs for Backend Connection and Structure](#configs-for-backend-connection-and-structure)
- [Getting All Products from Backend](#getting-all-products-from-backend)
- [Getting All T-shirt Name in Frontend](#getting-all-t-shirt-name-in-frontend)
- [Image Helper for Card](#image-helper-for-card)

## Configs for Backend Connection and Structure

We have got our APIs already and we need to build up the frontend that can call through those APIs and receive those things. First, we're going to create the React frontend project and install the dependencies.

```bash
# create the React project
$ npx create-react-app projfrontend

# install the dependencies
$ cd projfrontend
$ npm install react-router-dom
$ npm install braintree-web-drop-in-react
$ npm install query-string
```

After installation, we should handle our frontend part as the strcture shown below by create files and folders.

```
.
├── App.js
├── auth
│   ├── helper
│   │   ├── PrivateRoutes.js
│   │   └── ...
│   ├── index.js
│   └── ...
├── core
│   ├── helper
│   │   ├── cartHelper.js
│   │   └── ...
│   ├── Base.js
│   ├── Card.js
│   ├── Cart.js
│   ├── Home.js
│   ├── Menu.js
│   ├── Payment.js
│   └── ...
├── user
│   ├── helper
│   │   ├── userapicalls.js
│   │   └── ...
│   ├── Profile.js
│   ├── SignIn.js
│   ├── SignUp.js
│   ├── UserDashboard.js
│   └── ...
├── style.css
├── backend.js
├── index.js
├── Routes.js
└── ...
```

Now we can start the frontend server by following commands:

```bash
$ npm start
```

<br/>
<div align="right">
  <b><a href="#section-10-react-app-for-frontend">[ ↥ Back To Top ]</a></b>
</div>
<br/>

## Getting All Products from Backend

To get all products from backend, what we need to do in the frontend is sending the request to that APIs. Let's edit the `coreapicalls.js` by adding following code:

```javascript
import { API } from '../../backend';

export const getProducts = () => {
  return fetch(`${API}/product`, { method: 'GET' })
    .then((response) => {
      return response.json();
    })
    .catch((err) => console.log(err));
};
```

<br/>
<div align="right">
  <b><a href="#section-10-react-app-for-frontend">[ ↥ Back To Top ]</a></b>
</div>
<br/>

## Getting All T-shirt Name in Frontend

We want the request to send before the component mounts up so that when the page actually loads up, users can see all of the things directly. In order to do so, we need to have a hook there and it's almost like an life-cycle event.

```javascript
import React, { useState, useEffect } from 'react';
import { getProducts } from './helper/coreapicalls';

export default function Home() {
  const [products, setProducts] = useState([]);
  const [error, setError] = useState(false);

  const loadAllProducts = () => {
    getProducts().then((data) => {
      if (data.error) {
        setError(data.error);
        console.log(error);
      } else {
        setProducts(data);
      }
    });
  };

  useEffect(() => {
    loadAllProducts();
  }, []);

  return (
    <div>
      <h1>Home Component</h1>
      <div className="row">
        {products.map((product, index) => {
          return (
            <div key={index}>
              <h1>{product.name}</h1>
            </div>
          );
        })}
      </div>
    </div>
  );
}
```

<br/>
<div align="right">
  <b><a href="#section-10-react-app-for-frontend">[ ↥ Back To Top ]</a></b>
</div>
<br/>

## Image Helper for Card

Before we go to the next section, let's edit the `imageHelper.js` for handle the url of each image and group then into a container.

```javascript
import React from 'react';

const ImageHelper = ({ product }) => {
  const imageUrl = product ? product.image : 'https://i.imgur.com/z7EiIyZ.jpg';
  return (
    <div className="rounded border border-success p-2">
      <img
        src={imageUrl}
        style={{ maxHeight: '100%', maxWidth: '100%' }}
        className="mb-3 rounded"
        alt=""
      />
    </div>
  );
};

export default ImageHelper;
```


<br/>
<div align="right">
  <b><a href="#section-10-react-app-for-frontend">[ ↥ Back To Top ]</a></b>
</div>
<br/>