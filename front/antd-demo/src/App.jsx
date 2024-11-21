import "./App.css";
import { Layout } from "antd";
import PageHeader from "./layout/header/PageHeader";
import UserAvatar from "./modules/wiki/avatar/user-avatar";
import RoleAvatar from "./modules/wiki/avatar/role-avatar";

function App() {
  // Sólo muestra el header con un contenido random
  // Todo el contenido debe ser children del header
  return (
    <>
      <Layout className="app-layout">
        <PageHeader />

        <Layout.Content className="app-content">
          <h1>Contenido</h1>
          <UserAvatar/>
          <RoleAvatar
            image="https://yt3.googleusercontent.com/qk8AlThEihBfAmEgkgJRnKG1sQbsuSDfG4ejMS8o_dxDBkVM_1sKIB4fsHoVDvj_w9gjoxO_jQ=s900-c-k-c0x00ffffff-no-rj"
            username="TheGrefg"
            role="Author"
          />
        </Layout.Content>
      </Layout>
    </>
  );
}

export default App;
