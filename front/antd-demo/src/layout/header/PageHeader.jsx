import PropTypes from "prop-types";
import "./PageHeader.css";
import { Layout } from "antd";
import MainHeader from "./MainHeader";
import WikiHeader from "./WikiHeader";


const PageHeader = () => {
  return (
    <Layout.Header className="app-header">
       {/* Coger path del url para saber qué header mostrar
       <MainHeader/> */}

      <WikiHeader/>
    </Layout.Header>
  );
};

PageHeader.propTypes = {
  children: PropTypes.node,
};

export default PageHeader;
