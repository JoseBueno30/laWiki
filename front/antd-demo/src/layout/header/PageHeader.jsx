import "./PageHeader.css";
import { Layout } from "antd";
import MainHeader from "./MainHeader";
import WikiHeader from "./WikiHeader";

const PageHeader = () => {
  return (
    <Layout.Header className="app-header">
      {/* Coger path del url para saber qué header mostrar */}
      {/* <MainHeader /> */}
      <WikiHeader />
    </Layout.Header>
  );
};

export default PageHeader;
