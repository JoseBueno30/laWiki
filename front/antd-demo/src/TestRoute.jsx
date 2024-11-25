import { useLocation } from "react-router-dom"
import { Button } from "antd"
import { useContext } from "react"
import { ThemeContext } from "./context/theme-context"

import ArticleList from "./modules/articles/components/article-list/article-list";
import WikiEditPage from "./modules/wiki/pages/wiki-edit-page/wiki-edit-page";
import ArticleEditPage from "./modules/articles/pages/article-edit-page/article-edit-page";

const TestRoute = () => {
    const {colorTheme, toggleTheme} = useContext(ThemeContext)

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

    let location = useLocation()
    return (
        <>
        
        <div>
            {/* <h1>{location.pathname}</h1>
            <Button onClick={toggleTheme}>
                Toggle theme
            </Button>
            <ArticleList articleList={article}/> */}
            {/* <WikiEditPage></WikiEditPage> */}
            <ArticleEditPage></ArticleEditPage>

        </div>
        </>
    )
}

export default TestRoute