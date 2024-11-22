import "./App.css";
import { Layout } from "antd";
import PageHeader from "./layout/header/PageHeader";
import UserAvatar from "./modules/wiki/avatar/user-avatar";
import RoleAvatar from "./modules/wiki/avatar/role-avatar";
import Comment from "./modules/article/components/comment/comment";

function App() {
  // Sólo muestra el header con un contenido random
  // Todo el contenido debe ser children del header
  const comment = {
    id: "673101ecdfbf37502ca360e5",
    article_id: "672f950ef345b60e372e34d8",
    author: {
      id: "672272c65150a9cd3f46599e",
      name: "author_name",
      image: "author_image"
    },
    body: "COMENTARIO PRUEBA ART2 1",
    creation_date: "2024-11-08"
  }

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
          <Comment comment={comment}/>
        </Layout.Content>
      </Layout>
    </>
  );
}

export default App;
