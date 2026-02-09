import { useState } from 'react'
import { Search, Loader2, BookOpen, Sparkles, MessageSquare } from 'lucide-react'
import './App.css'

function App() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [answer, setAnswer] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [searched, setSearched] = useState(false)

  const handleSearch = async () => {
    if (!query.trim()) return;

    setLoading(true)
    setError(null)
    setResults([])
    setAnswer('')
    setSearched(true)

    try {
      const response = await fetch(`http://127.0.0.1:8000/search?query=${encodeURIComponent(query)}`)
      if (!response.ok) throw new Error('Failed to connect to the knowledge base')
      const data = await response.json()
      setResults(data.results || [])
      setAnswer(data.answer) // Don't default to "No answer generated" so we can hide UI
    } catch (err) {
      setError('Could not retrieve answers. Please ensure the backend is running.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <div className="background-gradient"></div>

      <main className="main-content">
        <header className="header">
          <div className="logo">
            <Sparkles className="icon-sparkle" />
            <h1>SIRL <span className="highlight">Explorer</span></h1>
          </div>
          <p className="subtitle">Unlock knowledge from the SIRL paper with AI-powered search</p>
        </header>

        <div className="search-section">
          <div className="search-bar-wrapper">
            <Search className="search-icon" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask a question..."
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
              className="search-input"
            />
            <button
              onClick={handleSearch}
              disabled={loading || !query.trim()}
              className="search-button"
            >
              {loading ? <Loader2 className="animate-spin" /> : 'Search'}
            </button>
          </div>
        </div>

        {error && (
          <div className="error-message">
            <p>{error}</p>
          </div>
        )}

        {loading && (
          <div className="loading-state">
            <Loader2 className="animate-spin-large" />
            <p>Analyzing documents and generating answer...</p>
          </div>
        )}

        {!loading && searched && (
          <div className="results-section">

            {answer && (
              <div className="answer-card">
                <div className="card-header">
                  <MessageSquare className="card-icon highlight-icon" />
                  <h3>AI Assist Answer</h3>
                </div>
                <div className="card-content answer-content">
                  <p>{answer}</p>
                </div>
              </div>
            )}

            {results.length > 0 && (
              <div className="sources-list">
                <h4 className="section-title">Sources & Context</h4>
                <div className="results-grid">
                  {results.map((result, index) => (
                    <div key={index} className="result-card" style={{ animationDelay: `${index * 0.1}s` }}>
                      <div className="card-header">
                        <BookOpen className="card-icon" />
                        <h3>Source {index + 1}</h3>
                        <span className="page-badge">Page {result.page}</span>
                      </div>
                      <div className="card-content">
                        <p>{result.content}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {results.length === 0 && !error && (
              <div className="empty-state">
                <p>No relevant information found. Try a different question.</p>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  )
}

export default App
