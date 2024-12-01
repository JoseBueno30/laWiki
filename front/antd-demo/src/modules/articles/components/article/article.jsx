import React, { useContext } from "react";
import "./article.css";
import { Grid, Flex, Rate, Row, Col } from "antd";
import UserAvatar from "../../../wiki/components/avatar/user-avatar";
import SettingsContext from "../../../../context/settings-context";

const { useBreakpoint } = Grid;

const Article = ({ article }) => {
  const { locale } = useContext(SettingsContext);
  const screens = useBreakpoint();

  //Match title with current language of the App

  return (
    <Row
      className="article"
      title={article.title[locale]}
      id={article.id}
      tabIndex={0}
      justify="space-around"
      align="middle"
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
        <UserAvatar username={article.author.name} justify={"center"} />
      </Col>
      <Col
        md={4}
        sm={5}
        xs={24}
        className="article-date"
        title={"Last modified: " + article.creation_date.split("T")[0]}
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
