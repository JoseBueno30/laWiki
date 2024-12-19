import { Tabs } from "antd";
import { useContext, useState } from "react";
import { useTranslation } from "react-i18next";
import SettingsContext from "../../../../context/settings-context";
import ArticleService from "../../../articles/service/article-service";
import UserWikis from "../UserWikis/UserWikis";
import UserArticles from "../UserArticles/UserArticles";
import { useSearchParams } from "react-router-dom";

const UserContent = ({author_name="", author_id}) => {
    const { t } = useTranslation();
    const { locale } = useContext(SettingsContext);
    const [wikiActive, setWikiActive] = useState(true);
    const [searchParams, setSearchParams] = useSearchParams();

    const onChange = (key) => {
        setWikiActive(key == "1");
    }

    const content_wikis = <UserWikis
    author_name={author_name}
    active={wikiActive}
    search_limit={3}/>;

    const content_articles = <UserArticles
    author_name={author_name}
    active={!wikiActive}
    author_id={author_id}
    search_limit={6}/>;

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