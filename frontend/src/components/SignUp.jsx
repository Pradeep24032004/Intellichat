import React from 'react';
import { signup } from '../api';
import './SignUp.css';

export default function Signup({ switchPage }) {
  const handleSignup = async (e) => {
    e.preventDefault();
    const { username, email, password } = e.target;
    try {
      await signup({
        username: username.value,
        email: email.value,
        password: password.value,
      });
      alert('Signup successful! Please sign in.');
      switchPage('signin');
    } catch (err) {
      alert(err.response?.data?.detail || 'Signup failed');
    }
  };

  return (
    <form onSubmit={handleSignup} className="">
      <h2 className="signup">Sign Up</h2>
      <input name="username" placeholder="Username" className="input" required />
      <input name="email" type="email" placeholder="Email" className="input" required />
      <input name="password" type="password" placeholder="Password" className="input" required />
      <button type="submit" className="btn-signup">Sign Up</button>
      <p className="signin1">Already have an account? <span className="text-blue-500 cursor-pointer" onClick={() => switchPage('signin')}>Sign In</span></p>
    </form>
  );
}
