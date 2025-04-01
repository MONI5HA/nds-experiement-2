import { useEffect, useState } from "react";

function App() {
  const [tab, setTab] = useState(0);
  const [logs, setLogs] = useState([]);
  const [error, setError] = useState(false);
  const [jwt, setJwt] = useState(null);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [username, setUsername] = useState("");
  const [loading, setLoading] = useState(false);

  async function fetchLogs() {
    fetch("http://127.0.0.1:5000/api/logs", {
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then(res => res.json())
      .then(response => {
        setLogs(response.data || []);
      });
  }
  useEffect(() => {
    fetchLogs();
  }, []);

  const login = () => {
    if (!email || !password) {
      return alert("Fill all the fields");
    }
    setLoading(true);
    fetch("http://127.0.0.1:5000/api/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    })
      .then(res => res.json())
      .then(response => {
        if (response?.message === "DECOY") {
          setError(true);
          setPassword("");
        } else if (response?.message === "Incorrect Password") {
          setError(true);
          setPassword("");
        } else {
          setJwt(response?.token);
          setTab(-1);
          setEmail("");
          setPassword("");
          setUsername("");
        }
      })
      .catch(err => console.log(err))
      .finally(() => setLoading(false));
  };

  const register = () => {
    if (!email || !password || !username) {
      return alert("Fill all the fields");
    }
    setLoading(true);
    fetch("http://127.0.0.1:5000/api/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, username, password }),
    })
      .then(res => res.json())
      .then(response => {
        alert("User Account Registered!");
        setEmail("");
        setPassword("");
        setUsername("");
        setTab(0);
      })
      .catch(err => console.log(err))
      .finally(() => setLoading(false));
  };

  return (
    <div className="w-full h-screen flex flex-col items-center justify-center bg-white">
      {tab === 0 ? (
        <div className="w-1/4 mx-auto flex flex-col items-center space-y-4">
          <h2 className="w-full text-center text-lg text-black py-2">
            Protected by{" "}
            <span className="text-white bg-blue-500 rounded-md font-medium px-2 py-1">
              Honeywords 🐝
            </span>
          </h2>
          <input
            value={email}
            onChange={e => setEmail(e.target.value)}
            type="email"
            autoComplete="dfsd"
            className="w-full p-2 outline-none bg-gray-100 rounded-md"
            placeholder="Email Address"
          />
          <input
            onFocus={() => setError(false)}
            value={password}
            onChange={e => setPassword(e.target.value)}
            type="password"
            autoComplete="sdfdsf"
            className="w-full p-2 outline-none bg-gray-100 rounded-md"
            placeholder="Password"
          />
          {error && (
            <p className="w-full text-red-500 font-medium text-left text-md">
              Password is incorrect
            </p>
          )}
          <button
            onClick={() => login()}
            className="w-full bg-black rounded-md text-white text-center py-2 px-3 cursor-pointer hover:bg-gray-800"
          >
            {loading ? "Please Wait..." : "Sign In"}
          </button>
          <p
            onClick={() => {
              setTab(2)
              fetchLogs()  
            }}
            className="w-full text-center text-gray-500 hover:underline hover:text-pink-600 cursor-pointer"
          >
            View Authentication Logs
          </p>
          <p className="text-sm text-gray-400 text-center">(or)</p>
          <p
            onClick={() => setTab(1)}
            className="w-full text-center text-gray-500 hover:underline hover:text-pink-600 cursor-pointer"
          >
            Create Account
          </p>
        </div>
      ) : tab === 1 ? (
        <div className="w-1/4 mx-auto flex flex-col items-center space-y-4">
          <h2 className="w-full text-center text-lg text-black py-2">
            <span className="text-white bg-blue-500 rounded-md font-medium px-2 py-1">
              Honeywords 🐝
            </span>{" "}
            Expirement
          </h2>
          <input
            value={username}
            onChange={e => setUsername(e.target.value)}
            type="text"
            autoComplete="dfdf"
            className="w-full p-2 outline-none bg-gray-100 rounded-md"
            placeholder="Username"
          />
          <input
            value={email}
            onChange={e => setEmail(e.target.value)}
            type="email"
            autoComplete="fg"
            className="w-full p-2 outline-none bg-gray-100 rounded-md"
            placeholder="Email Address"
          />
          <input
            value={password}
            onChange={e => setPassword(e.target.value)}
            type="password"
            autoComplete="fhfh"
            className="w-full p-2 outline-none bg-gray-100 rounded-md"
            placeholder="Password"
          />
          <button
            onClick={() => register()}
            className="w-full bg-black rounded-md text-white text-center py-2 px-3 cursor-pointer hover:bg-gray-800"
          >
            {loading ? "Please Wait..." : "Register Account"}
          </button>
          <p
            onClick={() => {
              setTab(2)
              fetchLogs()  
            }}
            className="w-full text-center text-gray-500 hover:underline hover:text-pink-600 cursor-pointer"
          >
            View Authentication Logs
          </p>
          <p className="text-sm text-gray-400 text-center">(or)</p>
          <p
            onClick={() => setTab(0)}
            className="w-full text-center text-gray-500 hover:underline hover:text-pink-600 cursor-pointer"
          >
            Sign in into your Account
          </p>
        </div>
      ) : tab === 2 ? (
        <div className="w-full p-3 h-screen">
          <h2 className="w-full text-left text-lg text-black py-2 underline">
            Viewing System Logs
          </h2>
          <br />
          <table className="w-full border bg-white border-gray-500">
            <thead className="text-gray-800 py-2">
              <th className="border bg-gray-200">S.No.</th>
              <th className="border bg-gray-200">Email Address</th>
              <th className="border bg-gray-200">Origin IP</th>
              <th className="border bg-gray-200">Decoy Password Detected</th>
              <th className="border bg-gray-200">Updated At</th>
            </thead>
            <tbody className="border">
              {logs.map((log, index) => (
                <tr>
                  <td className="border text-center">{index + 1}.</td>
                  <td className="border text-center">{log[1]}</td>
                  <td className="border text-center">{log[2]}</td>
                  <td className="border text-center">
                    {log[3] ? "Yes" : "No"}
                  </td>
                  <td className="border text-center">{log[4]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="w-full p-3 h-screen flex items-center justify-center flex-col">
          <h1 className="text-black font-black text-center py-2 text-7xl">
            Hey! Good Morning 🐝
          </h1>
          <p className="max-w-md mx-auto flex flex-col items-center text-center text-black font-medium text-sm py-2">
            <span>JWT Token:</span> <span className="font-mono">{jwt}</span>
          </p>
        </div>
      )}
    </div>
  );
}

export default App;
