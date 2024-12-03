import "./PageHeader.css";
import { Layout } from "antd";
import MainHeader from "./MainHeader";
import WikiHeader from "./WikiHeader";
import { WikiContext } from "../../context/wiki-context";

import { useContext } from "react";

const PageHeader = () => {
  const { wiki } = useContext(WikiContext);

  return (
    <Layout.Header className="app-header">
      {wiki && wiki.wiki_info ? (
        <WikiHeader wiki_name={wiki.wiki_name} wiki={wiki.wiki_info} />
      ) : (
        <MainHeader />
      )}
    </Layout.Header>
  );
};

export default PageHeader;
