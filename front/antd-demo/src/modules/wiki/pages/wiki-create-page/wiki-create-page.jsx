import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Tag, Input, Button, message } from "antd";
import { PlusOutlined } from "@ant-design/icons";
import { useTranslation } from "react-i18next";
import "./wiki-create-page.css";
import axios from "axios";

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
  const [isInputVisible, setIsInputVisible] = useState(false);
  const [language, setLanguage] = useState("es");

  const { t: tHeader } = useTranslation("header");
  const { t: tWiki } = useTranslation("wiki");
  const { t: tEdit } = useTranslation("edit");

  const createTags = async (wikiId) => {
    try {
      const tagCreationPromises = tags.map((tag) =>
        axios.post(`http://localhost:3000/v1/tags/wikis/${wikiId}`, {
          tag: tag.tag,
          translation: true,
          lan: language,
        })
      );
      await Promise.all(tagCreationPromises);
      message.success("Tags created successfully!");
    } catch (error) {
      console.error("Error creating tags:", error);
      message.error("Failed to create tags.");
    }
  };

  const createWiki = async () => {
    try {
      const newWiki = {
        name: wikiData.title,
        description: wikiData.description,
        author: "DefaultAuthor",
        lang: language,
        image: "DefaultImage",
        translate: true,
      };

      const response = await axios.post("http://localhost:3000/v1/wikis", newWiki);
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

  return (
    <section className="create-wiki-section">
      <div className="create-wiki-container">
        <h1>{tHeader("new-wiki")}</h1>
        <div className="create-wiki-item">
          <label htmlFor="create-wiki-title" className="create-wiki-label">
            {tWiki("table-title")}
          </label>
          <Input
            id="create-wiki-title"
            value={wikiData.title}
            onChange={(e) => updateField("title", e.target.value)}
          />
        </div>

        <div className="create-wiki-item">
          <label htmlFor="create-wiki-description" className="create-wiki-label">
            {tEdit("description-label")}
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
            {tEdit("tags-label")}
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
                placeholder={tEdit("tags-newtag")}
                className="tag-input"
              />
            ) : (
              <Button
                size="small"
                icon={<PlusOutlined />}
                onClick={() => setIsInputVisible(true)}
                className="add-tag-button"
              >
                {tEdit("tags-newtag")}
              </Button>
            )}
          </div>
        </div>

        <div className="create-wiki-buttons-section">
          <Button type="primary" onClick={createWiki}>
            {tEdit("create-button", { type: "Wiki" })}
          </Button>
          <Button onClick={() => navigate("/")}>
            {tEdit("cancel-button")}
          </Button>
        </div>
      </div>
    </section>
  );
};

export default WikiCreatePage;
