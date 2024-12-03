import React, { useEffect, useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { Tag, Input, Button, message, Spin } from "antd";
import { PlusOutlined } from "@ant-design/icons";
import { useTranslation } from "react-i18next";
import { WikiContext } from "../../../../context/wiki-context";
import "./wiki-edit-page.css";
import WikiService from "../../service/wiki-service";
import SettingsContext from "../../../../context/settings-context";

const { updateWiki, createWikiTag, deleteWikiTag, deleteWiki } = WikiService();
const { TextArea } = Input;

const WikiEditPage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [wikiData, setWikiData] = useState({
    title: "",
    description: "",
    tags: [],
  });
  const [tags, setTags] = useState([]);
  const [originalTags, setOriginalTags] = useState([]);
  const [newTag, setNewTag] = useState("");
  const [isInputVisible, setIsInputVisible] = useState(false);
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
      });
      console.log(wiki.wiki_info);
      setTags(currentTags);
      setOriginalTags(currentTags);
    } catch (error) {
      console.error("Error loading wiki data:", error);
      message.error("Failed to load wiki data.");
    } finally {
      setLoading(false);
    }
  };

  const saveWikiData = async () => {
    try {
      setLoading(true);

      const newTags = tags.filter(
        (tag) => !tag.id
      );
      
      const deletedTags = originalTags.filter(
        (origTag) => !tags.some((tag) => origTag.id === tag.id)
      );

      for (const tag of newTags) {
        await createWikiTag(wiki.wiki_info.id, tag, locale);
      }

      for (const tag of deletedTags) {
        await deleteWikiTag(tag.id);
      }

      const updatedData = {
        name: wikiData.title,
        description: wikiData.description,
        author: "DefaultAuthor",
        lang: locale,
        image: "DefaultImage",
        translate: true,
      };
      await updateWiki(wiki.wiki_info.id, updatedData);

      message.success("Wiki updated successfully!");
      loadWikiData();
    } catch (error) {
      console.error("Error saving wiki data:", error);
      message.error("Failed to save wiki changes.");
    } finally {
      setLoading(false);
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
      message.success("Wiki deleted successfully!");
      navigate("/");
    } catch (error) {
      console.error("Error deleting wiki:", error);
      message.error("Failed to delete wiki.");
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
          <Spin></Spin>
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

            <div className="edit-wiki-buttons-section">
              <Button type="primary" onClick={saveWikiData}>
              {t("common.save-button", { type: "Wiki" })}
              </Button>
              <Button onClick={() => navigate("/")}>
                {t("common.cancel-button")}
              </Button>
              <Button danger className="right-button" onClick={deleteWikiFunction}>
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
