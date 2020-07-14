import React from 'react';
import superagent from 'superagent'

import './App.css';
import "antd/dist/antd.css";

import WebcamCapture from './components/WebcamCapture'
import Result from './components/Result'
import { Button } from 'antd';

function App() {
  const [img, setImg] = React.useState(null)
  const [showModal, setShowModal] = React.useState(false)
  const [result, setResult ] = React.useState(null)
  const [checkingData, setCheckingData] = React.useState({
    examId: "123",
    values: ["D","C","A","B","B","C","A","B","C","D","A","C","A","D","B","C","B","D","A","C","A","C","B","D","A","A","C","A","B","C","C","B","D","A","D","B","C","A","D","C","D","C","B","C","A","A","A","B","C","D"]
  })

  const [point, setPoint] = React.useState(0)

  const handleSendImage = async () => {
    if (!img)
      return

    setShowModal(true)
    let form_data = new FormData();
    form_data.append('image', img)

    const data = await superagent.post('/api/upload_image').send(form_data)
  
    const { examId, studentId, values, errorCode } = data.body

    if (errorCode == 500) {
      setResult({ error: 500 })
      return
    } 

    let p = 0;
    let wrongs = []
    for(let i = 0; i < values.length; i++) {
      if(values[i] == checkingData.values[i]) {
        p++
      } else {
        wrongs.push(i)
      }
    }

    setPoint(p)
    setResult({ examId, studentId, values, wrongs, expected_results: checkingData.values })
  }

  const handleCancel = () => {
    window.location.reload()
  }

  return (
    <div className="App">
      <WebcamCapture onCapture={(img) => setImg(img)} />
      <Button type="primary" onClick={handleSendImage}>
        Send
      </Button>
      <Result showModal={showModal} result={result} onCancel={handleCancel} point={point} />
    </div>
  );
}

export default App;
