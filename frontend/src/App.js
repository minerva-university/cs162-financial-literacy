import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import ProfilePage from './pages/ProfilePage';

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/profile" component={ProfilePage} />
        {/* Add more routes here */}
      </Switch>
    </Router>
  );
}

export default App;
