import { Button } from "antd";
import { useNavigate } from "react-router-dom";
import { NotFound } from '../../components/not-found/not-found';
import { useTranslation } from 'react-i18next';
import "./wiki-not-found.css";

const NotFoundPage = ({status_code, error_message = "", resource_type = "Resource"}) => {
    const {t} = useTranslation();
    const navigate = useNavigate();

    const return_to_main = () => {
        if (resource_type=="Article"){
            //Article Not Found returns to Wiki Main Page
            navigate(location.pathname.split("/articles")[0]);
        }else{
            navigate("/");
        }
    }

    const go_back = () => {
        navigate(-1);
    }

    return (
    <div className="not-found-content">
    <NotFound status_code={status_code} resource_type={resource_type} error_message={error_message}>
    </NotFound>
    <div id="not-found-buttons">
        <Button onClick={return_to_main} type="primary">{resource_type=="Article"? t("common.back-to-wiki-main-page"):t("common.back-to-main-page")}</Button>
        <Button onClick={go_back}>{t("common.back-to-previous-page")}</Button>
    </div>
    </div>
    );
}
  
export default NotFoundPage;