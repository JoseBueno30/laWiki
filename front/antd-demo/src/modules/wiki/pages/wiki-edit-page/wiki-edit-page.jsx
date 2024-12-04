import React, { useEffect, useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { Tag, Input, Button, message, Spin, Upload } from "antd";
import { PlusOutlined, UploadOutlined } from "@ant-design/icons";
import { useTranslation } from "react-i18next";
import { WikiContext } from "../../../../context/wiki-context";
import "./wiki-edit-page.css";
import WikiService from "../../service/wiki-service";
import SettingsContext from "../../../../context/settings-context";
import { uploadImage } from "../../../articles/service/article_service";

const { updateWiki, createWikiTag, deleteWikiTag, deleteWiki } = WikiService();
const { TextArea } = Input;

const DEFAULT_IMAGE = "https://via.placeholder.com/400x300?text=Default+Image";

const WikiEditPage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [loadingImage, setLoadingImage] = useState(false);
  const [savingWiki, setSavingWiki] = useState(false);
  const [wikiData, setWikiData] = useState({
    title: "",
    description: "",
    tags: [],
    image: DEFAULT_IMAGE,
  });
  const [tags, setTags] = useState([]);
  const [originalTags, setOriginalTags] = useState([]);
  const [newTag, setNewTag] = useState("");
  const [isInputVisible, setIsInputVisible] = useState(false);
  const [image, setImage] = useState(DEFAULT_IMAGE);
  const { t } = useTranslation();
  const { wiki } = useContext(WikiContext);
  const { locale } = useContext(SettingsContext);

  const loadWikiData = async () => {
    setLoading(true);
    try {
      const currentTags = wiki.wiki_info.tags.map((tagObj) => ({
        id: tagObj.id,
        tag: tagObj.tag[locale],
      }));

      setWikiData({
        title: wiki.wiki_info.name[locale] || "",
        description: wiki.wiki_info.description || "",
        tags: currentTags,
        image: wiki.wiki_info.image || DEFAULT_IMAGE,
      });
      setImage(wiki.wiki_info.image || DEFAULT_IMAGE);
      setTags(currentTags);
      setOriginalTags(currentTags);
    } catch (error) {
      console.error("Error loading wiki data:", error);
      // message.error("Failed to load wiki data.");
    } finally {
      setLoading(false);
    }
  };

  const saveWikiData = async () => {
    try {
      setSavingWiki(true);
      const newTags = tags.filter((tag) => !tag.id);
      const deletedTags = originalTags.filter(
        (origTag) => !tags.some((tag) => origTag.id === tag.id)
      );

      const tagCreationPromises = newTags.map((tag) =>
        createWikiTag(wiki.wiki_info.id, tag.tag, locale)
      );
      await Promise.all(tagCreationPromises);

      const tagDeletedPromises = deletedTags.map((tag) =>
        deleteWikiTag(tag.id)
      );
      await Promise.all(tagDeletedPromises);

      const updatedData = {
        name: wikiData.title,
        description: wikiData.description,
        author: "DefaultAuthor",
        lang: locale,
        image: image,
        translate: true,
      };
      await updateWiki(wiki.wiki_info.id, updatedData);

      message.success(t("wikis.wiki-edit-success"));
      navigate(`/wikis/${updatedData.name.replace(/ /g, "_")}`);
    } catch (error) {
      console.error("Error saving wiki data:", error);
      message.error(t("wikis.wiki-edit-failure"));
    } finally {
      setSavingWiki(false);
    }
  };

  const customRequest = async ({ file, onSuccess, onError }) => {
    setLoadingImage(true);
    try {
      const imageUrl = await uploadImage(file);
      setImage(imageUrl);
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

  const updateField = (field, value) => {
    setWikiData({ ...wikiData, [field]: value });
  };

  const addTag = () => {
    if (newTag.trim() && !tags.some((t) => t.tag === newTag)) {
      setTags([...tags, { id: null, tag: newTag }]);
      setNewTag("");
      setIsInputVisible(false);
    }
  };

  const removeTag = (tagToRemove) => {
    setTags(tags.filter((tag) => tag.tag !== tagToRemove));
  };

  const deleteWikiFunction = async () => {
    try {
      await deleteWiki(wiki.wiki_info.id);
      message.success(t("wikis.wiki-delete-success"));
      navigate("/");
    } catch (error) {
      console.error("Error deleting wiki:", error);
      message.error(t("wikis.wiki-delete-failure"));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadWikiData();
  }, [wiki]);

  return (
    <section className="edit-wiki-section">
      <div className="edit-wiki-container">
        {loading ? (
          <Spin />
        ) : (
          <>
            <h1>{t("wikis.edit-wiki")}</h1>
            <div className="edit-wiki-item">
              <label htmlFor="edit-wiki-title" className="edit-wiki-label">
                {t("edit.title-label")}
              </label>
              <Input
                id="edit-wiki-title"
                value={wikiData.title}
                onChange={(e) => updateField("title", e.target.value)}
              />
            </div>

            <div className="edit-wiki-item">
              <label htmlFor="edit-wiki-description" className="edit-wiki-label">
                {t("edit.description-label")}
              </label>
              <TextArea
                id="edit-wiki-description"
                value={wikiData.description}
                onChange={(e) => updateField("description", e.target.value)}
                autoSize={{ minRows: 6, maxRows: 10 }}
              />
            </div>

            <div className="edit-wiki-item">
              <label htmlFor="edit-wiki-tags" className="edit-wiki-label">
                {t("common.tags-header")}
              </label>
              <div className="tags-section edit-wiki-textarea">
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
                    placeholder={t("common.tags-addtag")}
                    className="tag-input"
                  />
                ) : (
                  <Button
                    size="small"
                    icon={<PlusOutlined />}
                    onClick={() => setIsInputVisible(true)}
                    className="add-tag-button"
                  >
                    {t("common.tags-addtag")}
                  </Button>
                )}
              </div>
            </div>

            <div className="image-preview-container edit-wiki-item">
              <label className="edit-wiki-label">{t("wikis.wiki-image")}</label>
              <div>
                <img className="image-preview" src={image} alt="Preview" />
              </div>
            </div>

            <div className="edit-wiki-item">
              <Upload
                customRequest={customRequest}
                multiple={false}
                showUploadList={false}
                accept="image/*"
              >
                <Button 
                  icon={<UploadOutlined />} 
                  loading={loadingImage}
                  iconPosition="end">
                  {loadingImage ? t("common.loading-button") : t("common.upload-image-button")}
                </Button>
              </Upload>
            </div>

            <div className="edit-wiki-buttons-section">
              <Button type="primary" 
                onClick={saveWikiData} 
                loading={savingWiki}
                iconPosition="end">
                {savingWiki ? t("common.saving-button", { type: "Wiki" }) : t("common.save-button", { type: "Wiki" })}
              </Button>
              <Button onClick={() => navigate("/")}>
                {t("common.cancel-button")}
              </Button>
              <Button
                danger
                className="right-button"
                onClick={deleteWikiFunction}
              >
                {t("common.delete-button", { type: "Wiki" })}
              </Button>
            </div>
          </>
        )}
      </div>
    </section>
  );
};

export default WikiEditPage;
