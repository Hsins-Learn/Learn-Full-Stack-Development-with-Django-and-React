import React from 'react';
import { BrowserRouter, Switch, Route } from 'react-router-dom';

import Home from './core/Home';
import PrivateRoutes from "./auth/helper/PrivateRoutes";

const Routes = () => {
  return (
    <BrowserRouter>
      <Switch>
        <Route path="/" exact component={Home} />
        {/* <PrivateRoutes path="/user/dashboard" exact component={ } /> */}
      </Switch>
    </BrowserRouter>
  );
};

export default Routes;
