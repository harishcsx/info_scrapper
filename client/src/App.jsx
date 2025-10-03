import { useState } from 'react'
import './App.css'

function App() {
  const [txt, setTxt] = useState("")
  const [data, setData] = useState([])

  async function queryHandler() {
      const res = await fetch("https://info-scrapper.onrender.com", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({query: txt}) 
      })
      const data = await res.json();
      console.log(data);
      setData(data['data']);
  }
  return (
    <>
      <input type="text" placeholder='enter query: ' onChange={(e) => {setTxt(e.target.value)}} />
      <button onClick={queryHandler}>Enter</button>
  
      if (data) {
         <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Contact</th>
              
            </tr>
          </thead>
          <tbody>
            {data.map((row) => (
              <tr key={row.id}>
                <td>{row.name}</td>
                <td>{row.ph_no}</td>
              </tr>
            ))}
          </tbody>
        </table>
      }
    </>
  )
}

export default App
