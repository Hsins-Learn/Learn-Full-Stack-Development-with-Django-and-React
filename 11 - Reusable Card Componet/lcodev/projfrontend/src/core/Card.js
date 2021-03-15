import React from 'react'
import ImageHelper from "./helper/imageHelper";
import { Redirect } from "react-router-dom"

// TODO: Deal with this later
const isAuthenticated = true

const Card = ({
  product,
  addtoCard = true,
  removeFromCart = false,
}) => {
  const cardTitle = product ? product.name : "A photo from pexels";
  const cardDescription = product ? product.description : "Default description";
  const cardPrice = product ? product.price : "Default";

  const addToCart = () => {
    if (isAuthenticated) {
      console.log("Added to cart!");
    } else {
      console.log("Login Please!");
    }
  };

  const getRedirect = (redirect) => {
    if (redirect) {
      return <Redirect to="/cart" />
    }
  }

  const showAddToCart = addToCart => {
    return (addToCart && (
      <button
        onClick={addToCart}
        className="btn btn-block btn-outline-success mt-2 mb-2"
      >
        Add to Cart
      </button>))
  }

  const showRemoveFromCart = removeFromCart => {
    return (
      removeFromCart && (
        <button
          onClick={() => {
            // TODO: handle this
            console.log("Product removed from cart");
          }}
          className="btn btn-block btn-outline-danger mt-2 mb-2"
        >
          Remove from cart
        </button>
      )
    )
  }

  return (
    <div className="card text-white bg-dark border border-info ">
      <div className="card-header lead">{cardTitle}</div>
      <div className="card-body">
        <ImageHelper product={product} />
        <p className="lead bg-success font-weight-normal text-wrap">
          {cardDescription}
        </p>
        <p className="btn btn-success rounded  btn-sm px-4">$ {cardPrice}</p>
        <div className="row">
          <div className="col-12">
            {showAddToCart(addToCart)}
          </div>
          <div className="col-12">
            {showRemoveFromCart(removeFromCart)}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Card