import { useState } from "react"
import logo from "./logo192.png"


export const App = () => {
  var baseUrl = "http://127.0.0.1:5000"
  const [file, setFile] = useState(null)
  const [isGenerating, setIsGenerating] = useState(false)
  const [error, setError] = useState(false)
  const [outcome, setOutcome] = useState(null)

  const handleLearning = async imageFile => {
    setError(false); setFile(imageFile); setIsGenerating(true)

    let formData = new FormData()
    formData.append('file', imageFile)


    await fetch(`${baseUrl}/api/start`, {
      method: "POST",
      mode: "cors",
      headers: {
        "Origin": window.location.origin,
        "Access-Control-Request-Method": "POST, OPTIONS",
        "Access-Control-Request-Headers": "*",
      },
      body: formData
    })
      .then(res => {
        if (res.ok === false) { setError(true); setFile(null); setIsGenerating(false) }
        else { return res.text() }
      })
      .then(res => {
        const res_obj = JSON.parse(JSON.parse(res)["text"])
        if (res_obj !== undefined) { setOutcome(res_obj?.groups[0]?.words); setIsGenerating(false) }
        else { setIsGenerating(false); setOutcome("Successfully processed.") }
      })
      .catch(err => { setError(true); setFile(null); setIsGenerating(false) })
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
        <p style={{ fontSize: "14px" }}>Format: jpg, jpeg, png</p>
        {isGenerating && <p>...processing...</p>}
        {error && <p>Something went wrong.</p>}
        {(outcome !== null && typeof outcome === String)
          ? <p>{outcome}</p>
          : outcome !== null && outcome.length > 0 ? outcome.map((item, i) => {
            const { word, meaning, sample } = item
            return (
              <div key={i}>
                <p>------</p>
                <p><span style={{ fontWeight: 700 }}>Vocabulary extracted: </span>{word}</p>
                <p><span style={{ fontWeight: 700 }}>Meaning: </span>{meaning}</p>
                <p><span style={{ fontWeight: 700 }}>Example: </span>{sample}</p>
              </div>
            )
          })
            : <></>
        }
      </div>
    </div >
  )
}