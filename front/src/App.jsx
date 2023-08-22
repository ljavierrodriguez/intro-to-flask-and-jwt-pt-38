import { useState } from 'react'
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './App.css'

function App() {

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [currentUser, setCurrentUser] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();

    login({ username: username, password: password })

  }

  const login = async (credenciales) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/login', {
        method: 'POST',
        body: JSON.stringify(credenciales),
        headers: {
          'Content-Type': 'application/json'
        }
      })

      const data = await response.json();
      console.log(data);

      if (data.fail) {
        toast.error(data.fail);
      } else {
        toast.success(data.success)
        setCurrentUser(data)
        setUsername("")
        setPassword("")

        /* En cual deberia guardar la informacion sessionStorage o localStorage */

      }


    } catch (error) {
      console.log(error.message)
    }
  }

  const profile = async (token) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/profile', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      })

      const data = await response.json();
      console.log(data);

    } catch (error) {
      console.log(error.message)
    }
  }

  const style = {
    width: '400px',
    display: 'flex',
    flexDirection: 'column',
    padding: '10px',
    margin: '10px auto'
  }

  const inputStyle = {
    padding: '5px',
    margin: '5px'
  }

  return (
    <div>

      {
        !!currentUser ? (
          <>
            <h1>{currentUser.user.username}</h1>
            {/* <h4>{currentUser.access_token}</h4> */}
            <button onClick={() => profile(currentUser.access_token)}>
              Obtener Profile
            </button>
          </>
        ) : (
          <form style={style} onSubmit={handleSubmit}>
            <input type="email" name="username" id="username" placeholder='Username' style={inputStyle} value={username} onChange={e => setUsername(e.target.value)} autoComplete='off' />
            <input type="password" name='password' id='password' placeholder='Password' style={inputStyle} value={password} onChange={e => setPassword(e.target.value)} autoComplete='off' />
            <button>Login</button>
          </form>
        )
      }


      <ToastContainer />
    </div>
  )
}

export default App
