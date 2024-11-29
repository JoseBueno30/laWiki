import React from "react";
import "./wiki-recommendation-page.css";
import "../../../../assets/css/pages.css";
import WikiCardGrid from "../../components/wiki-card-grid/wiki-card-grid";

const getHighestRatedWikis = () => {
  // TODO consume real data from wiki API
  console.log("object");
  return [
    {
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
    },
    {
      id: 4,
      title: "React",
      description: "A JavaScript library for building user interfaces",
      rating: 4.9,
      image: "https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg",
    },
    {
      id: 5,
      title: "Node.js",
      description:
        "A JavaScript runtime built on Chrome's V8 JavaScript engine",
      rating: 4.8,
      image: "https://upload.wikimedia.org/wikipedia/commons/d/d9/Node.js_logo.svg",
    },
    {
      id: 6,
      title: "Angular",
      description:
        "A platform for building mobile and desktop web applications",
      rating: 4.7,
      image: "https://upload.wikimedia.org/wikipedia/commons/c/cf/Angular_full_color_logo.svg",
    },
    {
      id: 7,
      title: "React",
      description: "A JavaScript library for building user interfaces",
      rating: 4.9,
      image: "https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg",
    },
    {
      id: 8,
      title: "Node.js",
      description:
        "A JavaScript runtime built on Chrome's V8 JavaScript engine",
      rating: 4.8,
      image: "https://upload.wikimedia.org/wikipedia/commons/d/d9/Node.js_logo.svg",
    },
    {
      id: 9,
      title: "Angular",
      description:
        "A platform for building mobile and desktop web applications",
      rating: 4.7,
      image: "https://upload.wikimedia.org/wikipedia/commons/c/cf/Angular_full_color_logo.svg",
    },
    {
      id: 10,
      title: "React",
      description: "A JavaScript library for building user interfaces",
      rating: 4.9,
      image: "https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg",
    },
    {
      id: 11,
      title: "Node.js",
      description:
        "A JavaScript runtime built on Chrome's V8 JavaScript engine",
      rating: 4.8,
      image: "https://upload.wikimedia.org/wikipedia/commons/d/d9/Node.js_logo.svg",
    },
    {
      id: 12,
      title: "Angular",
      description:
        "A platform for building mobile and desktop web applications",
      rating: 4.7,
      image: "https://upload.wikimedia.org/wikipedia/commons/c/cf/Angular_full_color_logo.svg",
    },
  ];
};

const WikiRecommendationPage = () => {
  return (
    <>
      <div className="page-wrapper">
          <div className="md-flex">
              {/* TODO: Translate title */}
              <h1>Highest Rated Wikis</h1>
          </div>
          <WikiCardGrid wikiList={getHighestRatedWikis()} />
      </div>
    </>
  );
};

export default WikiRecommendationPage;
