import './App.css'
import { Layout } from "antd";
import PageHeader from './layout/header/PageHeader'

function App() {
  // Sólo muestra el header con un contenido random
  // Todo el contenido debe ser children del header
  return (
    <>
    
    <Layout className="app-layout">
      <PageHeader/>

      <Layout.Content className="app-content">
        <h1>Contenido</h1>
      </Layout.Content>

    </Layout>
      
    </>
  )
}

export default App
