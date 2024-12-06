import { Button, Result } from "antd";
import { useNavigate } from "react-router-dom";
import "./wiki-not-found.css";

const NotFound = ({status_code, error_message = "", resource_type = "Resource"}) => {
    const navigation = useNavigate();
    let error_type = "", error_explanation = "", final_status_code;
    if (status_code == 404) {
        error_type = " - Not Found";
        final_status_code = 404;
        error_explanation = resource_type + " does not exist, it might have been deleted.";
    } else if (status_code >= 500) {
        error_type = " - Internal Server Error";
        final_status_code = 500;
        error_explanation = "We had a problem loading this page, try again later.";
    } else if (status_code == 403) {
        error_type = " - Forbidden";
        final_status_code = 403;
        error_explanation = "You are not authorized to access this page.";
    } else if (status_code >= 400 || status_code == null) { // Si no se le pasa asumirá 400
        error_type = " - Bad Request";
        final_status_code = "error"; // Para el icono
        error_explanation = "We cannot process this request, check request formatting.";
    } else { // Si es menor que 400 no llameis a esto
        error_type = " - Unexpexted exception";
        final_status_code = "info";
        error_explanation = "This error should not appear, or it has been asigned a bad status code.";
    }

    const return_to_main = () => {
        navigation("/");
    }

    const go_back = () => {
        navigation(-1);
    }

    return (
    <main className="not-found-content">
    <Result status={final_status_code} extra={error_message} title={status_code + error_type}subTitle={error_explanation}></Result>
    <div id="not-found-botones">
        <Button onClick={return_to_main} type="primary">Back to Main Page</Button>
        <Button onClick={go_back}>Back to previous page</Button>
    </div>
    </main>);
}
  
export default NotFound;