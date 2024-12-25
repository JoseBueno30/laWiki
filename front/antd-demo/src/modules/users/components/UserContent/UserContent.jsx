import { Tabs } from "antd";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import UserWikis from "../UserWikis/UserWikis";
import UserArticles from "../UserArticles/UserArticles";
import { useLocation, useSearchParams } from "react-router-dom";

const UserContent = ({author_name="", author_id}) => {
    const location = useLocation();
    const { t } = useTranslation();
    const [wikiActive, setWikiActive] = useState(true);
    const [searchParams, setSearchParams] = useSearchParams();

    const onChange = (key) => {
        setWikiActive(key == "1");
        location.state = null;
    }

    const content_wikis = wikiActive ? (<UserWikis
    author_name={author_name}
    active={wikiActive}
    search_limit={6}/>) : (<></>);

    const content_articles = wikiActive ? 
    (<></>) : <UserArticles
    author_name={author_name}
    active={!wikiActive}
    author_id={author_id}
    search_limit={6}/>;

    useEffect(() => {
        onChange("1");
    },[]);

    return(<Tabs
    centered
    defaultActiveKey={!searchParams.has("wiki_page") && searchParams.has("article_page")  ? "2" : "1"}
    onChange={onChange}
    items={[
        { "label": t("wikis.wikis"),
            "key": 1,
            "children": content_wikis
        },
        { "label": t("article.articles"),
            "key": 2,
            "children": content_articles
    }]}/>);
};
export default UserContent;