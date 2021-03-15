# Section 13: Sign-in and Sign-Up Components

- [Create Sign-Up Component](#create-sign-up-component)
- [Create Sign-In Component](#create-sign-in-component)

## Create Sign-Up Component

```javascript
import React, { useState } from "react";
import Base from "../core/Base";
import { Link } from "react-router-dom";
import { signup } from "../auth";

const Signup = () => {
  const [values, setValues] = useState({
    name: "",
    email: "",
    password: "",
    error: "",
    success: false,
  })

  const { name, email, password, error, success } = values;

  const handleChange = (name) => (event) => {
    setValues({ ...values, error: false, [name]: event.target.value });
  }

  const onSubmit = (event) => {
    event.preventDefault();
    setValues({ ...values, error: false });
    signup({ name, email, password })
      .then((data) => {
        console.log("DATA", data);
        if (data.email === email) {
          setValues({ ...values, name: "", email: "", password: "", error: "", success: true })
        } else {
          setValues({ ...values, error: true, success: false })
        }
      })
      .catch(err => console.log(err))
  }

  const successMessage = () => {
    return (
      <div className="row">
        <div className="col-md-6 offset-sm-3 text-left">
          <div
            className="alert alert-success"
            style={{ display: success ? "" : "none" }}>
            New account created successfully. Please <Link to="/signin">login now</Link>!
          </div>
        </div>
      </div>
    )
  }

  const errorMessage = () => {
    return (
      <div className="row">
        <div className="col-md-6 offset-sm-3 text-left">
          <div
            className="alert alert-danger"
            style={{ display: error ? "" : "none" }}>
            Check all fields again!
          </div>
        </div>
      </div>
    )
  }

  const signUpForm = () => {
    return (
      <div className="row">
        <div className="col-md-6 offset sm-3 text-left">
          <form>
            <div className="form-group">
              <label className="text-light">Name</label>
              <input
                className="form-control"
                value={name}
                onChange={handleChange("name")}
                type="text" />
            </div>
            <div className="form-group">
              <label className="text-light">Email</label>
              <input
                className="form-control"
                value={email}
                onChange={handleChange("email")}
                type="text" />
            </div>
            <div className="form-group">
              <label className="text-light">Password</label>
              <input
                className="form-control"
                value={password}
                onChange={handleChange("password")}
                type="text" />
            </div>
            <button
              onClick={onSubmit}
              className="btn btn-success btn-block">Submit
            </button>
          </form>
        </div>
      </div >
    )
  }

  return (
    <Base title="Sign Up Page" description="A signup for LCO user">
      {successMessage()}
      {errorMessage()}
      {signUpForm()}
    </Base>
  );
}

export default Signup;
```

<br/>
<div align="right">
  <b><a href="#section-13-sign-in-and-sign-up-components">[ ↥ Back To Top ]</a></b>
</div>
<br/>

## Create Sign-In Component

```javascript
import React, { useState } from 'react';
import { Link, Redirect } from 'react-router-dom';
import { authenticate, isAuthenticated, signin } from '../auth';
import Base from '../core/Base';

const Signin = () => {
  const [values, setValues] = useState({
    name: '',
    email: '',
    password: '',
    error: '',
    success: false,
    loading: false,
    didRedirect: false,
  });

  const { email, password, error, success, loading, didRedirect } = values;

  const handleChange = (name) => (event) => {
    setValues({ ...values, error: false, [name]: event.target.value });
  };

  const onSubmit = (event) => {
    event.preventDefault();
    setValues({ ...values, error: false, loading: true });

    signin({ email, password })
      .then((data) => {
        console.log('DATA', data);
        if (data.token) {
          let sessionToken = data.token;
          authenticate(sessionToken, () => {
            console.log('TOKEN ADDED');
            setValues({
              ...values,
              didRedirect: true,
            });
          });
        } else {
          setValues({
            ...values,
            loading: false,
          });
        }
      })
      .catch((err) => console.log(err));
  };

  const peformRedirect = () => {
    if (isAuthenticated()) {
      return <Redirect to="/" />;
    }
  };

  const loadingMessage = () => {
    return (
      loading && (
        <div className="alert alert-info">
          <h2>Loading....</h2>
        </div>
      )
    );
  };

  const successMessage = () => {
    return (
      <div className="row">
        <div className="col-md-6 offset-sm-3 text-left">
          <div
            className="alert alert-success"
            style={{ display: success ? '' : 'none' }}
          >
            New account created successfully. Please{' '}
            <Link to="/signin">login now</Link>!
          </div>
        </div>
      </div>
    );
  };

  const errorMessage = () => {
    return (
      <div className="row">
        <div className="col-md-6 offset-sm-3 text-left">
          <div
            className="alert alert-danger"
            style={{ display: error ? '' : 'none' }}
          >
            Check all fields again!
          </div>
        </div>
      </div>
    );
  };

  const signInForm = () => {
    return (
      <div className="row">
        <div className="col-md-6 offset sm-3 text-left">
          <form>
            <div className="form-group">
              <label className="text-light">Email</label>
              <input
                className="form-control"
                value={email}
                onChange={handleChange('email')}
                type="text"
              />
            </div>
            <div className="form-group">
              <label className="text-light">Password</label>
              <input
                className="form-control"
                value={password}
                onChange={handleChange('password')}
                type="text"
              />
            </div>
            <button onClick={onSubmit} className="btn btn-success btn-block">
              Submit
            </button>
          </form>
        </div>
      </div>
    );
  };

  return (
    <Base title="Welcome to sign in page" description="A T-Shirt Store">
      {loadingMessage()}
      {signInForm()}
      <p className="text-center">Welcome to sign-in page</p>
      {peformRedirect()}
    </Base>
  );
};

export default Signin;
```

<br/>
<div align="right">
  <b><a href="#section-13-sign-in-and-sign-up-components">[ ↥ Back To Top ]</a></b>
</div>
<br/>