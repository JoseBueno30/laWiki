import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Tag, Input, Button, message } from "antd";
import { PlusOutlined } from "@ant-design/icons";
import axios from "axios";
import "./wiki-create-page.css";

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

  const createWiki = async () => {
    try {
      const newWiki = {
        name: wikiData.title,
        description: wikiData.description,
        author: "JuanLuis",
        lang: language,
        image: "DefaultImage",
        translate: true,
      };

      await axios.post("http://localhost:3000/v1/wikis", newWiki);
      message.success("Wiki created successfully!");
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
      setTags([...tags, { id: null, name: newTag }]);
      setNewTag("");
      setIsInputVisible(false);
    }
  };

  const removeTag = (tagToRemove) => {
    setTags(tags.filter((tag) => tag.name !== tagToRemove));
  };

  return (
    <section className="create-wiki-section">
      <div className="create-wiki-container">
        <h1>Create New Wiki</h1>
        <div className="create-wiki-item">
          <label htmlFor="create-wiki-title" className="create-wiki-label">
            Title
          </label>
          <Input
            id="create-wiki-title"
            value={wikiData.title}
            onChange={(e) => updateField("title", e.target.value)}
          />
        </div>

        <div className="create-wiki-item">
          <label htmlFor="create-wiki-description" className="create-wiki-label">
            Description
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
            Tags
          </label>
          <div className="tags-section create-wiki-textarea">
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

        <div className="create-wiki-buttons-section">
          <Button type="primary" onClick={createWiki}>
            Create Wiki
          </Button>
          <Button onClick={() => navigate("/")}>Cancel</Button>
        </div>
      </div>
    </section>
  );
};

export default WikiCreatePage;
