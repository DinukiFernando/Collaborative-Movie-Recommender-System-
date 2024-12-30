import React, { useState } from "react";
import axios from "axios";

const Login = ({ onLogin }) => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const handleLogin = async () => {
        try {
            const response = await axios.post("http://127.0.0.1:5000/api/login", { email, password });
            onLogin(response.data.token);
        } catch (error) {
            console.error("Login failed", error);
        }
    };

    return (
        <div>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
            <button onClick={handleLogin}>Login</button>
        </div>
    );
};

export default Login;
