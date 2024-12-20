import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import { CacheSwitch, CacheRoute } from 'react-router-cache-route';

import MainPage from './pages/MainPage/MainPage';
import ProfilePage from './pages/ProfilePage/ProfilePage';
import RestaurantPage from './pages/RestaurantPage/RestaurantPage';
import AddAddressPage from "./pages/AddAddressPage/AddAddressPage";



const App = ({}) => {
  return (
    <Router>
      <CacheSwitch>
        <CacheRoute exact path={["/", "/main"]} component={MainPage} />
        <Route path="/profile" component={ProfilePage} />
        <Route path="/restaurant/:id" component={RestaurantPage} />
        <Route path="/addAddress" component={AddAddressPage} />
      </CacheSwitch>
    </Router>
  );
};

export default App;