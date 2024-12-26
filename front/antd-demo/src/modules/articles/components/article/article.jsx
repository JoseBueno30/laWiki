import React, { useContext } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./article.css";
import { Grid, Flex, Rate, Row, Col } from "antd";
import UserAvatar from "../../../wiki/components/avatar/user-avatar";
import SettingsContext from "../../../../context/settings-context";
import { useTranslation } from 'react-i18next';
import WikiService from "../../../wiki/service/wiki-service";

const { useBreakpoint } = Grid;
const { getWiki } = WikiService();

const Article = ({ article }) => {
  const { locale } = useContext(SettingsContext);
  const screens = useBreakpoint();
  const {t} = useTranslation()

  const navigate = useNavigate();
  const location = useLocation();

  const clickArticle = (e) =>{
    if (location.pathname.includes("/users")) {
      getWiki(article.wiki_id).then((response) => {
        navigate(location.pathname.split("/users")[0] + "/wikis/" + response.name[localStorage.getItem("locale")].replaceAll(" ", "_") + "/articles/" + article.title[locale].replaceAll(" ", "_"), {state: article});
      });
    } else {
      navigate(location.pathname.split("/search")[0] + "/articles/" + article.title[locale].replaceAll(" ", "_"), {state: article});
    }
  }

  return (
    <Row
      className="article"
      title={article.title[locale]}
      id={article.id}
      tabIndex={0}
      justify="space-around"
      align="middle"
      onClick={(clickArticle)}
    >
      <Col
        md={8}
        sm={9}
        xs={24}
        title={article.title[locale]}
        className="article-title"
        align="center"
      >
        {article.title[locale]}
      </Col>
      <Col
        md={5}
        sm={0}
        xs={24}
        title={article.author.name}
        className="article-author"
      >
        <UserAvatar username={article.author.name} justify={"center"}
              id={article.author.id} />
      </Col>
      <Col
        md={4}
        sm={5}
        xs={24}
        className="article-date"
        title={t("article.last-modified") + article.creation_date.split("T")[0]}
        align="center"
      >
        {article.creation_date.split("T")[0]}
      </Col>
      <Col md={7} sm={10} xs={24} className="article-rating" align="center">
        {article.rating.toFixed(2)}
        <Rate
          style={{ marginLeft: 10 }}
          disabled
          allowHalf
          value={article.rating}
        />
      </Col>
    </Row>
  );
};

export default Article;
