import "./App.css";
import { Layout } from "antd";
import PageHeader from "./layout/header/PageHeader";
import UserAvatar from "./modules/wiki/avatar/user-avatar";
import RoleAvatar from "./modules/wiki/avatar/role-avatar";
import Article from './modules/articles/components/article/article';
import ArticleList from "./modules/articles/components/article-list/article-list";
 
function App() {
  // Sólo muestra el header con un contenido random
  // Todo el contenido debe ser children del header

  const article = [
    {
      id: "673e4ff8eb2c93347976b0df",
      title: {
        en: "Parkway Drive",
        es: "Parkway Drive",
        fr: "Parkway Drive"
      },
      author: {
        name: "EdgyBoy",
        image: "itachi.png",
        id: "672901e41a1c2dc79c930ded"
      },
      tags: [
        {
          tag: {
            en: "Tag 3",
            es: "Tag 3",
            fr: "Tag 3"
          },
          id: "67310684be72ea3d639689b2"
        }
      ],
      wiki_id: "672c8721ba3ae42bd5985361",
      lan: "es",
      translate_title: false,
      creation_date: "2024-11-20",
      rating: 4.75,
      versions: [
        {
          title: {
            en: "Parkway Drive",
            es: "Parkway Drive",
            fr: "Parkway Drive"
          },
          author: {
            name: "EdgyBoy",
            image: "itachi.png",
            id: "672901e41a1c2dc79c930ded"
          },
          lan: "es",
          translate_title: false,
          modification_date: "2024-11-20T22:09:13.574Z",
          id:  "673e4ff9eb2c93347976b0e0"
        }
      ]
    },
    {
      id: "673e4ff8eb2c93347976b0df",
      title: {
        en: "ARTICULO 2",
        es: "AR \n  TICULOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO",
        fr: "Parkway Drive"
      },
      author: {
        name: "ADRIDUTY",
        image: "itachi.png",
        id: "672901e41a1c2dc79c930ded"
      },
      tags: [
        {
          tag: {
            en: "Tag 3",
            es: "Tag 3",
            fr: "Tag 3"
          },
          id: "67310684be72ea3d639689b2"
        }
      ],
      wiki_id: "672c8721ba3ae42bd5985361",
      lan: "es",
      translate_title: false,
      creation_date: "2024-11-20",
      rating: 0.75,
      versions: [
        {
          title: {
            en: "Parkway Drive",
            es: "Parkway Drive",
            fr: "Parkway Drive"
          },
          author: {
            name: "EdgyBoy",
            image: "itachi.png",
            id: "672901e41a1c2dc79c930ded"
          },
          lan: "es",
          translate_title: false,
          modification_date: "2024-11-20T22:09:13.574Z",
          id:  "673e4ff9eb2c93347976b0e0"
        }
      ]
    },
  ]

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
          {/* <h1>{article[0].id}</h1> */}
          <ArticleList articleList={article}/>
        </Layout.Content>
      </Layout>
    </>
  );
}

export default App;
