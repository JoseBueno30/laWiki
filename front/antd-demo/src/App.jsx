import './App.css'
import PageHeader from './layout/PageHeader'

function App() {
  // Sólo muestra el header con un contenido random
  // Todo el contenido debe ser children del header
  return (
    <>
      <PageHeader>
        <h1>Contenido</h1>
      </PageHeader>
    </>
  )
}

export default App
