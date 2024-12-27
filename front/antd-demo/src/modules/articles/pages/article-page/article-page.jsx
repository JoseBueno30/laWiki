import React, { useContext, useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Button, Flex, Grid, Select, Spin, Tag } from "antd";
import { EditOutlined, ReloadOutlined } from "@ant-design/icons";
import CommentList from "../../../comments/components/comment-list/comment-list";
import RatingsSection from "../../../ratings/components/ratings-section";
import UserAvatar from "../../../wiki/components/avatar/user-avatar";
import "./article-page.css";
import Title from "antd/es/typography/Title";
import ArticleService from "../../service/article-service";
import CommentService from "../../../comments/service/comment-service";
import { WikiContext } from "../../../../context/wiki-context";
import SettingsContext from "../../../../context/settings-context";
import RatingService from "../../../ratings/service/rating-service";
import { useTranslation } from "react-i18next";
import JsxParser from "react-jsx-parser";
import MapView from "../../components/map-view/map-view";

const { useBreakpoint } = Grid;
let article = null;
const ArticlePage = () => {
  const { wiki } = useContext(WikiContext);
  const { locale } = useContext(SettingsContext);
  const { t } = useTranslation();

  const navigate = useNavigate();
  const location = useLocation();

  const user = JSON.parse(localStorage.getItem("user"));

  article =
    article && (!location.state || article == location.state)
      ? article
      : location.state;
  // console.log("LOCATION: ",article)
  // console.log("LOCATION: ",article)

  const screen = useBreakpoint();
  const [loading, setLoading] = useState(true);
  const [articleVersion, setArticleVersion] = useState(null);
  const [versions, setVersions] = useState([]);
  const [comments, setComments] = useState({ comments: [] });
  const [ratings, setRatings] = useState({ average: 0, total: 0, ratings: [] });
  const [userRating, setUserRating] = useState({
    rating_object: null,
    enabled: false,
  });

  const fetchArticleRatings = async () => {
    const ratings_response = await RatingService().getArticleRatings(
      articleVersion.article_id
    );

    setRatings({
      average: ratings_response.average,
      total: ratings_response.total,
      ratings: [
        ratings_response.five_count,
        ratings_response.four_count,
        ratings_response.three_count,
        ratings_response.two_count,
        ratings_response.one_count,
      ],
    });
  };

  const fetchArticleComments = async () => {
    const comments_response = await CommentService().getArticleComments(
      articleVersion.article_id,
      0,
      3,
      "recent",
      null
    );
    setComments(comments_response);
  };

  const fetchArticleVersion = async () => {
    try {
      let articleName;
      console.log("articulo", article);
      if (article) {
        articleName = article.title[locale];
      } else {
        articleName = window.location
          .toString()
          .split("/")
          .pop()
          .replaceAll("_", " ");
      }

      const version_response = await ArticleService().getArticleVersionByName(
        wiki.wiki_info.id,
        articleName,
        article ? locale : null
      );
      setArticleVersion(version_response);
    } catch (error) {
      console.error(error)
      navigate(location.pathname.split("/articles")[0] + "/article_not_found");
    }
  };

  // useEffect (() =>{
  //   return () =>{
  //     article = null
  //   }
  // })

  useEffect(() => {
    if (wiki.wiki_info) {
      fetchArticleVersion();
    }
  }, [wiki, location]);

  const fetchVersions = async () => {
    //TODO: FETC THE ARTCILE. IT HAS A LIST OF SIMPLIFIED VERSIONS, WHEN ONE VERSION IS SELECTED THEN FETCH THAT ARTICLE VERSION
    // console.log("Article ? ", article)
    if (!article) {
      const versions_response =
        await ArticleService().getArticleVersionsByArticleID(
          articleVersion.article_id,
          "recent"
        );
      setVersions(versions_response.article_versions);
    } else {
      setVersions(article.versions);
    }
  };

  const fetchUpdatedArticle = async () => {
    const article_response = await ArticleService().getArticleById(
      articleVersion.article_id
    );
    article = article_response;
    fetchVersions();
  };

  useEffect(() => {
    const fetchUserRating = async () => {
      const userRating_response = await RatingService().getUserRatingInArticle(
        user.id,
        articleVersion.article_id
      );

      setUserRating({
        rating_object: userRating_response,
        enabled: true,
      });
    };

    if (articleVersion) {
      fetchVersions();
      fetchArticleComments();
      fetchArticleRatings();
      fetchUserRating();
    }
  }, [articleVersion]);

  useEffect(() => {
    if (articleVersion && versions.length > 0) {
      setLoading(false);
    }
  }, [articleVersion, versions]);

  useEffect(() => {
    const reloadVersionWithLocale = async () => {
      if (articleVersion) {
        await fetchUpdatedArticle();
        console.log("article", article);
        fetchArticleVersion();
        changeURL();
      }
    };
    reloadVersionWithLocale();
  }, [locale]);

  const formatVersions = () => {
    let simplifiedVersions = [];

    versions.forEach((element) => {
      const newVersion = {
        value: element.id,
        label: screen.md ? (
          <span>
            {element.modification_date.substring(0, 10) +
              " " +
              element.title[locale]}
          </span>
        ) : (
          <span>{element.modification_date.substring(0, 10)}</span>
        ),
      };
      simplifiedVersions.push(newVersion);
    });
    return simplifiedVersions;
  };

  const loadVersion = async (versionId, _) => {
    const version_response = await ArticleService().getArticleVersionByID(
      versionId,
      locale
    );
    setArticleVersion(version_response);
  };

  const updateRating = async (newRatingValue) => {
    let rating_response;
    // console.log("NUEVO RATING", newRatingValue)
    if (newRatingValue == 0) {
      rating_response = await RatingService().deleteRating(
        userRating.rating_object.id
      );
      setUserRating({ rating_object: null, enabled: false });
    } else if (userRating.rating_object != null) {
      rating_response = await RatingService().updateArticleRating(
        articleVersion.article_id,
        user.id,
        newRatingValue
      );
      setUserRating({ rating_object: rating_response, enabled: true });
    } else {
      rating_response = await RatingService().createArticleRating(
        articleVersion.article_id,
        user.id,
        newRatingValue
      );
      setUserRating({ rating_object: rating_response, enabled: true });
    }
    fetchArticleRatings();
  };

  const uploadComment = async (text) => {
    await CommentService().postComment(
      articleVersion.article_id,
      user.id,
      text
    );
    fetchArticleComments();
  };

  const deleteComment = async (commentId) => {
    await CommentService().deleteComment(commentId);
    fetchArticleComments();
  };

  const controlCommentsPaginationAndFilters = async (
    newOffset,
    order,
    creation_date
  ) => {
    const comments_response = await CommentService().getArticleComments(
      articleVersion.article_id,
      newOffset,
      3,
      order,
      creation_date
    );
    setComments(comments_response);
  };

  const changeURL = () => {
    const newPart = articleVersion.title[locale];
    const sanitizedNewPart = newPart.replace(/ /g, "_");

    // Reload with new URL
    navigate(
      (
        location.pathname.split("/articles")[0] +
        "/articles/" +
        sanitizedNewPart
      ).replace(" ", "_")
    );
  };

  const editArticle = () => {
    navigate(location.pathname + "/edit", {
      state: { articleVersion: articleVersion, lan: articleVersion.lan },
    });
  };

  const restoreArticleVersion = async () => {
    const restore_response = await ArticleService().restoreArticleVersion(
      articleVersion.article_id,
      articleVersion.id
    );
    fetchUpdatedArticle();
    changeURL();
  };

  return loading ? (
    <Spin className="loading-article-page" size="large"></Spin>
  ) : (
    <section className="article-page">
      <Flex align="center" justify="space-between">
        <Flex vertical>
          <Title>{articleVersion.title[locale]}</Title>
          <Flex gap={2}>
            {articleVersion.tags.map((tag) => (
              <Tag color="geekblue">{tag.tag[locale]}</Tag>
            ))}
          </Flex>
        </Flex>

        <Flex
          gap={screen.md ? "3dvw" : 10}
          vertical={screen.md ? false : true}
          align="center"
          style={screen.md ? { paddingTop: 25 } : { paddingTop: 15 }}
        >
          <Button color="default" variant="text">
            <UserAvatar
              image={articleVersion.author.image}
              username={articleVersion.author.name}
              id={articleVersion.author.id}
            ></UserAvatar>
          </Button>

          <Select
            title={t("article.select-version")}
            options={formatVersions()}
            defaultValue={versions[0].id}
            onChange={loadVersion}
          ></Select>
          {user ? articleVersion.id == versions[0].id ? (
            <Button
              icon={<EditOutlined />}
              iconPosition="start"
              type="secondary"
              color="default"
              variant="outlined"
              onClick={editArticle}
            >
              {t("article.edit-article-button")}
            </Button>
          ) : user.id == article.author.id || user.admin ? (
            <Button
              icon={<ReloadOutlined />}
              iconPosition="start"
              type="secondary"
              color="default"
              variant="outlined"
              onClick={restoreArticleVersion}
            >
              {t("article.restore-button")}
            </Button>
          ) : <></> : <></>}
        </Flex>
      </Flex>

      <div className="article-body-container">
        {articleVersion?
        <JsxParser
        components={{ MapView }}
        jsx={articleVersion.body
          .replaceAll("<mapview", "<MapView")
          // .replaceAll("</mapview></p>", "</MapView>")
          .replaceAll("</mapview>", "</MapView>")
          .replaceAll("'{[{", "{[{")
          .replaceAll("]}'", "]}")
          .replaceAll('"{[', '{[')
          .replaceAll(']}"', ']}')
          .replaceAll('"{[{', '{[{')
          .replaceAll(']}"', ']}')
        }/>:<></>
      }
      </div>

      <Flex
        className={screen.md ? "" : "reversed"}
        style={{ padding: "10px" }}
        vertical={screen.md ? false : true}
        align={screen.md ? "start" : "center"}
      >
        <CommentList
          uploadFunc={uploadComment}
          deleteFunc={deleteComment}
          commentsObject={comments}
          user={user}
          fetchFunc={controlCommentsPaginationAndFilters}
        ></CommentList>

        <RatingsSection
          ratings={ratings.ratings}
          avg_rating={ratings.average}
          total_ratings={ratings.total}
          updateRatingFunc={updateRating}
          user_value={
            userRating.rating_object ? userRating.rating_object.value : 0
          }
        ></RatingsSection>
      </Flex>
    </section>
  );
};

export default ArticlePage;
