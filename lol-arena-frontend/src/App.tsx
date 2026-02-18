import { useState } from 'react'
import './App.css'

function App() {
  // State to hold the user's input
  const [riotId, setRiotId] = useState('')
  // State to hold the fetched data
  const [gameData, setGameData] = useState(null)
  // State for loading and error handling
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSearch = async () => {
    if (!riotId) return

    setLoading(true)
    setError(null)
    setGameData(null)

    try {
      // IMPORTANT: Riot IDs contain '#', which breaks URLs if not encoded.
      // encodeURIComponent converts '#' to '%23'
      const encodedId = encodeURIComponent(riotId)
      
      // Update this URL if your FastAPI backend is on a different port (e.g., 8000)
      const response = await fetch(`http://127.0.0.1:8000/games/${encodedId}`)

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`)
      }

      const data = await response.json()
      setGameData(data)
    } catch (err) {
      console.error(err)
      setError("Failed to fetch games. Is the backend running?")
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <h1>Riot Match Lookup</h1>
      
      <div className="card">
        <div style={{ marginBottom: '20px', display: 'flex', gap: '10px', justifyContent: 'center' }}>
          <input 
            type="text" 
            placeholder="Name#Tag" 
            value={riotId}
            onChange={(e) => setRiotId(e.target.value)}
            style={{ padding: '10px', fontSize: '16px' }}
          />
          <button onClick={handleSearch} disabled={loading}>
            {loading ? 'Loading...' : 'Search'}
          </button>
        </div>

        {error && <p style={{ color: 'red' }}>{error}</p>}

        {gameData && (
          <div style={{ textAlign: 'left', background: '#242424', padding: '15px', borderRadius: '8px', overflowX: 'auto' }}>
            <h3>Results:</h3>
            {/* Displaying raw JSON as requested */}
            <pre>{JSON.stringify(gameData, null, 2)}</pre>
          </div>
        )}
      </div>
    </>
  )
}

export default App