
import React, { useState } from 'react';
import Signup from './components/SignUp.jsx';
import Signin from './components/SignIn.jsx';
import Chat from './components/Chat.jsx';

function App() {
  const [page, setPage] = useState('signin');
  const [token, setToken] = useState('');

  const switchPage = (p) => setPage(p);
  const logout = () => {
    setToken('');
    switchPage('signin');
  };

  return (
    <div className="">
      <div className="">
        {page === 'signup' && <Signup switchPage={switchPage} />}
        {page === 'signin' && <Signin switchPage={switchPage} setToken={setToken} />}
        {page === 'chat' && <Chat token={token} logout={logout} />}
      </div>

      
    </div>
  );
}

export default App;  