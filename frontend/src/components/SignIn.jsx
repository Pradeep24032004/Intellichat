import React from 'react';
import { signin } from '../api.js';
import './SignIn.css';

export default function Signin({ switchPage, setToken }) {
  const handleSignin = async (e) => {
    e.preventDefault();
    const { email, password } = e.target;
    try {
      const res = await signin({ username: email.value, password: password.value });
      localStorage.setItem('token', res.data.access_token);
      setToken(res.data.access_token);
      switchPage('chat');
    } catch (err) {
      alert(err.response?.data?.detail || 'Signin failed');
    }
  };

  return (
    <form onSubmit={handleSignin} className="">
      <h2 className="signin">Sign In</h2>
      <input name="email" type="email" placeholder="Email" className="input" required />
      <input name="password" type="password" placeholder="Password" className="input" required />
      <button type="submit" className="btn-signin">Sign In</button>
      <p className="text-sm text-center">Don't have an account? <span className="signup" onClick={() => switchPage('signup')}>Sign Up</span></p>
    </form>
  );
}