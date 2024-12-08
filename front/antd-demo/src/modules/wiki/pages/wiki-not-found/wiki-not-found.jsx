import { Button } from "antd";
import { useNavigate } from "react-router-dom";
import { NotFound } from '../../components/not-found/not-found';
import "./wiki-not-found.css";

const NotFoundPage = ({status_code, error_message = "", resource_type = "Resource"}) => {
    const navigation = useNavigate();

    const return_to_main = () => {
        navigation("/");
    }

    const go_back = () => {
        navigation(-1);
    }

    return (
    <div className="not-found-content">
    <NotFound status_code={status_code} resource_type={resource_type} error_message={error_message}>
    </NotFound>
    <div id="not-found-botones">
        <Button onClick={return_to_main} type="primary">Back to Main Page</Button>
        <Button onClick={go_back}>Back to previous page</Button>
    </div>
    </div>
    );
}
  
export default NotFoundPage;