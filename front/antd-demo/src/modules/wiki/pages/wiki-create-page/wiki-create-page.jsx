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

const WikiCreatePage = () => {
  const navigate = useNavigate();
  const [wikiData, setWikiData] = useState({
    title: "",
    description: "",
    tags: [],
  });
  const [tags, setTags] = useState([]);
  const [newTag, setNewTag] = useState("");
  const [images, setImages] = useState([]);
  const [isInputVisible, setIsInputVisible] = useState(false);
  const { locale } = useContext(SettingsContext);

  const { t } = useTranslation();

  const createTags = async (wikiId) => {
    try {
      for (const tag of tags) {
        await createWikiTag(wikiId, tag.tag, locale);
      }
      message.success("Tags created successfully!");
    } catch (error) {
      console.error("Error creating tags:", error);
      message.error("Failed to create tags.");
    }
  };

  const createWikiFunction = async () => {
    try {
      const newWiki = {
        name: wikiData.title,
        description: wikiData.description,
        author: "DefaultAuthor",
        lang: locale,
        image: images[0] || "DefaultImage", // Utiliza la primera imagen cargada o un valor predeterminado
        translate: true,
      };

      const response = await createWiki(newWiki);
      const wikiId = response.data.id;
      console.log(wikiId);

      message.success("Wiki created successfully!");

      if (tags.length > 0) {
        await createTags(wikiId);
      }

      navigate("/");
    } catch (error) {
      console.error("Error creating wiki:", error);
      message.error("Failed to create wiki.");
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
      const imageUrl = await uploadImage(file);
      setImages([...images, imageUrl]); // Agrega la URL de la imagen al estado
      message.success("Image uploaded successfully!");
      onSuccess();
    } catch (error) {
      console.error("Error uploading image:", error);
      message.error("Failed to upload image.");
      onError(error);
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
        <div className="create-wiki-item">
          <Upload
            customRequest={customRequest}
            multiple={false}
            showUploadList={false}
            accept="image/*"
          >
            <Button icon={<UploadOutlined />}>
              {t("common.upload-image-button")}
            </Button>
          </Upload>
        </div>
        <div className="image-preview-container" style={{ marginTop: "20px" }}>
          {images.map((image, index) => (
            <div
              key={index}
              className="image-preview"
              style={{ marginBottom: "10px" }}
            >
              <img
                src={image}
                alt={`Preview ${index}`}
                style={{
                  maxWidth: "100%",
                  height: "auto",
                  borderRadius: "8px",
                  border: "1px solid #ddd",
                }}
              />
            </div>
          ))}
        </div>
        <div className="create-wiki-buttons-section">
          <Button type="primary" onClick={createWikiFunction}>
            {t("common.create-button", { type: "Wiki" })}
          </Button>
          <Button onClick={() => navigate("/")}>
            {t("common.cancel-button")}
          </Button>
        </div>
      </div>
    </section>
  );
};

export default WikiCreatePage;
