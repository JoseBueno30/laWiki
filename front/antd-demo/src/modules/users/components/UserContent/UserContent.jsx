import { Tabs, Tree } from "antd";
import WikiCardGrid from "../../../wiki/components/wiki-card-grid/wiki-card-grid";
import { useContext, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import SettingsContext from "../../../../context/settings-context";
import ArticleService from "../../../articles/service/article-service";

const { searchArticlesWithParams } = ArticleService();

//Las wikis funcionan
//He cambiado de idea de como hacer los articulos un monton de veces
//Hare que se llame a articles y se obtengan las wikis de los articulos
const UserContent = ({wikis=[], author_name=""}) => {
    const { t } = useTranslation();
    const { locale } = useContext(SettingsContext);
    const [offset, setOffset] = useState(0);
    const [limit, setLimit] = useState(20);
    const [order, setOrder] = useState("recent");
    const [articleTree, setATree] = useState([]);

    console.log(wikis);

    const initTreeData = () => {
        return wikis.map((wiki, i) => ({
            "title": wiki.name,
            "key": i+""
        }));
    }
    
    const getParams = (key) => {
        return {
            "wiki_id": wikis[key].id,
            "author_name": author_name,
            "lan": locale,
            "offset": offset,
            "limit": limit,
            "order": order
        }
    }

    const getArticles = (key) => {
        let articles = [];
        searchArticlesWithParams(getParams(key)).then((response) => {
            articles = response.articles;
            setOffset(offset + limit);
        });
        console.log(`Articles from ${wikis[key].name}: ` + articles);
        return articles;
    }

    const onLoadData = ({ key, children }) =>
        new Promise((resolve) => {
            if (children) {
                resolve();
                return;
            }
            setTimeout(() => {
                const copy = Array.from(articleTree);
                const articles = getArticles(key);
                copy[key] = articles;
                setATree(copy);
                resolve();
            }, 5000);
        });

    useEffect(() => {
        setATree(initTreeData());

        console.log(articleTree);

    },[]);

    const content_wikis = <WikiCardGrid wikiList={wikis}/>;

    return(<Tabs
    centered
    items={[
        { "label": t("wikis.wikis"),
            "key": 1,
            "children": content_wikis
        },
        { "label": t("article.articles"),
            "key": 2,
            "children": <Tree treeData={articleTree} loadData={onLoadData}/>
    }]}/>);
};
export default UserContent;