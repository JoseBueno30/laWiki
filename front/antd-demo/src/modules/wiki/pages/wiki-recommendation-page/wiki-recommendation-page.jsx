import React, { useEffect, useState } from "react";
import "./wiki-recommendation-page.css";
import "../../../../assets/css/pages.css";
import WikiCardGrid from "../../components/wiki-card-grid/wiki-card-grid";
import apiClient from "../../../../interceptor/interceptor";
import { Spin } from "antd";

const WikiRecommendationPage = () => {
  const [wikiList, setWikiList] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHighestRatedWikis = async () => {
      // TODO dbc: proper api call;
        const response = await apiClient.get("/v1/articles/?wiki_id=672c8721ba3ae42bd5985361");
        setWikiList([ {
          id: 1,
          title: "React ReactReactReactReactReactReactReactReactReactReactReact",
          description: "A JavaScript library for building user interfaces ",
          rating: 4.9,
          image: "https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg",
        },
        {
          id: 2,
          title: "Node.js",
          description:
            "A JavaScript runtime built on Chrome's V8 JavaScript engine",
          rating: 4.8,
          image: "https://upload.wikimedia.org/wikipedia/commons/d/d9/Node.js_logo.svg",
        },
        {
          id: 3,
          title: "Angular",
          description:
            "A platform for building mobile and desktop web applications",
          rating: 4.7,
          image: "https://upload.wikimedia.org/wikipedia/commons/c/cf/Angular_full_color_logo.svg",
        },]);
        setLoading(false);
    };

    fetchHighestRatedWikis();
  }, []);

  return (
    <>
      <div className="page-wrapper">
        <div className="md-flex">
          {/* TODO: Translate title */}
          <h1>Highest Rated Wikis</h1>
        </div>
        {loading ? (
          <Spin></Spin>
        ) : (
          <WikiCardGrid wikiList={wikiList} />
        )}
      </div>
    </>
  );
};

export default WikiRecommendationPage;
