import { Tabs } from "antd";
import { useContext } from "react";
import { useTranslation } from "react-i18next";
import SettingsContext from "../../../../context/settings-context";
import ArticleService from "../../../articles/service/article-service";
import UserWikis from "../UserWikis/UserWikis";

const { searchArticlesWithParams } = ArticleService();

//Las wikis funcionan
//He cambiado de idea de como hacer los articulos un monton de veces
//Hare que se llame a articles y se obtengan las wikis de los articulos
const UserContent = ({author_name=""}) => {
    const { t } = useTranslation();
    const { locale } = useContext(SettingsContext);

    const content_wikis = <UserWikis author_name={author_name} search_limit={6}/>;

    return(<Tabs
    centered
    items={[
        { "label": t("wikis.wikis"),
            "key": 1,
            "children": content_wikis
        },
        { "label": t("article.articles"),
            "key": 2,
            "children": <></>
    }]}/>);
};
export default UserContent;