import { Layout } from "antd";
import { Outlet } from "react-router-dom";
import PageHeader from "./header/PageHeader";

// El layout principal de la aplicación
// Contiene el header y el contenido de la página
// El contenido de la página se renderiza en el Outlet

const RootLayout = () => (
    <Layout className="app-layout">
      <PageHeader />
      <Layout.Content className="app-content">
        <Outlet />
      </Layout.Content>
    </Layout>
);

export default RootLayout;