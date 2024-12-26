import { Layout } from "antd";
import { Outlet } from "react-router-dom";
import PageHeader from "./header/PageHeader";
import { WikiProvider } from "../context/wiki-context";
import { TokenProvider } from "../context/token-manager";

// El layout principal de la aplicación
// Contiene el header y el contenido de la página
// El contenido de la página se renderiza en el Outlet

const RootLayout = () => (
  <TokenProvider>
    <WikiProvider>
      <Layout className="app-layout">
        <PageHeader />
        <Layout.Content className="app-content">
          <Outlet />
        </Layout.Content>
      </Layout>
    </WikiProvider>
  </TokenProvider>
);

export default RootLayout;
