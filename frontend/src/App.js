import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import ProfilePage from './pages/ProfilePage';

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/profile" component={ProfilePage} />
        <Route path="/user/:userId" component={OtherUserProfilePage} />
        <Route path="/mentors" component={MentorsListPage} /> {/* Mentors list page route */}
      </Switch>
    </Router>
  );
}

export default App;
