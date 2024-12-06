

import React, { useState, useEffect, useContext } from "react";
import { useNavigate, useLocation } from "react-router-dom";
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
  Dropdown
} from "antd";
import { CheckOutlined, CloseOutlined } from "@ant-design/icons";
const { TextArea } = Input;
import { PlusOutlined, UploadOutlined } from "@ant-design/icons";
import './create-article-page.css';
import MapConfigurator from "../../components/map-configurator/map-configurator";
import {
  createArticle,
  getWikiTags,
  uploadImage,
} from "../../service/article_service";


const CreateArticlePage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const articleData = location.state;

  const { t } = useTranslation();
  const { wiki } = useContext(WikiContext);
  const { locale } = useContext(SettingsContext);

  const [title, setTitle] = useState("");
  const [translateTitle, setTransalateTitle] = useState(true);""
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
      fetchData();
    }
  }, [wiki]);

  const fetchData = async() => {
    setLoading(true);
    try{
      await fetchWikiTags();
    }catch(error){

    }finally{setLoading(false);}
  }


  const fetchWikiTags = async () => {
    const tagList = await getWikiTags(wiki.wiki_info.id);
    
    setAvailableTags(tagList);
  };

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
    navigate(location.pathname.replace("/articles/new", ""));
  };


  const checkValidTitle = (title) => {
    const regex = /^[a-zA-Z0-9\s]*$/;
    return regex.test(title);
  };

  const handleSaveArticle = async () => {
    //create new article and navigate to article page

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
      const newArticle = {
        wiki_id: wiki.wiki_info.id,
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

      const response = await createArticle(newArticle);
    } catch (error) {
      messageApi.open({
        type: "error",
        content: error.message,
      });
    } finally {
      setLoading(false);
      navigate(location.pathname.replace("/new", "/"+title).replaceAll(" ", "_"));
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
              onChange={(e) => {
                setTitle(e.target.value);
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
                  key={1}
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

export default CreateArticlePage;
