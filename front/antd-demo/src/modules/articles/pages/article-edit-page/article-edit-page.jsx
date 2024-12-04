import React, { useState, useEffect, useContext } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { WikiContext } from "../../../../context/wiki-context";
import SettingsContext from "../../../../context/settings-context";

import {
  Tag,
  Select,
  Button,
  Input,
  Upload,
  Modal,
  Flex,
  Switch,
  message,
  Spin,
  Popconfirm 
} from "antd";
import { CheckOutlined, CloseOutlined } from "@ant-design/icons";
const { TextArea } = Input;
import { PlusOutlined, UploadOutlined } from "@ant-design/icons";
import "./article-edit-page.css";
import MapComponent from "../../components/map-component/MapComponent";
import MapConfigurator from "../../components/map-configurator/map-configurator";
import MapView from "../../components/map-view/map-view";
import ReactDOM from "react-dom/client";
import JsxParser from "react-jsx-parser";
import {
  createArticleVersion,
  getWikiTags,
  uploadImage,
} from "../../service/article_service";

const { Option } = Select;

const ArticleEditPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const articleData = location.state;

  const { t } = useTranslation("edit");
  const { wiki } = useContext(WikiContext);
  const { locale } = useContext(SettingsContext);

  const [title, setTitle] = useState("");
  const [translateTitle, setTransalateTitle] = useState(true);
  const [availableTags, setAvailableTags] = useState([]);
  const [tags, setTags] = useState([]);
  const [body, setBody] = useState("");

  const [loading, setLoading] = useState(false);
  const [messageApi, contextHolder] = message.useMessage();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const showModal = () => {
    setIsModalOpen(true);
  };

  const handleModalCancel = () => setIsModalOpen(false);

  useEffect(() => {
    if (articleData != null) {
      fetchWikiTags();
      setTitle(articleData.title[locale]);
      setTags(articleData.tags);
      setBody(articleData.body);
    } else {
      navigate(location.pathname.replace("/edit", ""));
    }
  }, []);

  const fetchWikiTags = async () => {
    const tagList = getWikiTags(wiki.wiki_info.id);
    setAvailableTags(tagList);
  };

  const addTag = (value) => {
    if (value && !tags.includes(value)) {
      setTags([...tags, value]);
    }
  };

  const removeTag = (tag) => {
    setTags(tags.filter((t) => t !== tag));
  };

  const customRequest = async ({ file, onSuccess, onError }) => {
    try {
      const imageUrl = await uploadImage(file);

      const wikiTextImage = `[[File:${imageUrl}|title=""]]`;

      setBody(`${body}\n${wikiTextImage}`);

      onSuccess();
    } catch (error) {
      console.error("Error uploading file:", error);
      onError(error);
    }
  };

  const onMapSave = (wikiTextTag) => {
    setBody(`${body}\n${wikiTextTag}`);
    setIsModalOpen(false);
  };

  const confirmCancel = (e) => {
    navigate(location.pathname.replace("/edit", ""));
  };


  const checkValidTitle = (title) => {
    const regex = /^[a-zA-Z0-9\s]*$/;
    return regex.test(title);
  };

  const handleSaveArticle = async () => {
    //create new article version and navigate to article page

    if (checkValidTitle(title) == false) {
      messageApi.open({
        type: "error",
        content: "Invalid Title. The title can't contain special characters.",
      });
      return;
    } else {
      setLoading(true);
    }

    try {
      const newArticleVersion = {
        title: title,
        author: {
          //fake data until users are implemented
          id: "672901e41a1c2dc79c930dee",
          name: "Kirito",
          image: "image_url",
        },
        tags: tags,
        body: body,
        lan: locale,
        translate_title: translateTitle,
      };

      const response = await createArticleVersion(articleData.id, newArticleVersion);
    } catch (error) {
      messageApi.open({
        type: "error",
        content: error.message,
      });
    } finally {
      setLoading(false);
      navigate(("http://localhost:5173/wikis/" + wiki.wiki_info.name + "/articles/" + title).replace(" ", "_")); //MAKE url base a variable
    }
  };

  return (
    <section className="edit-article-section">
      {contextHolder}
      {loading ? (
        <Spin size="large" style={{ paddingTop: "40vh" }} />
      ) : (
        <div className="edit-article-container">
          <h1>{t("edit-article-header")}</h1>

          <div className="edit-article-item">
            <Flex justify="space-between" style={{ width: "100%" }}>
              <label
                htmlFor="edit-article-title"
                className="edit-article-label"
              >
                {t("title-label")}
              </label>
              <div>
                {t("translate-title")}
                <Switch
                  checkedChildren={<CheckOutlined />}
                  unCheckedChildren={<CloseOutlined />}
                  checked={translateTitle}
                  onClick={() => {
                    setTransalateTitle(!translateTitle);
                  }}
                  style={{ marginLeft: 10 }}
                />
              </div>
            </Flex>
            <Input
              id="edit-article-title"
              onChange={(e) => {
                setTitle(e.target.value);
              }}
            />
          </div>

          <div className="edit-article-item">
            <label htmlFor="edit-article-tags" className="edit-article-label">
              {t("tags-label")}
            </label>
            <div className="tags-section edit-article-textarea">
              {tags.map((tag) => (
                <Tag
                  key={tag}
                  closable
                  onClose={() => removeTag(tag)}
                  className="tag-item"
                >
                  {tag}
                </Tag>
              ))}

              <Select
                placeholder={t("tags-selection")}
                style={{ width: 200 }}
                onChange={addTag}
                className="tag-select"
              >
                {availableTags
                  .filter((tag) => !tags.includes(tag))
                  .map((tag) => (
                    <Option key={tag} value={tag}>
                      {tag}
                    </Option>
                  ))}
              </Select>
            </div>
          </div>

          <Flex
            align="center"
            justify="space-evenly"
            style={{ width: "100%", paddingBottom: 0 }}
          >
            <div>
              <Button type="primary" onClick={showModal}>
                {t("insert-map")}
              </Button>
              <Modal
                title="Configuración del Mapa"
                open={isModalOpen} // Aquí podrías guardar el mapa cuando se pulse OK
                width="80vw" // Ancho personalizado para adaptarse mejor al mapa
                style={{ height: "70vh", overflow: "hidden" }} // Altura ajustada
                onCancel={handleModalCancel}
                destroyOnClose
              >
                <MapConfigurator onSave={onMapSave} />
              </Modal>
            </div>

            <div>
              <Upload
                customRequest={customRequest}
                multiple={false}
                showUploadList={false}
                accept="image/*"
              >
                <Button icon={<UploadOutlined />}>{t("insert-image")}</Button>
              </Upload>
            </div>
          </Flex>

          <div className="edit-article-item">
            <label
              htmlFor="edit-article-description"
              className="edit-article-label"
            >
              {t("body-label")}
            </label>
            <TextArea
              id="edit-article-description"
              value={body} // El valor del textarea es el estado
              onChange={(e) => {
                setBody(e.target.value);
              }}
              autoSize={{ minRows: 6, maxRows: 30 }}
            />
          </div>

          <div className="edit-article-buttons-section">
            <Button
              type="primary"
              onClick={() => {
                handleSaveArticle();
              }}
            >
              {t("save-button")}
            </Button>
            <Popconfirm
              title="Cancel"
              description="All changes will be discarded. Are you sure to cancel?"
              onConfirm={confirmCancel}
              
              okText="Yes"
              cancelText="No"
            >
              <Button>{t("cancel-button")}</Button>
            </Popconfirm>
            

            {/* TODO: Only allow the author of the article to delete it */}
            {/* <Button danger className="right-button">
              Delete article
            </Button> */}
          </div>
        </div>
      )}
    </section>
  );
};

export default ArticleEditPage;
