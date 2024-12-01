import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Tag, Input, Button, message, Spin } from "antd";
import { PlusOutlined } from "@ant-design/icons";
import axios from "axios";
import "./wiki-edit-page.css";

const { TextArea } = Input;

const WikiEditPage = () => {
  const wikiId = "674c716c2c9c223912440f89";
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
  const [language, setLanguage] = useState("es");

  const loadWikiData = async () => {
    setLoading(true);
    try {
      const response = await axios.get(
        `http://localhost:3000/v1/wikis/${wikiId}?lang=${language}`
      );
      const data = response.data;

      const currentTags = data.tags.map((tagObj) => ({
        id: tagObj.id,
        name: tagObj.tag[language],
      }));

      setWikiData({
        title: data.name[language] || "",
        description: data.description || "",
        tags: currentTags,
      });
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
        (tag) => !originalTags.some((origTag) => origTag.name === tag.name)
      );

      const deletedTags = originalTags.filter(
        (origTag) => !tags.some((tag) => tag.name === origTag.name)
      );

      for (const tag of newTags) {
        await axios.post(`http://localhost:3000/v1/tags/wikis/${wikiId}`, {
          tag: tag.name,
          translation: true,
          lan: language,
        });
      }

      for (const tag of deletedTags) {
        await axios.delete(
          `http://localhost:3000/v1/tags/${tag.id}`
        );
      }

      const updatedData = {
        name: wikiData.title,
        description: wikiData.description,
        author: "DefaultAuthor",
        lang: language,
        image: "DefaultImage",
        translate: true,
      };
      await axios.put(`http://localhost:3000/v1/wikis/${wikiId}`, updatedData);

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
    if (newTag.trim() && !tags.some((t) => t.name === newTag)) {
      setTags([...tags, { id: null, name: newTag }]);
      setNewTag("");
      setIsInputVisible(false);
    }
  };

  const removeTag = (tagToRemove) => {
    setTags(tags.filter((tag) => tag.name !== tagToRemove));
  };

  useEffect(() => {
    if (wikiId) {
      loadWikiData();
    }
  }, [wikiId, language]);

  return (
    <section className="edit-wiki-section">
      <div className="edit-wiki-container">
        {loading ? (
          <Spin></Spin>
        ) : (
          <>
            <h1>Edit Wiki Information</h1>
            <div className="edit-wiki-item">
              <label htmlFor="edit-wiki-title" className="edit-wiki-label">
                Title
              </label>
              <Input
                id="edit-wiki-title"
                value={wikiData.title}
                onChange={(e) => updateField("title", e.target.value)}
              />
            </div>

            <div className="edit-wiki-item">
              <label htmlFor="edit-wiki-description" className="edit-wiki-label">
                Description
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
                Tags
              </label>
              <div className="tags-section edit-wiki-textarea">
                {tags.map((tag) => (
                  <Tag
                    key={tag.id || tag.name}
                    closable
                    onClose={() => removeTag(tag.name)}
                    className="tag-item"
                  >
                    {tag.name}
                  </Tag>
                ))}

                {isInputVisible ? (
                  <Input
                    size="small"
                    value={newTag}
                    onChange={(e) => setNewTag(e.target.value)}
                    onPressEnter={addTag}
                    onBlur={addTag}
                    placeholder="New Tag"
                    className="tag-input"
                  />
                ) : (
                  <Button
                    size="small"
                    icon={<PlusOutlined />}
                    onClick={() => setIsInputVisible(true)}
                    className="add-tag-button"
                  >
                    New Tag
                  </Button>
                )}
              </div>
            </div>

            <div className="edit-wiki-buttons-section">
              <Button type="primary" onClick={saveWikiData}>
                Save wiki
              </Button>
              <Button onClick={() => navigate("/")}>Cancel</Button>
            </div>
          </>
        )}
      </div>
    </section>
  );
};

export default WikiEditPage;
