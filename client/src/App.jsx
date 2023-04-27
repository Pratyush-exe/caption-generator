import './App.css'
import axios from 'axios'
import { useState } from 'react'
import ReactImageFileToBase64 from 'react-file-image-to-base64'

function App() {
  const [images, setImages] = useState([])
  const [loc, setLoc] = useState("")
  const [occ, setOcc] = useState("")
  const [vibe, setVibe] = useState("")
  const [person, setPerson] = useState("first")
  const [useImage, setUseImage] = useState(false)
  const [details, setDetails] = useState("")
  const [showLoading, setShowLoading] = useState(false)
  const [captions, setCaptions] = useState([])

  const handleClick = () => {
    setShowLoading(true)
    document.getElementsByTagName("input")[0].click()
  }

  const handleChange = (files) => {
    console.log(files)
    setImages(files)
    setShowLoading(false)
  }

  const handleGenerate = async () => {
    setShowLoading(true)
    const body = {
      images,
      location: loc,
      occasion: occ,
      details,
      vibe,
      useImage,
      person
    }
    console.log(body)
    let start = Date.now();
    if (images.length > 0) {
      const response = await axios.post("http://127.0.0.1:5000/generate_captions", body)
      console.log(response.data.result.choices)
      setCaptions(response.data.result.choices)
    } else alert("Images are not choosen!")
    setShowLoading(false)
    let timeTaken = Date.now() - start;
    alert("Total time taken : " + timeTaken/1000 + " seconds");
  }

  return (
    <div className='app'>
      { showLoading && <div className="loadingSpinnerContainer"> <div className="loadingSpinner"> </div> </div> }
      <h1>✒️ Caption Generator</h1>
      <div className='image-cont-main'>
        <div className="img-cont">
          {images.map((im, i) => {
          return (
            <img className='image' key={i} src={im["base64_file"]} />
          )})}
        </div>
        <div className='button-container'>
          <button className='upload-image' onClick={handleClick}>Upload Images</button>
          <button className='generate-caption' onClick={handleGenerate}>Generate Captions</button>
        </div>
      </div>
      <ReactImageFileToBase64 multiple={true} onCompleted={handleChange}/>
      <div className='caption-cont'>
          <div className='input-cont'>
            <input className='text-input' onChange={(e)=>setLoc(e.target.value)} type='text' placeholder='Location' />
            <input className='text-input' onChange={(e)=>setOcc(e.target.value)} type='text' placeholder='Occasion' />
            <input className='text-input' onChange={(e)=>setVibe(e.target.value)} type='text' placeholder='Vibe' />
            <div className='text-input'>
              <input id="checkbox" checked={useImage} className='text-input' onChange={()=>setUseImage(!useImage)} type='checkbox'/> 
              <p onClick={()=>{document.getElementById("checkbox").click()}}>Use Image text?</p>
            </div>
            <select onChange={(e) => setPerson(e.target.value)} className='text-input'>
              <option value="first">1st person</option>
              <option value="second">2nd person</option>
              <option value="third">3rd person</option>
            </select>
            <textarea className='text-input' onChange={(e)=>setDetails(e.target.value)} style={{height: 'inherit', paddingTop: "5px"}} type='text' placeholder='More details' />
          </div>
          <div className='display-cont'>
            {captions.map((caption, i) => (
              <div key={i} className='caption'>
                <div style={{height:"80%", overflowY: "scroll"}}><p>{caption.text}</p></div>
                <button 
                  className='copy-button'
                  onClick={()=>{navigator.clipboard.writeText(caption.text).then(()=>alert("Caption copied to clipboard"))}
                }>Copy</button>
              </div>
            ))}
          </div>
      </div>
    </div>
  )
}

export default App
