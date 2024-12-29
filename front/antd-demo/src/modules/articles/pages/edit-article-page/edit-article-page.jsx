import React, { useState, useEffect, useContext } from "react";
import { useNavigate, useLocation, redirect } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { WikiContext } from "../../../../context/wiki-context";
import SettingsContext from "../../../../context/settings-context";

import {
  Tag,
  Button,
  Input,
  Upload,
  Modal,
  Flex,
  Switch,
  message,
  Spin,
  Popconfirm,
  Dropdown,
} from "antd";
import { CheckOutlined, CloseOutlined } from "@ant-design/icons";
const { TextArea } = Input;
import { PlusOutlined, UploadOutlined } from "@ant-design/icons";
import "./edit-article-page.css";
import MapConfigurator from "../../components/map-configurator/map-configurator";
import ArticleService from "../../service/article-service";
import { popup } from "leaflet";
const { createArticleVersion,
  getArticleWikiTextBody,
  getWikiTags,
  uploadImage, deleteArticleByID } = ArticleService();


const EditArticlePage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const articleData = location.state.articleVersion;

  const { t } = useTranslation();
  const { wiki } = useContext(WikiContext);
  const { locale } = useContext(SettingsContext);
  const user = JSON.parse(localStorage.getItem("user"));


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
    
    if(wiki!=null){

      if (articleData != null) {
        fetchData();
      } else {
        navigate(location.pathname.replace("/edit", ""));
      }
    }
  }, [wiki]);

  const fetchData = async() => {
    setLoading(true);
    try{
      await fetchWikiTags();
      setTitle(articleData.title[locale]);
      setTags(articleData.tags);
      await fetchWikiTextBody();

    }catch(error){

    }finally{setLoading(false);}
  }

  const fetchWikiTags = async () => {
    const tagList = await getWikiTags(wiki.wiki_info.id);
    
    setAvailableTags(tagList);
  };

  const fetchWikiTextBody = async() =>{
    const response = await getArticleWikiTextBody(articleData.id, articleData.lan);
    console.log("BODY: ", response)
    setBody(response.body);
  }

  
  const addTag = (e) => {
    const selectedTag = availableTags.find(tag => tag.id === e.key);

    setTags([...tags, selectedTag]);
    
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
      messageApi.open({
        type: "error",
        content: "Error uploading the image",
      });
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
    let articleTitle
    try {
      const newArticleVersion = {
        title: title,
        author: {
          id: user.id,
          name: user.username,
          image: user.image,
        },
        tags: tags,
        body: body,
        lan: location.state.lan,
        translate_title: translateTitle,
      };

      const response = await createArticleVersion(articleData.article_id, newArticleVersion);
      articleTitle = response.title[locale]
    } catch (error) {
      messageApi.open({
        type: "error",
        content: error.message,
      });
    } finally {
      setLoading(false);
      console.log((location.pathname.split("/articles")[0]+"/articles/" + articleTitle.replaceAll(" ", "_")))
      navigate((location.pathname.split("/articles")[0]+"/articles/" + articleTitle.replaceAll(" ", "_")));

    }
  };

  const items = (availableTags.filter(tag => !(new Set(tags.map(tag => tag.id))).has(tag.id))).map(tag => ({
    key: tag.id,
    label: tag.tag[locale],
  }));

  const menuProps = {
    items,
    onClick: addTag,
  };

  const handleDeleteArticle = async () => {
    try {
      const response = await deleteArticleByID(articleData.article_id);
      navigate(("/wikis/" + wiki.wiki_info.name[locale].replaceAll(" ", "_")));
    }catch(error){
      popup("error", "Error deleting article", error.message);
    }
  }

  return (
    <section className="edit-article-section">
      {contextHolder}
      {loading ? (
        <Spin size="large" style={{ paddingTop: "40vh" }} />
      ) : (
        <div className="edit-article-container">
          <h1>{t("edit.edit-article-header")}</h1>

          <div className="edit-article-item">
            <Flex justify="space-between" style={{ width: "100%" }}>
              <label
                htmlFor="edit-article-title"
                className="edit-article-label"
              >
                {t("edit.title-label")}
              </label>
              <div>
                {t("edit.translate-title")}
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
              value={title}
              onChange={(e) => {
                setTitle(e.target.value); console.log(title.replaceAll(" ", "_"))
              }}
            />
          </div>

          <div className="edit-article-item">
            <label htmlFor="edit-article-tags" className="edit-article-label">
              {t("edit.tags-label")}
            </label>
            <div className="tags-section edit-article-textarea">
              {tags.map((tag) => (
                <Tag
                  key={tag.id}
                  closable
                  onClose={() => removeTag(tag)}
                  className="tag-item"
                >
                  {tag.tag[locale]}
                </Tag>
              ))}

              <Dropdown
                menu={
                  menuProps
                }
                placement="bottom"
              >
                <Button>{t("edit.tags-selection")}</Button>
              </Dropdown>
            </div>
          </div>

          <Flex
            align="center"
            justify="space-evenly"
            style={{ width: "100%", paddingBottom: 0 }}
          >
            <div>
              <Button type="primary" onClick={showModal}>
                {t("edit.insert-map")}
              </Button>
              <Modal
                title="Configuración del Mapa"
                open={isModalOpen} // Aquí podrías guardar el mapa cuando se pulse OK
                width="80vw" // Ancho personalizado para adaptarse mejor al mapa
                style={{ height: "70vh", overflow: "hidden", minWidth:"350px" }} // Altura ajustada
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
                <Button icon={<UploadOutlined />}>{t("edit.insert-image")}</Button>
              </Upload>
            </div>
          </Flex>

          <div className="edit-article-item">
            <label
              htmlFor="edit-article-description"
              className="edit-article-label"
            >
              {t("edit.body-label")}
            </label>
            <TextArea
              id="edit-article-description"
              value={body} // El valor del textarea es el estado
              onChange={(e) => {
                setBody(e.target.value);
              }}
              autoSize={{ minRows: 6, maxRows: 20 }}
            />
          </div>

          <div className="edit-article-buttons-section">
            <Button
              type="primary"
              onClick={() => {
                handleSaveArticle();
              }}
            >
              {t("edit.save-button")}
            </Button>
            <Popconfirm
              title={t("edit.confirm-cancel")}
              description={t("edit.confirm-cancel-message")}
              onConfirm={confirmCancel}
              
              okText={t("edit.confirm-cancel-yes")}
              cancelText={t("edit.confirm-cancel-no")}
            >
              <Button>{t("edit.cancel-button")}</Button>
            </Popconfirm>
            
            {user.admin || user.id === articleData.author.id || user.id === wiki.wiki_info.author.id ?
              <Button onClick={handleDeleteArticle} danger className="right-button">
                Delete article
              </Button> :
              ""
            }
            
          </div>
        </div>
      )}
    </section>
  );
};
export default EditArticlePage;
