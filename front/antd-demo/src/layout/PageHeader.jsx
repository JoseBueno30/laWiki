import PropTypes from "prop-types";
import "./PageHeader.css";
import MainHeader from "./MainHeader";
import WikiHeader from "./WikiHeader";


const PageHeader = ({ children }) => {
  return (
    // Coger path del url para saber qué header mostrar
    // <MainHeader>
    //     {children}
    // </MainHeader>

    <WikiHeader>
        {children}
    </WikiHeader>
  );
};

PageHeader.propTypes = {
  children: PropTypes.node,
};

export default PageHeader;
