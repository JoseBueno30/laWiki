import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { Tag, Input, Button, message, Upload } from "antd";
import { PlusOutlined, UploadOutlined } from "@ant-design/icons";
import { useTranslation } from "react-i18next";
import "./wiki-create-page.css";
import WikiService from "../../service/wiki-service";
import SettingsContext from "../../../../context/settings-context";
import { uploadImage } from "../../../articles/service/article_service";

const { createWiki, createWikiTag } = WikiService();
const { TextArea } = Input;

const DEFAULT_IMAGE = "https://via.placeholder.com/400x300?text=Default+Image";

const WikiCreatePage = () => {
  const navigate = useNavigate();
  const [wikiData, setWikiData] = useState({
    title: "",
    description: "",
    tags: [],
  });
  const [tags, setTags] = useState([]);
  const [newTag, setNewTag] = useState("");
  const [image, setImage] = useState(DEFAULT_IMAGE);
  const [isInputVisible, setIsInputVisible] = useState(false);
  const [loadingImage, setLoadingImage] = useState(false);
  const [creatingWiki, setCreatingWiki] = useState(false);
  const { locale } = useContext(SettingsContext);
  const { t } = useTranslation();

  const createTags = async (wikiId) => {
    try {
      const tagCreationPromises = tags.map((tag) =>
        createWikiTag(wikiId, tag.tag, locale)
      );
      await Promise.all(tagCreationPromises);
      message.success(t("wikis.tags-create-success"));
    } catch (error) {
      console.error("Error creating tags:", error);
      message.error(t("wikis.tags-create-failure"));
    }
  };

  const createWikiFunction = async () => {
    try {
      setCreatingWiki(true);
      const newWiki = {
        name: wikiData.title,
        description: wikiData.description,
        author: "DefaultAuthor",
        lang: locale,
        image: image,
        translate: true,
      };

      const response = await createWiki(newWiki);
      const wikiId = response.id;
      message.success(t("wikis.wiki-create-success"));
      if (tags.length > 0) {
        await createTags(wikiId);
      }
      navigate(`/wikis/${newWiki.name.replace(/ /g, "_")}`);
    } catch (error) {
      console.error("Error creating wiki:", error);
      message.error(t("wikis.wiki-create-failure"));
    } finally {
      setCreatingWiki(false);
    }
  };

  const updateField = (field, value) => {
    setWikiData({ ...wikiData, [field]: value });
  };

  const addTag = () => {
    if (newTag.trim() && !tags.some((t) => t.name === newTag)) {
      setTags([...tags, { id: null, tag: newTag }]);
      setNewTag("");
      setIsInputVisible(false);
    }
  };

  const removeTag = (tagToRemove) => {
    setTags(tags.filter((tag) => tag.tag !== tagToRemove));
  };

  const customRequest = async ({ file, onSuccess, onError }) => {
    try {
      setLoadingImage(true);
      const image_url = await uploadImage(file);
      setImage(image_url);
      message.success(t("wikis.image-upload-success"));
      onSuccess();
    } catch (error) {
      console.error("Error uploading image:", error);
      message.error(t("wikis.image-upload-failure"));
      onError(error);
    } finally {
      setLoadingImage(false);
    }
  };

  return (
    <section className="create-wiki-section">
      <div className="create-wiki-container">
        <h1>{t("wikis.new-wiki")}</h1>
        <div className="create-wiki-item">
          <label htmlFor="create-wiki-title" className="create-wiki-label">
            {t("edit.title-label")}
          </label>
          <Input
            id="create-wiki-title"
            value={wikiData.title}
            onChange={(e) => updateField("title", e.target.value)}
          />
        </div>
        <div className="create-wiki-item">
          <label htmlFor="create-wiki-description" className="create-wiki-label">
            {t("edit.description-label")}
          </label>
          <TextArea
            id="create-wiki-description"
            value={wikiData.description}
            onChange={(e) => updateField("description", e.target.value)}
            autoSize={{ minRows: 6, maxRows: 10 }}
          />
        </div>
        <div className="create-wiki-item">
          <label htmlFor="create-wiki-tags" className="create-wiki-label">
            {t("common.tags-header")}
          </label>
          <div className="tags-section create-wiki-textarea">
            {tags.map((tag) => (
              <Tag
                key={tag.id || tag.tag}
                closable
                onClose={() => removeTag(tag.tag)}
                className="tag-item"
              >
                {tag.tag}
              </Tag>
            ))}
            {isInputVisible ? (
              <Input
                size="small"
                value={newTag}
                onChange={(e) => setNewTag(e.target.value)}
                onPressEnter={addTag}
                onBlur={addTag}
                placeholder={t("common.tags-newtag")}
                className="tag-input"
              />
            ) : (
              <Button
                size="small"
                icon={<PlusOutlined />}
                onClick={() => setIsInputVisible(true)}
                className="add-tag-button"
              >
                {t("common.tags-newtag")}
              </Button>
            )}
          </div>
        </div>
        <div className="image-preview-container create-wiki-item">
          <label className="create-wiki-label">{t("wikis.wiki-image")}</label>
          <div>
            <img className="image-preview" src={image} alt="Preview" />
          </div>
        </div>
        <div className="create-wiki-item">
          <Upload
            customRequest={customRequest}
            multiple={false}
            showUploadList={false}
            accept="image/*"
          >
            <Button
              icon={<UploadOutlined />}
              loading={loadingImage}
              iconPosition="end"
            >
              {loadingImage ? t("common.loading-button") : t("common.upload-image-button")}
            </Button>
          </Upload>
        </div>
        <div className="create-wiki-buttons-section">
          <Button
            type="primary"
            onClick={createWikiFunction}
            loading ={creatingWiki}
            iconPosition="end"
          >
            {creatingWiki ? t("common.creating-button", { type: "Wiki" }) : t("common.create-button", { type: "Wiki" })}
          </Button>
          <Button onClick={() => navigate("/")}>{t("common.cancel-button")}</Button>
        </div>
      </div>
    </section>
  );
};

export default WikiCreatePage;
