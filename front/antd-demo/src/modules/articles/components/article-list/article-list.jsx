import React from "react";
import "./article-list.css";
import Article from "../article/article";
import { Grid, Flex, Row, Col } from "antd";

const { useBreakpoint } = Grid;

const ArticleList = ({ articleList }) => {
  const screens = useBreakpoint();

  return (
    <Flex className="article-list" vertical gap="small" align="center">
      <Row className="article-info" justify="space-around" align="center">
        <Col md={8} sm={9} xs={24} align="center">
          Title
        </Col>
        <Col md={5} sm={0} xs={24} align="center">
          Author
        </Col>
        <Col md={4} sm={5} xs={24} align="center">
          Last modified
        </Col>
        <Col md={7} sm={10} xs={24} align="center">
          Rating
        </Col>
      </Row>

      {articleList.map((article) => (
        <Article key={article} article={article} />
      ))}
    </Flex>
  );
};

export default ArticleList;
