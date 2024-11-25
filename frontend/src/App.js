import { useState } from "react"
import logo from "./logo192.png"


export const App = () => {
  var baseUrl = window.location.hostname === "localhost" ? "http://127.0.0.1:5000" : ""
  const [file, setFile] = useState(null)
  const [error, setError] = useState(false)

  const handleLearning = imageFile => {
    setError(false); setFile(imageFile)

    let formData = new FormData()
    formData.append('file', imageFile)

    fetch(`${baseUrl}/api/start`, {
      method: "POST",
      mode: "cors",
      headers: {
        "Origin": window.location.hostname === "localhost"
          ? "http://localhost:3000"
          : "https://rag-agent-system-chrome-extention.vercel.app",
        "Access-Control-Request-Method": "POST, OPTIONS",
        "Access-Control-Request-Headers": "*",
      },
      body: formData
    })
      .then(res => {
        console.log(res)
        if (res.ok === false) { setError(true); setFile(null) }
        // else {
        // }
      })
      .catch(err => { setError(true); setFile(null) })
  }


  return (
    <div className="container content">
      <nav className="navbar" role="navigation" aria-label="main navigation">
        <div className="navbar-brand">
          <a className="navbar-item" href="/">
            AI Learning Assistant <img src={logo} alt="logo" />
          </a>
          <div role="button" className="navbar-burger" aria-label="menu" aria-expanded="false">
            <span aria-hidden="true" style={{ backgroundColor: "black" }}></span>
            <span aria-hidden="true" style={{ backgroundColor: "black" }}></span>
            <span aria-hidden="true" style={{ backgroundColor: "black" }}></span>
            <span aria-hidden="true" style={{ backgroundColor: "black" }}></span>
          </div>
        </div>
      </nav>

      <hr style={{ width: "100%", margin: 0 }} />

      <div className="section">

        <div className="file has-name" style={{ width: "800px", marginBottom: 0 }}>
          <label className="file-label">
            <input className="file-input" type="file" name="textbook" onChange={e => handleLearning(e.target.files[0])} />
            <span className="file-cta">
              <span className="file-label"> Upload an image... </span>
            </span>
            <span className="file-name" style={{ width: "500px" }}>{file ? file?.name : ""}</span>
          </label>
        </div>
        <p style={{ fontSize: "14px" }}>Format: jpg, jpeg, png, pdf, gif</p>
        {error && <p>Something went wrong.</p>}

      </div>
    </div>
  )
}