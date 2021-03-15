import React from 'react';
import { BrowserRouter, Switch, Route } from 'react-router-dom';

import Home from './core/Home';
import Signup from './user/SignUp';
import Signin from './user/SignIn';
import PrivateRoutes from "./auth/helper/PrivateRoutes";
import UserDashboard from './user/UserDashboard';

const Routes = () => {
  return (
    <BrowserRouter>
      <Switch>
        <Route path="/" exact component={Home} />
        <Route path="/signup" exact component={Signup} />
        <Route path="/signin" exact component={Signin} />
        <PrivateRoutes path="/user/dashboard" exact component={UserDashboard} />
      </Switch>
    </BrowserRouter>
  );
};

export default Routes;
